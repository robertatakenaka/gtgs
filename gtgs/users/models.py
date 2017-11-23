from datetime import datetime

from PIL import Image

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


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
        self.resize_photo()
        super(AbstractUser, self).save(*args, **kwargs)

    def resize_photo(self):
        if self.photo:
            image = Image.open(self.photo)
            (width, height) = image.size
            size = (100, 100)
            if image.size != size:
                image = image.resize(size, Image.ANTIALIAS)
                image.save(self.photo.path)
