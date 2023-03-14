from typing import Any, Dict

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse
from django.template.response import TemplateResponse

from . import forms, models


def feedback(request: WSGIRequest) -> HttpResponse:
    template = r'feedback\feedback.html'
    feedback_form = forms.FeedbackForm()
    data: Dict[str, Any] = {}
    if request.method == 'POST':
        feedback_form = forms.FeedbackForm(
            request.POST or None, request.FILES or None
        )
        if feedback_form.is_valid():
            email = request.POST['email']
            text = request.POST['text']
            name = request.POST['name']
            models.Feedback.objects.create_feedback(
                name, email, text, request.FILES.getlist('files')
            )
            data['status_good'] = 'Сообщение отправлено'
    data['feedback_form'] = feedback_form
    response: HttpResponse = TemplateResponse(request, template, data)
    return response
