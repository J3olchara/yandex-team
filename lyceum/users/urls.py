from django.urls import path

# isort: off
from users import views  # noqa: I100

# isort: on

app_name = 'users'

urlpatterns = [
    path('user_list/', views.UserList.as_view(), name='list'),
    path(
        'user_detail/<nat:pk>/',
        views.UserDetail.as_view(),
        name='details',
    ),
    path('profile/', views.Profile.as_view(), name='profile'),
]
