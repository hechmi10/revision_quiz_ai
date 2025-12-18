"""
Vues Django pour la gestion des quiz
- home_view : Page d'accueil
- generer_quiz_view : Génération de quiz via IA (professeur)
- quiz_detail_view : Affichage et passage du quiz (étudiant)
- quiz_result_view : Affichage des résultats avec feedbacks IA
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from .models import Chapitre, QuizQuestion, QuizResult, StudentUser, Formation
from .services import ServiceIA

logger = logging.getLogger(__name__)


def home_view(request):
    """
    Vue d'accueil qui liste les formations disponibles.
    """
    formations = Formation.objects.all().order_by('-id')
    
    context = {
        'formations': formations,
    }
    return render(request, 'formation/home.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def generer_quiz_view(request, chapitre_id):
    """
    Vue pour générer un quiz via l'IA (accès professeur).
    
    GET : Affiche le formulaire de génération
    POST : Génère le quiz et redirige vers la liste des quiz
    """
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    
    # Vérification des permissions (optionnel : vérifier que l'utilisateur est professeur)
    # if request.user.role != 'TEACHER':
    #     messages.error(request, "Vous n'avez pas les permissions pour générer un quiz.")
    #     return redirect('some_view')
    
    if request.method == "POST":
        try:
            # Récupération des paramètres du formulaire
            nombre_questions = int(request.POST.get('nombre_questions', 5))
            difficulte = request.POST.get('difficulte', 'Moyen')
            
            # Validation
            nombre_questions = max(5, min(20, nombre_questions))
            if difficulte not in ['Facile', 'Moyen', 'Difficile']:
                difficulte = 'Moyen'
            
            logger.info(f"Génération de quiz demandée : {nombre_questions} questions, difficulté {difficulte}")
            
            # Initialisation du service IA
            service = ServiceIA()
            
            # Génération du quiz
            donnees_questions = service.generer_quiz(
                chapitre=chapitre,
                nombre_questions=nombre_questions,
                difficulte=difficulte
            )

            # chapitre.questions.all().delete()
            
            # Enregistrement des nouvelles questions
            questions_creees = []
            for data in donnees_questions:
                # Conversion de l'index (0-3) en lettre (A-D)
                index_bonne_reponse = data['bonne_reponse']
                lettre_bonne_reponse = ['A', 'B', 'C', 'D'][index_bonne_reponse]
                
                question = QuizQuestion.objects.create(
                    question_texte=data['question'],
                    choix_A=data['choix'][0],
                    choix_B=data['choix'][1],
                    choix_C=data['choix'][2],
                    choix_D=data['choix'][3],
                    bonne_reponse=lettre_bonne_reponse,
                    explication=data['explication'],
                    chapitre=chapitre,
                    createur=request.user,
                    generee_ia=True
                )
                questions_creees.append(question)
            
            messages.success(
                request,
                f"✅ Quiz généré avec succès ! {len(questions_creees)} questions créées pour le chapitre '{chapitre.titre}'."
            )
            
            # Redirection vers la page de détail du quiz
            return redirect('quiz_detail', quiz_id=chapitre.id)
            
        except ValueError as e:
            logger.error(f"Erreur de validation : {e}")
            messages.error(request, f"❌ Erreur de validation : {str(e)}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du quiz : {e}")
            erreur_message = str(e)
            # Détection des erreurs de quota pour message personnalisé
            if "quota" in erreur_message.lower() or "429" in erreur_message:
                messages.error(
                    request,
                    "❌ Le quota de l'API OpenAI a été dépassé. "
                    "La génération du quiz nécessite un quota disponible sur votre compte OpenAI. "
                    "Veuillez vérifier votre plan et vos informations de facturation, ou réessayez plus tard."
                )
            else:
                messages.error(
                    request,
                    f"❌ Erreur lors de la génération du quiz : {erreur_message}. Veuillez réessayer."
                )
    
    # GET : Affichage du formulaire
    context = {
        'chapitre': chapitre,
        'nombre_questions_actuel': chapitre.questions.count(),
    }
    return render(request, 'formation/generer_quiz.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def quiz_detail_view(request, quiz_id):
    """
    Vue pour afficher et passer un quiz (accès étudiant).
    
    GET : Affiche le quiz avec toutes les questions
    POST : Traite les réponses, crée le résultat et redirige vers les résultats
    """
    # Récupération du chapitre (on utilise quiz_id comme chapitre_id pour simplifier)
    chapitre = get_object_or_404(Chapitre, id=quiz_id)
    questions = chapitre.questions.all().order_by('id')
    
    if not questions.exists():
        messages.warning(request, "Aucune question disponible pour ce quiz. Veuillez d'abord générer le quiz.")
        return redirect('generer_quiz', chapitre_id=chapitre.id)
    
    if request.method == "POST":
        try:
            # Initialisation du service IA
            service = ServiceIA()
            
            score = 0
            total = questions.count()
            reponses_etudiant = {}
            explications_erreurs = {}
            
            # Vérification des réponses
            for question in questions:
                reponse_choisie = request.POST.get(f'question_{question.id}')
                
                if reponse_choisie:
                    reponses_etudiant[str(question.id)] = reponse_choisie
                    
                    if reponse_choisie == question.bonne_reponse:
                        score += 1
                    else:
                        # Génération d'un feedback IA pour les erreurs
                        try:
                            explication_ia = service.generer_feedback(
                                question=question,
                                reponse_utilisateur=reponse_choisie,
                                bonne_reponse=question.bonne_reponse
                            )
                            explications_erreurs[str(question.id)] = explication_ia
                        except Exception as e:
                            logger.warning(f"Erreur lors de la génération du feedback : {e}")
                            # Fallback : utilisation de l'explication par défaut
                            explications_erreurs[str(question.id)] = (
                                f"La bonne réponse était {question.bonne_reponse}. {question.explication}"
                            )
                else:
                    # Question non répondue
                    reponses_etudiant[str(question.id)] = None
            
            # Calcul du score en pourcentage
            score_pourcentage = int((score / total) * 100) if total > 0 else 0
            
            # Création du résultat en base
            resultat = QuizResult.objects.create(
                score=score_pourcentage,  # Score en pourcentage
                reponses_etudiant=reponses_etudiant,
                explications_erreurs=explications_erreurs if explications_erreurs else None,
                chapitre=chapitre,
                etudiant=request.user  # Accepte maintenant tous les utilisateurs (CustomUser)
            )
            
            # Mise à jour de la progression de l'étudiant (si c'est un StudentUser)
            try:
                etudiant = request.user.studentuser
                # Points gagnés : 10 points par bonne réponse
                points_gagnes = score * 10
                etudiant.progression_globale = F('progression_globale') + points_gagnes
                
                # Gestion des badges
                badges = etudiant.badges_obtenus or []
                
                if score == total and "Expert" not in badges:
                    badges.append("Expert")
                elif score >= total * 0.8 and "Excellent" not in badges:
                    badges.append("Excellent")
                elif score >= 1 and "Débutant" not in badges:
                    badges.append("Débutant")
                
                etudiant.badges_obtenus = badges
                etudiant.save()
                etudiant.refresh_from_db()
            except StudentUser.DoesNotExist:
                # L'utilisateur n'est pas un StudentUser, on ne met pas à jour la progression
                # mais le résultat a quand même été enregistré
                pass
            
            logger.info(f"Quiz soumis : score {score}/{total} ({score_pourcentage}%) pour {request.user.username}")
            
            # Redirection vers la page de résultats
            return redirect('quiz_result', result_id=resultat.id)
            
        except Exception as e:
            logger.error(f"Erreur lors de la soumission du quiz : {e}")
            messages.error(request, f"❌ Erreur lors de la soumission : {str(e)}")
    
    # GET : Affichage du quiz
    context = {
        'chapitre': chapitre,
        'questions': questions,
    }
    return render(request, 'formation/quiz_detail.html', context)


@login_required
def quiz_result_view(request, result_id):
    """
    Vue pour afficher les résultats détaillés d'un quiz avec feedbacks IA.
    
    Args:
        result_id: ID du résultat QuizResult à afficher
    """
    resultat = get_object_or_404(QuizResult, id=result_id)
    
    # Vérification que l'utilisateur a le droit de voir ce résultat
    if request.user != resultat.etudiant and request.user.role != 'TEACHER':
        messages.error(request, "Vous n'avez pas accès à ce résultat.")
        return redirect('home')
    
    # Récupération des questions du chapitre
    questions = resultat.chapitre.questions.all().order_by('id')
    
    # Construction d'un dictionnaire pour faciliter l'affichage
    questions_avec_reponses = []
    for question in questions:
        reponse_etudiant = resultat.reponses_etudiant.get(str(question.id))
        est_correcte = reponse_etudiant == question.bonne_reponse if reponse_etudiant else False
        feedback_ia = resultat.explications_erreurs.get(str(question.id)) if resultat.explications_erreurs else None
        
        questions_avec_reponses.append({
            'question': question,
            'reponse_etudiant': reponse_etudiant,
            'est_correcte': est_correcte,
            'feedback_ia': feedback_ia,
        })
    
    # Calcul des statistiques
    total = questions.count()
    bonnes_reponses = sum(1 for q in questions_avec_reponses if q['est_correcte'])
    score_pourcentage = resultat.score
    
    context = {
        'resultat': resultat,
        'questions_avec_reponses': questions_avec_reponses,
        'total': total,
        'bonnes_reponses': bonnes_reponses,
        'score_pourcentage': score_pourcentage,
        'chapitre': resultat.chapitre,
    }
    
    return render(request, 'formation/quiz_result.html', context)
