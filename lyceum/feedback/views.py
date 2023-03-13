from typing import Dict, Any

from django.core import mail
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse
from django.template.response import TemplateResponse

from . import forms


def feedback(request: WSGIRequest) -> HttpResponse:
    template = r'feedback\feedback.html'
    feedback_form = forms.FeedbackForm()
    data: Dict[str, Any] = {}
    if request.method == 'POST':
        feedback_form = forms.FeedbackForm(request.POST or None)
        if feedback_form.is_valid():
            email = request.POST['email']
            text = request.POST['text']
            mail.send_mail(
                subject='Feedback',
                from_email=email,
                message=text,
                recipient_list=['to@gmail.com'],
            )
            data['status_good'] = 'Сообщение отправлено'
    data['feedback_form'] = feedback_form
    response: HttpResponse = TemplateResponse(request, template, data)
    return response
