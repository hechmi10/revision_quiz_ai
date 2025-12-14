from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ChapitreApp.models import Chapitre
from FormationApp.models import Formation
from django.views.generic import ListView
# Create your views here.
class FormationListView(LoginRequiredMixin, ListView):
    model = Formation
    template_name = 'formation_list.html'
    context_object_name = 'formations'
    login_url = '/login/'

    def get_queryset(self):
        # Prefetch chapters to avoid N+1 queries when rendering formations with their chapters
        return (
            Formation.objects.all()
            .prefetch_related('chapitres')
            .order_by('titre')
        )