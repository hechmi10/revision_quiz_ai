from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from FormationApp.models import Formation
from ChapitreApp.models import Chapitre

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['formations_count'] = Formation.objects.count()
            context['chapitres_count'] = Chapitre.objects.count()
        return context
