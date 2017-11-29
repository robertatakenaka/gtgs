from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User
from .models import user_ordered_by_month_day


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['photo', 'birthdate', 'anniversary', 'is_checked']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        status = int(self.kwargs.get('status', 0))
        if status == 0:
            return User.objects.all().order_by('email')

        is_checked = True
        is_checked_by_admin = True
        if status == 1:
            is_checked = False
            is_checked_by_admin = False
        elif status == 2:
            is_checked = True
            is_checked_by_admin = False
        return User.objects.filter(
            is_checked=is_checked,
            is_checked_by_admin=is_checked_by_admin
            ).order_by('email')


class UserBirthdayListView(ListView):
    template_name = 'users/birthday_list.html'
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        month = self.kwargs.get('month')
        return user_ordered_by_month_day('birthdate', month)


class UserAnniversaryListView(ListView):
    template_name = 'users/anniversary_list.html'
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        month = self.kwargs.get('month')
        return user_ordered_by_month_day('anniversary', month)


class UserDatesUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_form_dates.html'
    fields = [
        'photo',
        'birthdate',
        'anniversary',
        'is_checked',
        'is_checked_by_admin',
        'is_active',
        ]

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.kwargs['username']})

    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.kwargs['username']})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.kwargs['username'])
