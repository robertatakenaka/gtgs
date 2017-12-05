from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^list/$',
        view=views.ReminderListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.ReminderRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<name>[\w-]+)/$',
        view=views.ReminderDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^update/(?P<name>[\w-]+)/$',
        view=views.ReminderUpdateView.as_view(),
        name='update'
    ),
]
