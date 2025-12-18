import os
from pathlib import Path

# On définit le dossier de base (là où est ce script)
BASE_DIR = Path(__file__).resolve().parent

print("-" * 50)
print(f"1. JE SUIS ICI : {BASE_DIR}")
print("-" * 50)

# Chemin théorique du fichier
chemin_attendu = BASE_DIR / 'formation' / 'templates' / 'formation' / 'quiz_detail.html'

print(f"2. JE CHERCHE CE FICHIER EXACTEMENT :")
print(f"   {chemin_attendu}")

print("-" * 50)
print("3. VERIFICATION :")

if chemin_attendu.exists():
    print("✅ LE FICHIER EXISTE ! Django devrait le voir.")
else:
    print("❌ LE FICHIER N'EXISTE PAS à cet endroit.")
    
    # On va lister ce qu'on trouve pour t'aider
    dossier_templates = BASE_DIR / 'formation' / 'templates'
    print(f"\n   Contenu du dossier '{dossier_templates}' :")
    
    if not dossier_templates.exists():
        print("   ⚠️ Le dossier 'templates' lui-même n'existe pas !")
    else:
        for fichier in dossier_templates.glob('**/*'):
            print(f"   - {fichier.relative_to(dossier_templates)}")

print("-" * 50)