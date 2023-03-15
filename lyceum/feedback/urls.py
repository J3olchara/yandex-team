from django.urls import path, register_converter

from . import converters, views

register_converter(converters.BooleanConverter, 'bool')

app_name = 'feedback'

urlpatterns = [
    path('<bool:feedback_status>', views.feedback, name='feedback'),
    path('', views.feedback, name='feedback'),
]
