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
        return User.objects.filter(is_checked_by_admin=True)
    if datename == 'birthdate':
        if d == 0:
            return User.objects.filter(is_checked_by_admin=True, birthdate__month=m)
        return User.objects.filter(is_checked_by_admin=True, birthdate__month=m, birthdate__day=d)
    elif datename == 'anniversary':
        if d == 0:
            return User.objects.filter(is_checked_by_admin=True, anniversary__month=m)
        return User.objects.filter(is_checked_by_admin=True, anniversary__month=m, anniversary__day=d)


def user_ordered_by_month_day(datename, month_day=None):
    month, day = parse_month_day(month_day)
    selection = select_by_month_day(datename, month, day)
    return selection.extra(
            select={'month': SQL_MONTH.format(datename),
                    'day': SQL_DAY.format(datename)},
            order_by=['month', 'day']
            )


def get_months():
    birthday = []
    anniversary = []
    a_users = []
    b_users = []
    for user in User.objects.filter(is_checked_by_admin=True).order_by('birthdate', 'anniversary'):
        month = user.birthdate.isoformat()[5:7]
        if month not in birthday:
            birthday.append(month)
            b_users.append(user.id)
        month = user.anniversary.isoformat()[5:7]
        if month not in anniversary:
            anniversary.append(month)
            a_users.append(user.id)
    return birthday, anniversary


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    birthdate = models.DateField(_('Birthdate (DD/MM/AAAA)'), default=now)
    anniversary = models.DateField('Data de admissão (DD/MM/AAAA)', default=now)
    photo = models.ImageField(_('Photo'), default=settings.MEDIA_ROOT +'/photo.png')
    is_checked = models.BooleanField(_('Confirmo que meus dados estão atualizados'), default=False)
    is_checked_by_admin = models.BooleanField(_('Validado'), default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def fullname(self):
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
            if width > 200:
                fixed_w = 200
                r = 200.0 / width
                fixed_h = int(r * height)
            else:
                fixed_w = 200
                r = width / 200.0 
                fixed_h = int(r * height)
            size = (fixed_w, fixed_h)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.photo.path)
