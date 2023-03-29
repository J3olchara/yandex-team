"""ABOUT app html views"""
from django.views import generic


class Description(generic.TemplateView):
    template_name = 'about/about_us.html'
