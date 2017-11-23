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
    is_checked = models.BooleanField(_('Data is checked'), default=False)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def save(self):
        super(AbstractUser, self).save()
        self.resize_photo()

    def resize_photo(self):
        if self.photo:
            image = Image.open(self.photo)
            (width, height) = image.size
            size = (100, 100)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(self.photo.path)
