from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home_view, name='home'),
    
    # Générer le quiz via l'IA (Action prof)
    path('chapitre/<int:chapitre_id>/generer/', views.generer_quiz_view, name='generer_quiz'),
    
    # Afficher et passer le quiz (Action étudiant)
    path('quiz/<int:quiz_id>/', views.quiz_detail_view, name='quiz_detail'),
    
    # Afficher les résultats du quiz
    path('resultat/<int:result_id>/', views.quiz_result_view, name='quiz_result'),
]