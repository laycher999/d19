from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib import messages
from allauth.account.views import SignupView
from allauth.account.views import LoginView

class SignUpView(SignupView):
    template_name = 'signup.html'
    form_class = CustomUserCreationForm  # ваша форма

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.request.session.get('allauth_signup', None)
        return context