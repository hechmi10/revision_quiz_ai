from django.shortcuts import render
from django.http import HttpResponse
from UserApp.models import User
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView
from django import forms

# Create your views here.
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return '/'