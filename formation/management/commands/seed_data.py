"""
Commande Django pour peupler la base de données avec des données de test.
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from formation.models import CustomUser, StudentUser, Formation, Chapitre, QuizQuestion

User = get_user_model()


class Command(BaseCommand):
    help = 'Peuple la base de données avec des données de test (seed data)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Supprime toutes les données existantes avant d\'ajouter les nouvelles',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Suppression des données existantes...'))
            QuizQuestion.objects.all().delete()
            Chapitre.objects.all().delete()
            Formation.objects.all().delete()
            StudentUser.objects.all().delete()
            CustomUser.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Données supprimées avec succès.'))

        self.stdout.write(self.style.SUCCESS('Début du seed des données...'))

        # Création des utilisateurs
        self.create_users()
        
        # Création des formations et chapitres
        self.create_formations()

        self.stdout.write(self.style.SUCCESS('\n✅ Seed terminé avec succès!'))

    def create_users(self):
        """Crée les utilisateurs de test"""
        self.stdout.write('\n📝 Création des utilisateurs...')

        # Création d'un professeur
        prof, created = CustomUser.objects.get_or_create(
            username='professeur',
            defaults={
                'email': 'prof@elearning.com',
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'role': 'TEACHER',
                'is_staff': True,
            }
        )
        if created:
            prof.set_password('prof123')
            prof.save()
            self.stdout.write(self.style.SUCCESS('  ✅ Professeur créé (username: professeur, password: prof123)'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Professeur existe déjà'))

        # Création d'un étudiant
        etudiant = None
        if StudentUser.objects.filter(username='etudiant').exists():
            etudiant = StudentUser.objects.get(username='etudiant')
            self.stdout.write(self.style.WARNING('  ⚠️  Étudiant existe déjà'))
        elif CustomUser.objects.filter(username='etudiant').exists():
            self.stdout.write(self.style.WARNING('  ⚠️  Un utilisateur "etudiant" existe déjà mais n\'est pas un StudentUser'))
        else:
            etudiant, created = StudentUser.objects.get_or_create(
                username='etudiant',
                defaults={
                    'email': 'etudiant@elearning.com',
                    'first_name': 'Marie',
                    'last_name': 'Martin',
                    'role': 'STUDENT',
                }
            )
            if created:
                etudiant.set_password('etudiant123')
                etudiant.save()
                self.stdout.write(self.style.SUCCESS('  ✅ Étudiant créé (username: etudiant, password: etudiant123)'))
            else:
                self.stdout.write(self.style.WARNING('  ⚠️  Étudiant existe déjà'))

        # Création d'un autre étudiant
        if StudentUser.objects.filter(username='olsen').exists():
            self.stdout.write(self.style.WARNING('  ⚠️  Étudiant Olsen existe déjà'))
        elif CustomUser.objects.filter(username='olsen').exists():
            self.stdout.write(self.style.WARNING('  ⚠️  Un utilisateur "olsen" existe déjà mais n\'est pas un StudentUser (ignoré)'))
        else:
            etudiant2, created = StudentUser.objects.get_or_create(
                username='olsen',
                defaults={
                    'email': 'olsen@elearning.com',
                    'first_name': 'Pierre',
                    'last_name': 'Olsen',
                    'role': 'STUDENT',
                }
            )
            if created:
                etudiant2.set_password('olsen123')
                etudiant2.save()
                self.stdout.write(self.style.SUCCESS('  ✅ Étudiant Olsen créé (username: olsen, password: olsen123)'))
            else:
                self.stdout.write(self.style.WARNING('  ⚠️  Étudiant Olsen existe déjà'))

        # Retourner le professeur pour utilisation dans create_formations
        return prof

    def create_formations(self):
        """Crée les formations et chapitres avec du contenu"""
        self.stdout.write('\n📚 Création des formations...')

        prof = CustomUser.objects.get(username='professeur')

        # Formation 1: Python pour débutants
        formation1, created = Formation.objects.get_or_create(
            titre='Python pour débutants',
            defaults={
                'description': 'Une formation complète pour apprendre Python depuis le début. Découvrez les bases de la programmation, les structures de données, les fonctions, et bien plus encore.',
                'niveau': 'Débutant',
                'createur': prof,
                'est_public': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('  ✅ Formation "Python pour débutants" créée'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Formation "Python pour débutants" existe déjà'))

        # Chapitre 1.1
        chapitre1_1, created = Chapitre.objects.get_or_create(
            formation=formation1,
            titre='Introduction à Python',
            defaults={
                'ordre': 1,
                'contenu_texte': '''
Python est un langage de programmation interprété, de haut niveau et à usage général. Créé par Guido van Rossum et publié pour la première fois en 1991, Python est conçu avec une philosophie qui met l'accent sur la lisibilité du code, notamment avec l'utilisation d'espaces blancs significatifs.

Les principales caractéristiques de Python incluent:
- Syntaxe simple et claire qui facilite l'apprentissage
- Typage dynamique (les variables n'ont pas besoin d'être déclarées avec un type)
- Support de plusieurs paradigmes de programmation (orienté objet, impératif, fonctionnel)
- Grande bibliothèque standard riche en fonctionnalités
- Communauté active et nombreuse

Python est largement utilisé dans de nombreux domaines: développement web, science des données, intelligence artificielle, automatisation de tâches, développement de jeux vidéo, et bien plus encore.

Pour installer Python, vous pouvez télécharger la dernière version depuis python.org. Python 3.x est la version recommandée, car Python 2.x n'est plus maintenu depuis 2020.

Une fois Python installé, vous pouvez vérifier l'installation en ouvrant un terminal et en tapant: python --version ou python3 --version selon votre système d'exploitation.
                ''',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('    ✅ Chapitre "Introduction à Python" créé'))
        else:
            self.stdout.write(self.style.WARNING('    ⚠️  Chapitre existe déjà'))

        # Chapitre 1.2
        chapitre1_2, created = Chapitre.objects.get_or_create(
            formation=formation1,
            titre='Les variables et types de données',
            defaults={
                'ordre': 2,
                'contenu_texte': '''
En Python, les variables sont des conteneurs pour stocker des valeurs. Contrairement à d'autres langages, vous n'avez pas besoin de déclarer le type d'une variable - Python le détermine automatiquement.

Types de données de base:
1. Les entiers (int): nombres entiers positifs ou négatifs
   Exemple: age = 25

2. Les nombres à virgule flottante (float): nombres décimaux
   Exemple: prix = 19.99

3. Les chaînes de caractères (str): séquences de caractères entre guillemets
   Exemple: nom = "Marie"

4. Les booléens (bool): valeurs True ou False
   Exemple: est_actif = True

5. Les listes (list): collections ordonnées et modifiables d'éléments
   Exemple: fruits = ["pomme", "banane", "orange"]

6. Les dictionnaires (dict): collections de paires clé-valeur
   Exemple: personne = {"nom": "Jean", "age": 30}

Pour connaître le type d'une variable, vous pouvez utiliser la fonction type():
type(age)  # retourne <class 'int'>

Les variables en Python sont sensibles à la casse: nom et Nom sont deux variables différentes. Les noms de variables doivent commencer par une lettre ou un underscore, et peuvent contenir des lettres, chiffres et underscores.
                ''',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('    ✅ Chapitre "Les variables et types de données" créé'))
        else:
            self.stdout.write(self.style.WARNING('    ⚠️  Chapitre existe déjà'))

        # Formation 2: Django Web Development
        formation2, created = Formation.objects.get_or_create(
            titre='Développement Web avec Django',
            defaults={
                'description': 'Apprenez à créer des applications web modernes avec Django, le framework Python le plus populaire. De la création de modèles à l\'administration, cette formation couvre tous les aspects essentiels.',
                'niveau': 'Intermédiaire',
                'createur': prof,
                'est_public': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('  ✅ Formation "Développement Web avec Django" créée'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Formation "Développement Web avec Django" existe déjà'))

        # Chapitre 2.1
        chapitre2_1, created = Chapitre.objects.get_or_create(
            formation=formation2,
            titre='Introduction à Django',
            defaults={
                'ordre': 1,
                'contenu_texte': '''
Django est un framework web Python de haut niveau qui encourage le développement rapide et le design pragmatique. Créé en 2005, Django suit le principe "DRY" (Don't Repeat Yourself) et offre de nombreuses fonctionnalités prêtes à l'emploi.

Caractéristiques principales de Django:
- Framework MVC (Model-View-Controller) ou plus précisément MVT (Model-View-Template)
- ORM (Object-Relational Mapping) puissant pour interagir avec la base de données
- Système d'administration automatique
- Système d'URLs élégant et flexible
- Middleware pour traiter les requêtes HTTP
- Support multi-langue et internationalisation
- Sécurité intégrée contre de nombreuses vulnérabilités courantes

Pour installer Django, utilisez pip:
pip install django

Pour créer un nouveau projet Django:
django-admin startproject monprojet

La structure d'un projet Django comprend:
- settings.py: configuration du projet
- urls.py: routage des URLs
- wsgi.py: point d'entrée pour déploiement
- manage.py: script de gestion du projet

Django encourage la création d'applications modulaires qui peuvent être réutilisées dans différents projets. Pour créer une application:
python manage.py startapp monapp
                ''',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('    ✅ Chapitre "Introduction à Django" créé'))
        else:
            self.stdout.write(self.style.WARNING('    ⚠️  Chapitre existe déjà'))

        # Formation 3: Intelligence Artificielle
        formation3, created = Formation.objects.get_or_create(
            titre='Introduction à l\'Intelligence Artificielle',
            defaults={
                'description': 'Découvrez les fondamentaux de l\'IA: machine learning, réseaux de neurones, et traitement du langage naturel. Cette formation vous initie aux concepts essentiels de l\'intelligence artificielle moderne.',
                'niveau': 'Avancé',
                'createur': prof,
                'est_public': True,
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('  ✅ Formation "Introduction à l\'Intelligence Artificielle" créée'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Formation "Introduction à l\'Intelligence Artificielle" existe déjà'))

        # Chapitre 3.1
        chapitre3_1, created = Chapitre.objects.get_or_create(
            formation=formation3,
            titre='Les bases du Machine Learning',
            defaults={
                'ordre': 1,
                'contenu_texte': '''
Le Machine Learning (apprentissage automatique) est un sous-domaine de l'intelligence artificielle qui permet aux machines d'apprendre à partir de données sans être explicitement programmées pour chaque tâche.

Types d'apprentissage:
1. Apprentissage supervisé: Le modèle apprend à partir d'exemples étiquetés. L'algorithme apprend une fonction qui mappe des entrées vers des sorties en se basant sur des paires entrée-sortie d'exemples.

2. Apprentissage non supervisé: Le modèle trouve des patterns dans les données sans labels. L'algorithme essaie de trouver une structure cachée dans les données.

3. Apprentissage par renforcement: Le modèle apprend à prendre des décisions en interagissant avec un environnement et en recevant des récompenses ou des pénalités.

Le processus typique de machine learning:
1. Collecte et préparation des données
2. Sélection et entraînement du modèle
3. Évaluation des performances
4. Optimisation et ajustement
5. Déploiement du modèle

Bibliothèques Python populaires pour le ML:
- scikit-learn: pour les algorithmes classiques
- TensorFlow et PyTorch: pour les réseaux de neurones profonds
- pandas: pour la manipulation de données
- numpy: pour le calcul numérique
                ''',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('    ✅ Chapitre "Les bases du Machine Learning" créé'))
        else:
            self.stdout.write(self.style.WARNING('    ⚠️  Chapitre existe déjà'))

        self.stdout.write(self.style.SUCCESS('\n✅ Formations et chapitres créés avec succès!'))

