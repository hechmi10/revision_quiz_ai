from django.db import models

# Create your models here.
class Chapitre(models.Model):
    titre = models.CharField(max_length=100)
    contenu_texte = models.TextField()
    ordre = models.IntegerField()
    formation = models.ForeignKey(
        'FormationApp.Formation', 
        on_delete=models.CASCADE,
        related_name='chapitres'
    )
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name = "Chapitre"
        verbose_name_plural = "Chapitres"
        ordering = ['formation', 'ordre']