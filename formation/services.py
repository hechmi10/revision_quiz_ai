"""
Service IA pour la génération de contenu via OpenAI API ou Groq (API gratuite)
Gestion robuste des erreurs, retry automatique, logging et validation JSON
"""

import json
import re
import logging
import time
from typing import Dict, List, Optional, Any
from django.conf import settings
from openai import OpenAI
from openai import APITimeoutError, APIError, APIConnectionError

# Configuration du logging
logger = logging.getLogger(__name__)


class ServiceIA:
    """
    Classe de service pour interagir avec l'API OpenAI ou Groq.
    Gère la génération de quiz et de feedbacks avec gestion d'erreur robuste.
    
    Par défaut, utilise Groq (gratuit) pour les tests. 
    Pour utiliser OpenAI, définir USE_OPENAI=True dans settings.
    """
    
    def __init__(self, api_key: Optional[str] = None, timeout: int = 30, max_retries: int = 3, provider: Optional[str] = None):
        """
        Initialise le client OpenAI/Groq avec gestion d'erreur.
        
        Args:
            api_key: Clé API (si None, cherche dans settings)
            timeout: Timeout en secondes pour les appels API (défaut: 30)
            max_retries: Nombre maximum de tentatives en cas d'échec (défaut: 3)
            provider: "groq" ou "openai" (si None, utilise la config dans settings)
        """
        try:
            # Détermination du provider à utiliser
            if provider:
                self.provider = provider.lower()
            else:
                # Par défaut, utiliser Groq (gratuit) pour les tests
                self.provider = getattr(settings, 'AI_PROVIDER', 'groq').lower()
            
            # Récupération de la clé API selon le provider
            if api_key:
                self.api_key = api_key
            elif self.provider == 'groq':
                self.api_key = getattr(settings, 'GROQ_API_KEY', None)
                if not self.api_key:
                    # Pour tester, vous pouvez obtenir une clé gratuite sur https://console.groq.com/
                    # En attendant, on laisse None et on affichera un message d'erreur clair
                    logger.warning("GROQ_API_KEY non définie. Obtenez une clé gratuite sur https://console.groq.com/")
            else:
                self.api_key = getattr(settings, 'OPENAI_API_KEY', None)
            
            if not self.api_key:
                if self.provider == 'groq':
                    raise ValueError(
                        "Clé API Groq manquante. "
                        "Obtenez une clé gratuite sur https://console.groq.com/ "
                        "et définissez-la dans settings.GROQ_API_KEY ou comme variable d'environnement."
                    )
                else:
                    raise ValueError("Clé API OpenAI invalide ou manquante")
            
            # Initialisation du client selon le provider
            if self.provider == 'groq':
                # Groq utilise la même interface qu'OpenAI, mais avec une URL de base différente
                base_url = "https://api.groq.com/openai/v1"
                self.client = OpenAI(api_key=self.api_key, base_url=base_url, timeout=timeout)
                # Modèle actuel : llama-3.3-70b-versatile (le modèle llama-3.1-70b-versatile a été décommissionné)
                # Alternative : llama-3.1-8b-instant (plus rapide, moins puissant)
                self.model_name = getattr(settings, 'GROQ_MODEL', 'llama-3.3-70b-versatile')
                logger.info(f"ServiceIA initialisé avec Groq (API gratuite) - Modèle: {self.model_name}")
            else:
                self.client = OpenAI(api_key=self.api_key, timeout=timeout)
                self.model_name = "gpt-3.5-turbo"
                logger.info("ServiceIA initialisé avec OpenAI")
            
            self.timeout = timeout
            self.max_retries = max_retries
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de ServiceIA : {e}")
            raise Exception(f"Impossible d'initialiser le service IA : {str(e)}")
    
    def nettoyer_json(self, texte: str) -> str:
        """
        Nettoie le texte JSON retourné par l'API OpenAI.
        Supprime les backticks, les espaces superflus, et extrait le JSON valide.
        
        Args:
            texte: Texte brut contenant potentiellement du JSON
            
        Returns:
            Chaîne JSON nettoyée
        """
        try:
            # Suppression des backticks markdown (```json ... ```)
            texte = re.sub(r'```json\s*', '', texte)
            texte = re.sub(r'```\s*', '', texte)
            
            # Suppression des backticks simples
            texte = texte.strip('`')
            
            # Recherche du JSON entre accolades
            match = re.search(r'\{.*\}', texte, re.DOTALL)
            if match:
                texte = match.group(0)
            
            # Recherche du JSON entre crochets (liste)
            match = re.search(r'\[.*\]', texte, re.DOTALL)
            if match:
                texte = match.group(0)
            
            # Nettoyage des espaces et retours à la ligne superflus
            texte = texte.strip()
            
            return texte
            
        except Exception as e:
            logger.warning(f"Erreur lors du nettoyage JSON : {e}")
            return texte
    
    def _appel_api_avec_retry(self, fonction_appel, *args, **kwargs) -> Any:
        """
        Exécute un appel API avec retry automatique en cas d'échec.
        
        Args:
            fonction_appel: Fonction à exécuter (lambda ou fonction)
            *args: Arguments positionnels pour la fonction
            **kwargs: Arguments nommés pour la fonction
            
        Returns:
            Résultat de l'appel API
            
        Raises:
            Exception: Si toutes les tentatives échouent
        """
        dernier_erreur = None
        
        for tentative in range(1, self.max_retries + 1):
            try:
                logger.info(f"Tentative {tentative}/{self.max_retries} d'appel API")
                resultat = fonction_appel(*args, **kwargs)
                logger.info("Appel API réussi")
                return resultat
                
            except APITimeoutError as e:
                dernier_erreur = e
                logger.warning(f"Timeout API (tentative {tentative}/{self.max_retries}): {e}")
                if tentative < self.max_retries:
                    time.sleep(2 ** tentative)  # Backoff exponentiel
                    
            except APIConnectionError as e:
                dernier_erreur = e
                logger.warning(f"Erreur de connexion API (tentative {tentative}/{self.max_retries}): {e}")
                if tentative < self.max_retries:
                    time.sleep(2 ** tentative)
                    
            except APIError as e:
                dernier_erreur = e
                logger.error(f"Erreur API (tentative {tentative}/{self.max_retries}): {e}")
                # Pour les erreurs d'API (quota, clé invalide, authentification, modèle décommissionné), on ne retry pas
                erreur_str = str(e).lower()
                erreur_code = getattr(e, 'status_code', None)
                
                # Détection des erreurs non-réessayables
                est_erreur_quota = (
                    erreur_code == 429 or
                    "429" in str(e) or 
                    "quota" in erreur_str or 
                    "insufficient_quota" in erreur_str
                )
                est_erreur_auth = (
                    erreur_code == 401 or
                    "401" in str(e) or
                    ("invalid" in erreur_str and "api key" in erreur_str) or
                    "authentication" in erreur_str or
                    "unauthorized" in erreur_str
                )
                est_erreur_modele = (
                    erreur_code == 400 or
                    "400" in str(e) or
                    "model_decommissioned" in erreur_str or
                    "decommissioned" in erreur_str or
                    "model" in erreur_str and ("deprecated" in erreur_str or "no longer" in erreur_str)
                )
                
                if est_erreur_quota or est_erreur_auth or est_erreur_modele:
                    # Ne pas réessayer pour ces erreurs
                    if est_erreur_quota:
                        provider_name = "OpenAI" if self.provider != 'groq' else "Groq"
                        raise Exception(
                            f"Le quota de l'API {provider_name} a été dépassé. "
                            "Veuillez vérifier votre plan et vos informations de facturation. "
                            "Vous pouvez également essayer de générer le quiz plus tard."
                        ) from e
                    elif est_erreur_modele:
                        provider_name = "OpenAI" if self.provider != 'groq' else "Groq"
                        raise Exception(
                            f"Le modèle utilisé n'est plus disponible sur l'API {provider_name}. "
                            "Le modèle a été décommissionné. Veuillez contacter le support technique "
                            "ou consulter la documentation pour connaître les modèles disponibles."
                        ) from e
                    else:
                        provider_name = "OpenAI" if self.provider != 'groq' else "Groq"
                        raise Exception(
                            f"Erreur d'authentification avec l'API {provider_name}. "
                            "Veuillez vérifier votre clé API dans les paramètres."
                        ) from e
                    
                if tentative < self.max_retries:
                    time.sleep(2 ** tentative)
                    
            except Exception as e:
                dernier_erreur = e
                logger.error(f"Erreur inattendue (tentative {tentative}/{self.max_retries}): {e}")
                if tentative < self.max_retries:
                    time.sleep(2 ** tentative)
        
        # Toutes les tentatives ont échoué
        logger.error(f"Échec après {self.max_retries} tentatives")
        raise Exception(f"Impossible de contacter l'API OpenAI après {self.max_retries} tentatives : {str(dernier_erreur)}")
    
    def generer_quiz(self, chapitre, nombre_questions: int = 5, difficulte: str = "Moyen") -> List[Dict[str, Any]]:
        """
        Génère un quiz complet à partir du contenu d'un chapitre.
        
        Args:
            chapitre: Instance du modèle Chapitre
            nombre_questions: Nombre de questions à générer (5-20)
            difficulte: Niveau de difficulté ("Facile", "Moyen", "Difficile")
            
        Returns:
            Liste de dictionnaires contenant les questions au format standardisé
            
        Format JSON attendu:
        {
            "questions": [
                {
                    "question": "Texte de la question",
                    "choix": ["Choix 1", "Choix 2", "Choix 3", "Choix 4"],
                    "bonne_reponse": 0,
                    "explication": "Explication de la bonne réponse"
                }
            ]
        }
        """
        try:
            # Validation des paramètres
            nombre_questions = max(5, min(20, nombre_questions))  # Entre 5 et 20
            
            texte = chapitre.contenu_texte
            if not texte or len(texte.strip()) < 50:
                raise ValueError("Le contenu du chapitre est trop court pour générer un quiz")
            
            # Construction du prompt système
            prompt_systeme = """Tu es un expert pédagogique spécialisé dans la création de QCM éducatifs.
Tu dois générer des questions de quiz à choix multiples (QCM) à partir d'un texte de cours.

FORMAT DE SORTIE OBLIGATOIRE (JSON strict) :
{
    "questions": [
        {
            "question": "Intitulé de la question claire et précise ?",
            "choix": ["Premier choix", "Deuxième choix", "Troisième choix", "Quatrième choix"],
            "bonne_reponse": 0,
            "explication": "Explication détaillée de pourquoi cette réponse est correcte et pédagogique."
        }
    ]
}

RÈGLES IMPORTANTES :
- "choix" est un tableau de 4 chaînes de caractères
- "bonne_reponse" est l'INDEX (0, 1, 2 ou 3) du choix correct dans le tableau "choix"
- Les questions doivent être variées (définition, application, analyse)
- Les explications doivent être pédagogiques et aider à comprendre
- Réponds UNIQUEMENT avec le JSON, sans texte avant ou après"""
            
            # Construction du prompt utilisateur
            niveau_difficulte = {
                "Facile": "des questions simples de compréhension basique",
                "Moyen": "des questions de niveau intermédiaire nécessitant une bonne compréhension",
                "Difficile": "des questions complexes nécessitant une analyse approfondie"
            }.get(difficulte, "des questions de niveau intermédiaire")
            
            prompt_user = f"""Génère exactement {nombre_questions} questions QCM {niveau_difficulte} basées sur ce texte de cours :

{texte[:4000]}  # Limite à 4000 caractères pour éviter les tokens excessifs

Assure-toi que :
- Chaque question teste une compétence différente
- Les choix de réponses sont plausibles (évite les réponses évidentes)
- La bonne réponse est bien répartie (pas toujours la première)
- Les explications sont claires et pédagogiques"""
            
            logger.info(f"Génération de quiz pour chapitre '{chapitre.titre}' ({nombre_questions} questions, {difficulte})")
            
            # Appel API avec retry
            def appel_api():
                return self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": prompt_systeme},
                        {"role": "user", "content": prompt_user}
                    ],
                    temperature=0.7,
                    max_tokens=2000,
                    timeout=self.timeout
                )
            
            response = self._appel_api_avec_retry(appel_api)
            
            # Récupération et nettoyage de la réponse
            content = response.choices[0].message.content
            logger.debug(f"Réponse brute reçue (premiers 200 caractères) : {content[:200]}...")
            
            # Nettoyage du JSON
            content_nettoye = self.nettoyer_json(content)
            
            # Parsing et validation du JSON
            try:
                questions_data = json.loads(content_nettoye)
            except json.JSONDecodeError as e:
                logger.error(f"Erreur de parsing JSON : {e}")
                logger.error(f"Contenu reçu : {content_nettoye[:500]}")
                raise ValueError(f"Le format JSON retourné par l'IA est invalide : {str(e)}")
            
            # Normalisation de la structure
            if isinstance(questions_data, dict) and "questions" in questions_data:
                questions_list = questions_data["questions"]
            elif isinstance(questions_data, list):
                questions_list = questions_data
            else:
                raise ValueError("Format de réponse inattendu : structure JSON invalide")
            
            # Validation de chaque question
            questions_validees = []
            for idx, q in enumerate(questions_list):
                try:
                    # Vérification des champs requis
                    if not all(key in q for key in ["question", "choix", "bonne_reponse", "explication"]):
                        logger.warning(f"Question {idx + 1} incomplète, ignorée")
                        continue
                    
                    # Vérification du format des choix
                    if not isinstance(q["choix"], list) or len(q["choix"]) != 4:
                        logger.warning(f"Question {idx + 1} : format de choix invalide, ignorée")
                        continue
                    
                    # Vérification de l'index de bonne réponse
                    bonne_reponse_idx = q["bonne_reponse"]
                    if not isinstance(bonne_reponse_idx, int) or bonne_reponse_idx < 0 or bonne_reponse_idx > 3:
                        logger.warning(f"Question {idx + 1} : index de bonne réponse invalide, ignorée")
                        continue
                    
                    questions_validees.append(q)
                    
                except Exception as e:
                    logger.warning(f"Erreur lors de la validation de la question {idx + 1} : {e}")
                    continue
            
            if not questions_validees:
                raise ValueError("Aucune question valide n'a pu être générée")
            
            logger.info(f"Quiz généré avec succès : {len(questions_validees)} questions valides")
            return questions_validees
            
        except ValueError as e:
            logger.error(f"Erreur de validation : {e}")
            raise e
        except Exception as e:
            logger.error(f"Erreur lors de la génération du quiz : {e}")
            raise Exception(f"Impossible de générer le quiz : {str(e)}")
    
    def generer_feedback(self, question, reponse_utilisateur: str, bonne_reponse: str) -> str:
        """
        Génère un feedback personnalisé pour une réponse d'étudiant.
        
        Args:
            question: Instance du modèle QuizQuestion
            reponse_utilisateur: Réponse choisie par l'étudiant (A, B, C ou D)
            bonne_reponse: Bonne réponse attendue (A, B, C ou D)
            
        Returns:
            Texte de feedback personnalisé en français
        """
        try:
            # Récupération du texte de la réponse choisie
            choix_map = {
                'A': question.choix_A,
                'B': question.choix_B,
                'C': question.choix_C,
                'D': question.choix_D
            }
            
            reponse_texte = choix_map.get(reponse_utilisateur, "Réponse inconnue")
            bonne_reponse_texte = choix_map.get(bonne_reponse, "Réponse inconnue")
            
            # Construction du prompt
            prompt_systeme = """Tu es un tuteur pédagogique bienveillant et encourageant.
Ton rôle est d'expliquer les erreurs des étudiants de manière constructive et pédagogique.
Utilise un ton positif et motivant, même quand l'étudiant s'est trompé."""
            
            prompt_user = f"""L'étudiant a répondu "{reponse_utilisateur}) {reponse_texte}" à la question suivante :

"{question.question_texte}"

La bonne réponse était "{bonne_reponse}) {bonne_reponse_texte}".

Génère un feedback pédagogique en 2-3 phrases qui :
1. Explique pourquoi la réponse choisie est incorrecte (si applicable)
2. Explique pourquoi la bonne réponse est correcte
3. Encourage l'étudiant à continuer à apprendre

Réponds UNIQUEMENT avec le feedback, sans introduction ni conclusion."""
            
            logger.info(f"Génération de feedback pour question {question.id}")
            
            # Appel API avec retry
            def appel_api():
                return self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": prompt_systeme},
                        {"role": "user", "content": prompt_user}
                    ],
                    temperature=0.8,
                    max_tokens=200,
                    timeout=self.timeout
                )
            
            response = self._appel_api_avec_retry(appel_api)
            
            feedback = response.choices[0].message.content.strip()
            logger.info("Feedback généré avec succès")
            
            return feedback
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération du feedback : {e}")
            # Fallback : retourne une explication basique
            return f"La bonne réponse était {bonne_reponse}. {question.explication}"
