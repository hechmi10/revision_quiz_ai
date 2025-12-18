# Configuration de Groq (API gratuite pour les tests)

Votre application a été configurée pour utiliser **Groq**, une API gratuite avec des modèles open source (comme Llama 3.1) qui est parfaite pour tester votre application.

## 🚀 Avantages de Groq

- ✅ **Gratuit** avec quota généreux
- ✅ **Rapide** - API très performante
- ✅ **Open source** - Utilise des modèles comme Llama 3.1
- ✅ **Compatible OpenAI** - Même interface, pas besoin de changer le code

## 📝 Étapes pour obtenir votre clé API Groq

1. **Allez sur le site Groq Console** : https://console.groq.com/

2. **Créez un compte** (c'est gratuit et rapide)

3. **Générez une clé API** :
   - Connectez-vous à votre compte
   - Allez dans "API Keys" dans le menu
   - Cliquez sur "Create API Key"
   - Copiez votre clé (elle commence par `gsk_...`)

4. **Configurez votre clé dans Django** :

   Le fichier `.env` a déjà été créé à la racine du projet. Il vous suffit de :
   
   **Éditez le fichier `.env`** et ajoutez votre clé API après le signe `=` :
   ```
   GROQ_API_KEY=gsk_votre_cle_ici
   ```
   
   Le fichier devrait ressembler à ça :
   ```
   GROQ_API_KEY=gsk_votre_cle_ici
   AI_PROVIDER=groq
   ```
   
   **Note** : Le fichier `.env` est automatiquement chargé par Django (déjà configuré dans `settings.py`).
   
   **Alternative : Variable d'environnement système**
   
   Si vous préférez, vous pouvez définir la variable directement :
   - **Windows PowerShell** :
     ```powershell
     $env:GROQ_API_KEY="gsk_votre_cle_ici"
     ```
   - **Linux/Mac** :
     ```bash
     export GROQ_API_KEY="gsk_votre_cle_ici"
     ```

## 🔄 Changer de provider

Si vous voulez revenir à OpenAI plus tard, changez simplement :

```python
# Dans settings.py ou variable d'environnement
AI_PROVIDER = 'openai'
OPENAI_API_KEY = 'sk-votre_cle_openai'
```

## ✅ Vérification

Une fois la clé configurée, redémarrez votre serveur Django :

```bash
python manage.py runserver
```

L'application utilisera maintenant Groq au lieu d'OpenAI !

## 📚 Documentation

- Site Groq : https://groq.com/
- Console Groq : https://console.groq.com/
- Documentation API : https://console.groq.com/docs

## 💡 Modèles disponibles

Par défaut, le code utilise `llama-3.3-70b-versatile` qui est excellent pour la génération de quiz.

### Modèles Groq recommandés :

- **llama-3.3-70b-versatile** (par défaut) - Modèle le plus puissant, idéal pour la génération de quiz
- **llama-3.1-8b-instant** - Plus rapide, moins puissant, bon pour des tests rapides
- **mixtral-8x7b-32768** - Bon compromis vitesse/puissance

### Changer le modèle :

Vous pouvez modifier le modèle dans `config/settings.py` :
```python
GROQ_MODEL = 'llama-3.1-8b-instant'  # Pour un modèle plus rapide
```

Ou dans le fichier `.env` :
```
GROQ_MODEL=llama-3.1-8b-instant
```

