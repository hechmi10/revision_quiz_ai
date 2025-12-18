# Instructions pour appliquer la migration

Le modèle `QuizResult` a été modifié pour accepter tous les utilisateurs (`CustomUser`) au lieu de seulement `StudentUser`.

## Étapes à suivre :

1. **Activez votre environnement virtuel** :
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Créez la migration** :
   ```bash
   python manage.py makemigrations
   ```

3. **Appliquez la migration** :
   ```bash
   python manage.py migrate
   ```

## Note importante

Si vous avez déjà des données dans la base de données, la migration devrait fonctionner car tous les `StudentUser` sont aussi des `CustomUser` (héritage).

Si vous rencontrez des erreurs, contactez-moi pour de l'aide.

