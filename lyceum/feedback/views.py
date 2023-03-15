from typing import Any, Dict

from django.core import mail
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, redirect
from django.template.response import TemplateResponse

from . import forms


def feedback(
    request: WSGIRequest, feedback_status: bool = False
) -> HttpResponse:
    template = r'feedback\feedback.html'
    feedback_form = forms.FeedbackForm(
        request.POST or None, request.FILES or None
    )
    data: Dict[str, Any] = {
        'feedback_form': feedback_form,
        'status': feedback_status,
    }
    if feedback_form.is_valid():
        email = request.POST['email']
        text = request.POST['text']
        name = request.POST['name']
        mail.send_mail(
            subject=f'Feedback from {name}',
            from_email=email,
            message=text,
            recipient_list=['yoursite@gmail.com'],
        )
        feedback_form.save(files=request.FILES.getlist('files'))
        return redirect('feedback:feedback', feedback_status=1)
    return TemplateResponse(request, template, data)
