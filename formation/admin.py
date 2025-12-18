from django.contrib import admin
from .models import CustomUser, StudentUser, Formation, Chapitre, QuizQuestion, QuizResult

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'niveau', 'createur')

@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'formation', 'ordre')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_texte', 'chapitre', 'generee_ia')
    list_filter = ('chapitre', 'generee_ia')

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'chapitre', 'score', 'date_passage')