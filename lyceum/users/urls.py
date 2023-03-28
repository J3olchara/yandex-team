from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('user_list/', views.UserList.as_view(), name='list'),
    path(
        'user_detail/<nat:user_id>/',
        views.UserDetail.as_view(),
        name='details',
    ),
    path('profile/', views.Profile.as_view(), name='profile'),
]
