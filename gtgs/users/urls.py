from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^~list/(?P<status>[\w.@+-]+)/$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^birthday/$',
        view=views.UserBirthdayListView.as_view(),
        name='birthday'
    ),
    url(
        regex=r'^anniversary/$',
        view=views.UserAnniversaryListView.as_view(),
        name='anniversary'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
    url(
        regex=r'^~update_dates/(?P<username>[\w.@+-]+)/$',
        view=views.UserDatesUpdateView.as_view(),
        name='update_dates'
    ),
]
