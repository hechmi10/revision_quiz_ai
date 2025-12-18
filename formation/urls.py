from django.urls import path
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home_view, name='home'),
    
    # Liste des formations
    path('formations/', views.formation_list_view, name='formation_list'),
    
    # Détails d'une formation
    path('formation/<int:formation_id>/', views.formation_detail_view, name='formation_detail'),
    
    # Liste des chapitres
    path('chapitres/', views.chapitre_list_view, name='chapitre_list'),
    
    # Générer le quiz via l'IA (Action prof)
    path('chapitre/<int:chapitre_id>/generer/', views.generer_quiz_view, name='generer_quiz'),
    
    # Afficher et passer le quiz (Action étudiant)
    path('quiz/<int:quiz_id>/', views.quiz_detail_view, name='quiz_detail'),
    
    # Afficher les résultats du quiz
    path('resultat/<int:result_id>/', views.quiz_result_view, name='quiz_result'),
    
    # Authentication routes
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]