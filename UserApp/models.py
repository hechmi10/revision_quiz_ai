from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    role = models.CharField(max_length=50, choices=[ ('student', 'Student'), ('instructor', 'Instructor')], default='student')
    specialite = models.CharField(max_length=100, blank=False, null=False)
    niveau_etude = models.CharField(max_length=100, blank=False, null=False)
    date_naissance = models.DateField(blank=False, null=False)
    preferences=models.JSONField(blank=False, null=False, default=dict)

class AdminUser(User):
    department = models.CharField(max_length=100, blank=False, null=False)
    permissions= models.JSONField(blank=False, null=False, default=dict)


    def save(self, *args, **kwargs):
        self.role = 'admin'
        super().save(*args, **kwargs)
class InstructorUser(User):
    principal_module = models.CharField(max_length=100, blank=False, null=False)
    experience_enseignement = models.IntegerField(blank=False, null=False)
    diploma = models.CharField(max_length=100, blank=False, null=False)
    formations_enseignees = models.JSONField(blank=False, null=False, default=list)

    def save(self, *args, **kwargs):
        self.role = 'instructor'
        super().save(*args, **kwargs)
class StudentUser(User):
    inscripted_formation = models.CharField(blank=False, null=False, max_length=100)
    progression_globale = models.IntegerField(blank=False, null=False)
    obtained_badges = models.JSONField(blank=False, null=False, default=list)

    def save(self, *args, **kwargs):
        self.role = 'student'
        super().save(*args, **kwargs)
