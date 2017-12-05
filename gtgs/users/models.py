from datetime import datetime

from PIL import Image

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


SQL_MONTH = 'MONTH({})'
SQL_DAY = 'DAY({})'

SQL_MONTH = 'EXTRACT(MONTH FROM {})'
SQL_DAY = 'EXTRACT(DAY FROM {})'

WIDTH = 150
HEIGHT = 165


def parse_month_day(month_day=None):
    m = 0
    d = 0
    if month_day is not None:
        if month_day == '99':
            month_day = datetime.now().isoformat()[5:7]
        if '-' in month_day:
            m, d = month_day.split('-')
            m = int(m)
            d = int(d)
        else:
            d = 0
            m = int(month_day)
    return m, d


def select_by_month_day(datename, m, d):
    if d + m == 0:
        if datename == 'birthdate':
            return User.objects.filter(is_checked_by_admin=True)
        return User.objects.filter(is_checked_by_admin=True, anniversary_alert=True)
    if datename == 'birthdate':
        if d == 0:
            return User.objects.filter(is_checked_by_admin=True, birthdate__month=m)
        return User.objects.filter(is_checked_by_admin=True, birthdate__month=m, birthdate__day=d)
    elif datename == 'anniversary':
        if d == 0:
            return User.objects.filter(is_checked_by_admin=True, anniversary_alert=True, anniversary__month=m)
        return User.objects.filter(is_checked_by_admin=True, anniversary_alert=True, anniversary__month=m, anniversary__day=d)


def user_ordered_by_month_day(datename, month_day=None):
    month, day = parse_month_day(month_day)
    selection = select_by_month_day(datename, month, day)
    return selection.extra(
            select={'month': SQL_MONTH.format(datename),
                    'day': SQL_DAY.format(datename)},
            order_by=['month', 'day']
            )


def get_sysadmin_email():
    return [user.email for user in User.objects.filter(is_superuser=True)]


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    birthdate = models.DateField(_('Data de nascimento (DD/MM/AAAA)'), default=now)
    anniversary = models.DateField('Data de admissão (DD/MM/AAAA)', default=now)
    photo = models.ImageField(_('Foto'), default=settings.MEDIA_ROOT +'/perfil.png')
    is_checked = models.BooleanField(_('Confirmo que estes dados estão atualizados'), default=False)
    is_checked_by_admin = models.BooleanField(_('Validado'), default=False)
    anniversary_alert = models.BooleanField(_('Alertar tempo de SciELO'), default=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def fullname(self):
        if all([self.first_name, self.last_name]):
            if self.first_name + self.last_name != '':
                return ' '.join([self.first_name, self.last_name])
        if self.email != '':
            return self.email[:self.email.find('@')].replace('.', ' ').title()
        if self.username:
            return self.username.replace('.', ' ').title()

    def status(self):
        if self.is_checked and self.is_checked_by_admin:
            return 'valid'
        if self.is_checked:
            return 'updated'
        return 'pending'

    def registration_status(self):
        if self.is_checked and self.is_checked_by_admin:
            return '100'
        if self.is_checked:
            return '60'
        return '30'

    def years(self):
        current = datetime.now().isoformat()[:4]
        d = self.anniversary.isoformat()[:4]
        return int(current) - int(d)

    def display_years(self):
        y = self.years()
        if y > 1:
            return '{} anos de SciELO'.format(y)
        if y == 1:
            return '{} ano de SciELO'.format(y)
        return ''

    def save(self, *args, **kwargs):
        super(AbstractUser, self).save(*args, **kwargs)
        self.resize_photo()

    def resize_photo(self):
        if self.photo is not None:
            image = Image.open(self.photo)
            (width, height) = image.size
            fixed_w = width
            fixed_h = height
            fixed_w = WIDTH
            r = float(WIDTH) / width
            fixed_h = int(r * height)
            size = (fixed_w, fixed_h)
            image = image.resize(size, Image.ANTIALIAS)
            if fixed_h > HEIGHT:
                y = (fixed_h - HEIGHT) // 2
                image = image.crop((0, y, WIDTH, HEIGHT))

            image.save(self.photo.path)
