from typing import Any, Dict

from django.core import mail
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from . import forms


class Feedback(generic.FormView):  # type: ignore[type-arg]
    """
    Feedback page

    returns feedback form page;
    validates and saves feedback forms;
    """

    template_name = 'feedback/feedback.html'
    form_class = forms.FeedbackForm
    success_url = reverse_lazy(
        'feedback:feedback', kwargs={'feedback_status': 1}
    )

    def get_form_kwargs(self) -> Dict[str, Any]:
        return {'data': self.request.POST or None}

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(Feedback, self).get_context_data(**kwargs)
        if self.kwargs.get('feedback_status'):
            context['status'] = self.kwargs['feedback_status']
        return context

    def form_valid(self, form: forms.FeedbackForm) -> HttpResponse:
        email = form.cleaned_data['email']
        text = form.cleaned_data['text']
        name = form.cleaned_data['name']
        mail.send_mail(
            subject=f'Feedback from {name}',
            from_email=email,
            message=text,
            recipient_list=['yoursite@gmail.com'],
        )
        form.save(files=self.request.FILES.getlist('files'))
        return super(Feedback, self).form_valid(form)
