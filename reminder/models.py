from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


# Create your models here.
@python_2_unicode_compatible
class Reminder(models.Model):

    @classmethod
    def create(cls, name='idle'):
        reminder = cls(name=name)
        # do something with the reminder
        return reminder

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Nome'), blank=False, max_length=255)
    email_from = models.EmailField(_('E-mail from'), blank=False)
    email_to = models.EmailField(_('E-mail para'), blank=False)
    email_to_alt = models.EmailField(_('E-mail para (alternativo)'), blank=True)
    is_active = models.BooleanField(_('Ativo'), default=False)
    default_date = models.CharField(_('Date (MM-DD)'), blank=True, max_length=5)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reminder:detail', kwargs={'name': self.name})

