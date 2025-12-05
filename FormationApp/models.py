from django.db import models

# Create your models here.
class Formation(models.Model):
    titre= models.CharField(max_length=100)
    description= models.TextField()
    niveau= models.CharField(max_length=50)
    domaine= models.CharField(max_length=100)
    creator= models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='formations_created')
    
    def __str__(self):
        return self.titre
    
    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"