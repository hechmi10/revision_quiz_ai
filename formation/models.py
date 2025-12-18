from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# ---------------------------------------------------------
# 1. GESTION DES UTILISATEURS (Basé sur ton UML)
# ---------------------------------------------------------

class CustomUser(AbstractUser):
    """
    Classe parente pour tous les utilisateurs.
    Hérite de AbstractUser (gère déjà username, password, email, first_name, last_name).
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    date_naissance = models.DateField(null=True, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.username

class StudentUser(CustomUser):
    """
    Modèle spécifique pour les étudiants.
    """
    date_inscription = models.DateField(auto_now_add=True)
    progression_globale = models.IntegerField(default=0)
    badges_obtenus = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name = "Étudiant"

# ---------------------------------------------------------
# 2. STRUCTURE PÉDAGOGIQUE (Formation -> Chapitre)
# ---------------------------------------------------------

class Formation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    niveau = models.CharField(max_length=50)
    # Lien vers le créateur (Professeur)
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='formations_creees')
    est_public = models.BooleanField(default=False)

    def __str__(self):
        return self.titre

class Chapitre(models.Model):
    titre = models.CharField(max_length=200)
    contenu_texte = models.TextField(verbose_name="Contenu du cours")
    ordre = models.IntegerField(default=1)
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='chapitres')
    # Résumé généré par IA stocké ici
    resume_ia = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.formation.titre} - {self.titre}"

# ---------------------------------------------------------
# 3. LE QUIZ (TA DEMANDE SPÉCIFIQUE)
# ---------------------------------------------------------

class QuizQuestion(models.Model):
    """
    Représente une question de QCM liée à un chapitre.
    """
    question_texte = models.TextField(verbose_name="Énoncé")
    
    # Les 4 choix
    choix_A = models.CharField(max_length=255)
    choix_B = models.CharField(max_length=255)
    choix_C = models.CharField(max_length=255)
    choix_D = models.CharField(max_length=255)
    
    # La bonne réponse
    REPONSE_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]
    bonne_reponse = models.CharField(max_length=1, choices=REPONSE_CHOICES)
    
    explication = models.TextField(help_text="Explication pédagogique de la solution")
    
    # Métadonnées
    generee_ia = models.BooleanField(default=False)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE, related_name='questions')
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.question_texte[:50]

class QuizResult(models.Model):
    """
    Stocke le résultat d'un étudiant à un quiz sur un chapitre donné.
    """
    score = models.IntegerField(help_text="Score sur 100 ou nombre de bonnes réponses")
    date_passage = models.DateTimeField(auto_now_add=True)
    
    # Stockage détaillé
    reponses_etudiant = models.JSONField(help_text="Format: {'question_id': 'A'}")
    explications_erreurs = models.JSONField(null=True, blank=True, help_text="Retours IA spécifiques")
    
    # Relations
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    # Utilisation de AUTH_USER_MODEL pour permettre à tous les utilisateurs de passer des quiz
    etudiant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resultats_quiz')

    def __str__(self):
        return f"Résultat {self.etudiant} - Chapitre {self.chapitre.id}"