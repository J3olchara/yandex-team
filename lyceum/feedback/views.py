from typing import Any, Dict

from django.core import mail
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic

from . import forms


def feedback(
    request: WSGIRequest, feedback_status: bool = False
) -> HttpResponse:
    """
    Feedback page

    returns feedback form page;
    validates and saves feedback forms;
    """
    template = 'feedback/feedback.html'
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


class Feedback(generic.FormView):
    """
    Feedback page

    returns feedback form page;
    validates and saves feedback forms;
    """
    template_name = 'feedback/feedback.html'
    form_class = forms.FeedbackForm
    success_url = reverse_lazy('feedback:feedback', kwargs={'feedback_status': 1})

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super(Feedback, self).get_form_kwargs()
        return {
            **kwargs,
            **self.request.POST
        }
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(Feedback, self).get_context_data(**kwargs)
        context['status'] = self.kwargs['feedback_status']
        return context
        
    def form_valid(self, form: forms.FeedbackForm) -> HttpResponse:
        email = self.request.POST().get('email')
        text = self.request.POST().get('text')
        name = self.request.POST().get('name')
        mail.send_mail(
            subject=f'Feedback from {name}',
            from_email=email,
            message=text,
            recipient_list=['yoursite@gmail.com'],
        )
        form.save(files=self.request.FILES().getlist('files'))
        return super(Feedback, self).form_valid(form)
