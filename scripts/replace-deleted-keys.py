#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour remplacer les clés supprimées du fichier i18n par leur texte original
"""

import re
import os
from pathlib import Path

def extract_translations_from_file():
    """Extrait toutes les clés définies dans le fichier i18n"""
    with open('src/i18n/index.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire toutes les clés définies
    keys_en = set()
    keys_fr = set()
    
    # Pattern pour trouver les clés: 'key.name': 'value'
    pattern = r"'([^']+)':\s*'[^']*'"
    
    # Chercher dans la section EN
    en_section = re.search(r"en:\s*\{(.*?)^\s*\},", content, re.DOTALL | re.MULTILINE)
    if en_section:
        for match in re.finditer(pattern, en_section.group(1)):
            keys_en.add(match.group(1))
    
    # Chercher dans la section FR
    fr_section = re.search(r"fr:\s*\{(.*?)^\s*\}", content, re.DOTALL | re.MULTILINE)
    if fr_section:
        for match in re.finditer(pattern, fr_section.group(1)):
            keys_fr.add(match.group(1))
    
    all_keys = keys_en | keys_fr
    print(f"✓ {len(all_keys)} clés trouvées dans i18n")
    return all_keys

def find_t_usage_in_files():
    """Trouve toutes les utilisations de t() dans les fichiers source"""
    usage = {}
    
    # Parcourir tous les fichiers .jsx et .js
    for root, dirs, files in os.walk('src'):
        # Ignorer node_modules et autres dossiers
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'dist', '.git']]
        
        for file in files:
            if file.endswith(('.jsx', '.js')):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        content = f.read()
                        # Pattern pour trouver t('key.name', lang)
                        pattern = r"t\('([^']+)',\s*\w+\)"
                        for match in re.finditer(pattern, content):
                            key = match.group(1)
                            if key not in usage:
                                usage[key] = []
                            usage[key].append(filepath)
                    except Exception as e:
                        print(f"Erreur lecture {filepath}: {e}")
    
    return usage

def main():
    print("="*60)
    print("RECHERCHE DES CLÉS SUPPRIMÉES")
    print("="*60)
    
    # Extraire les clés définies
    defined_keys = extract_translations_from_file()
    
    # Trouver les utilisations
    print("\n✓ Recherche des utilisations de t() dans le code...")
    usage = find_t_usage_in_files()
    print(f"✓ {len(usage)} clés différentes utilisées dans le code")
    
    # Trouver les clés utilisées mais non définies
    deleted_keys = set(usage.keys()) - defined_keys
    
    if not deleted_keys:
        print("\n✅ Aucune clé supprimée trouvée ! Toutes les clés utilisées sont définies.")
        return
    
    print(f"\n⚠️  {len(deleted_keys)} clé(s) supprimée(s) trouvée(s) :")
    print("="*60)
    
    for key in sorted(deleted_keys):
        print(f"\n📌 Clé: {key}")
        print(f"   Utilisée dans:")
        for file in usage[key]:
            print(f"   - {file}")
    
    print("\n" + "="*60)
    print("ATTENTION : Ces clés doivent être remplacées par leur texte original")
    print("dans les fichiers ci-dessus, ou réajoutées dans src/i18n/index.js")
    print("="*60)

if __name__ == '__main__':
    main()
