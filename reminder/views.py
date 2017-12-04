
# Create your views here.
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Reminder


class ReminderDetailView(LoginRequiredMixin, DetailView):
    model = Reminder
    # These next two lines tell the view to index lookups by name
    slug_field = 'name'
    slug_url_kwarg = 'name'


class ReminderRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('reminder:detail',
                       kwargs={'name': self.request.name})


class ReminderUpdateView(LoginRequiredMixin, UpdateView):

    fields = [
        'name',
        'email_from',
        'email_to',
        'is_active',
        'hour',
        ]

    # we already imported Reminder in the view code above, remember?
    model = Reminder

    # send the reminder back to their own page after a successful update
    def get_success_url(self):
        return reverse('reminder:detail',
                       kwargs={'name': self.request.name})

    def get_object(self):
        # Only get the Reminder record for the reminder making the request
        reminder = Reminder.objects.get(name=self.request.name)
        return reminder


class ReminderListView(LoginRequiredMixin, ListView):
    model = Reminder
    # These next two lines tell the view to index lookups by name
    slug_field = 'name'
    slug_url_kwarg = 'name'

