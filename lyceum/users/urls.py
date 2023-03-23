from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('user_list/', views.user_list, name='list'),
    path('user_detail/<nat:user_id>/', views.user_detail, name='details'),
    path('profile/', views.profile, name='profile'),
]
