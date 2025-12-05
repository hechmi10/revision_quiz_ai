from django.shortcuts import render
from django.http import HttpResponse
from UserApp.models import User
from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView
# Create your views here.
class RegisterView(FormView):
    template_name = 'register.html'
    model = User
    fields = ['username', 'email', 'password']
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return '/'