from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from ChapitreApp.models import Chapitre
from FormationApp.models import Formation
from django.views.generic import ListView
# Create your views here.
class ChapitreListView(LoginRequiredMixin, ListView):
    model = Chapitre
    template_name = 'chapitre_list.html'
    context_object_name = 'chapitres'
    login_url = '/login/'

    def get_queryset(self):
        return Chapitre.objects.all().order_by('formation__titre', 'ordre')