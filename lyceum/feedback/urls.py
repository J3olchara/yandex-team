from django.urls import path, register_converter

# isort: off
from feedback import converters, views  # noqa: I100

# isort: on

register_converter(converters.BooleanConverter, 'bool')

app_name = 'feedback'

urlpatterns = [
    path('<bool:feedback_status>', views.Feedback.as_view(), name='feedback'),
    path('', views.Feedback.as_view(), name='feedback'),
]
