#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour remplacer tous les textes hardcódés par des appels à t(key, lang)
dans tous les fichiers JSX de l'application.
"""

import os
import re
from pathlib import Path

PROJECT_ROOT = Path("c:\\Users\\philippe\\source\\repos\\ad-cyberwatch.ai")

# Mappingdes remplacements pour chaque fichier
REPLACEMENTS_MAP = {
    "src/pages/Connectors.jsx": [
        ('"Connecteurs"', '{t(\'connectors.title\', lang)}'),
        ('"Gérez les connexions aux sources de données"', '{t(\'connectors.description\', lang)}'),
        ('"BloodHound Enterprise"', '{t(\'connectors.bloodhound\', lang)}'),
        ('"Configuration de l\'accès API pour la récupération des graphes d\'attaque."', '{t(\'connectors.bloodhoundDescription\', lang)}'),
        ('"URL de l\'API / Instance"', '{t(\'connectors.apiUrl\', lang)}'),
        ('"Token API"', '{t(\'connectors.apiToken\', lang)}'),
        ('"PingCastle (Analyse Statique)"', '{t(\'connectors.pingcastle\', lang)}'),
        ('"Emplacement des rapports d\'audit XML et des fichiers de règles."', '{t(\'connectors.pingcastleDescription\', lang)}'),
        ('"Dossier des Rapports XML"', '{t(\'connectors.xmlReportFolder\', lang)}'),
        ('"Fichier Catalog des Règles"', '{t(\'connectors.rulesCatalogFile\', lang)}'),
        ('"Fréquences de Synchronisation"', '{t(\'connectors.frequencies\', lang)}'),
        ('"Intervalles de polling et de rafraîchissement des données."', '{t(\'connectors.frequenciesDescription\', lang)}'),
        ('"Polling BloodHound (heures)"', '{t(\'connectors.bhPolling\', lang)}'),
        ('"Fréquence de récupération des données BloodHound"', '{t(\'connectors.bhPollingDescription\', lang)}'),
        ('"Polling PingCastle (jours)"', '{t(\'connectors.pcPolling\', lang)}'),
        ('"Fréquence de lecture des rapports PingCastle"', '{t(\'connectors.pcPollingDescription\', lang)}'),
        ('"Refresh Application (secondes)"', '{t(\'connectors.appRefresh\', lang)}'),
        ('"Intervalle de mise à jour de l\'interface"', '{t(\'connectors.appRefreshDescription\', lang)}'),
    ],
    "src/pages/Compliance.jsx": [
        ('"Radar de Conformité"', '{t(\'compliance.title\', lang)}'),
        ('"Analysez votre posture de conformité selon différents modèles"', '{t(\'compliance.description\', lang)}'),
        ('"Sélectionnez votre modèle de conformité"', '{t(\'compliance.selectFramework\', lang)}'),
        ('"Choisissez le framework qui correspond à vos besoins"', '{t(\'compliance.chooseFramework\', lang)}'),
        ('"NIST CSF 2.0"', '{t(\'compliance.nist\', lang)}'),
        ('"CIS Controls v8"', '{t(\'compliance.cis\', lang)}'),
        ('"ISO/IEC 27001"', '{t(\'compliance.iso\', lang)}'),
        ('"Modèle Personnalisé"', '{t(\'compliance.custom\', lang)}'),
        ('"Couverture"', '{t(\'compliance.coverage\', lang)}'),
        ('"Score Global"', '{t(\'compliance.overallScore\', lang)}'),
        ('"/ 100"', '/ 100'),
        ('"Détails par catégorie"', '{t(\'compliance.categoryDetails\', lang)}'),
        ('"Score Actuel"', '{t(\'compliance.currentScore\', lang)}'),
        ('"Objectif"', '{t(\'compliance.target\', lang)}'),
    ],
    "src/pages/Users.jsx": [
        ('"Gestion des Utilisateurs"', '{t(\'users.title\', lang)}'),
        ('"Utilisateurs locaux, rôles et authentification (SSO optionnel)."', '{t(\'users.description\', lang)}'),
        ('"Créer un utilisateur"', '{t(\'users.create\', lang)}'),
        ('"Rafraîchir"', '{t(\'users.refresh\', lang)}'),
        ('"Utilisateurs"', '{t(\'users.username\', lang)}'),
        ('"Aucun utilisateur trouvé. Lancez un rafraîchissement ou créez un compte."', '{t(\'users.noUsers\', lang)}'),
        ('"Nom"', '{t(\'users.name\', lang)}'),
        ('"Rôles"', '{t(\'users.roles\', lang)}'),
        ('"Auth"', '{t(\'users.auth\', lang)}'),
        ('"Local"', '{t(\'users.local\', lang)}'),
        ('"SSO"', '{t(\'users.sso\', lang)}'),
        ('"Suppr"', '{t(\'users.delete\', lang)}'),
        ('"Rôles de l\'Application"', '{t(\'users.applicationRoles\', lang)}'),
        ('"Définissez les rôles disponibles pour les utilisateurs"', '{t(\'users.defineRoles\', lang)}'),
        ('"Sauvegarder Rôles"', '{t(\'users.saveRoles\', lang)}'),
        ('"Nom du nouveau rôle (ex: security-admin)"', '{t(\'users.newRoleName\', lang)}'),
        ('"Ajouter"', '{t(\'users.addRole\', lang)}'),
        ('"Les rôles définis ici seront disponibles lors de la création ou modification des utilisateurs."', '{t(\'users.rolesInfo\', lang)}'),
    ],
    "src/pages/Automation.jsx": [
        ('"Automatisation"', '{t(\'automation.title\', lang)}'),
        ('"Connexion aux outils ITSM pour la création automatique de tickets."', '{t(\'automation.description\', lang)}'),
        ('"Systèmes de Billetterie"', '{t(\'automation.ticketingSystems\', lang)}'),
        ('"Connexions aux API de ces systèmes pour la création automatique de tickets."', '{t(\'automation.ticketingDescription\', lang)}'),
        ('"JIRA Software"', '{t(\'automation.jira\', lang)}'),
        ('"Instance URL"', '{t(\'automation.instanceUrl\', lang)}'),
        ('"Projet Key (ex: SEC, IT)"', '{t(\'automation.projectKey\', lang)}'),
        ('"Service User"', '{t(\'automation.serviceUser\', lang)}'),
        ('"API Token"', '{t(\'automation.apiToken\', lang)}'),
        ('"ServiceNow"', '{t(\'automation.servicenow\', lang)}'),
        ('"User ID"', '{t(\'automation.userId\', lang)}'),
        ('"Password / Token"', '{t(\'automation.password\', lang)}'),
        ('"Remédiations"', '{t(\'automation.remediation\', lang)}'),
        ('"Configuration des conditions d\'automatisation du workflow"', '{t(\'automation.remediationDescription\', lang)}'),
        ('"Configuration Workflow Remédiation"', '{t(\'automation.workflowConfig\', lang)}'),
        ('"Auto-Approbation si Risque <"', '{t(\'automation.autoApproval\', lang)}'),
        ('"Assigné par défaut"', '{t(\'automation.assignedBy\', lang)}'),
        ('"Approbation CAB requise pour Tier 0"', '{t(\'automation.cabApproval\', lang)}'),
        ('"Configuration SSO"', '{t(\'automation.sso\', lang)}'),
        ('"Paramètres d\'authentification unique (Single Sign-On)"', '{t(\'automation.ssoDescription\', lang)}'),
        ('"Sauvegarder SSO"', '{t(\'automation.saveSso\', lang)}'),
        ('"Provider SSO"', '{t(\'automation.ssoProvider\', lang)}'),
        ('"Azure AD / Entra ID"', '{t(\'automation.azureAd\', lang)}'),
        ('"Okta"', '{t(\'automation.okta\', lang)}'),
        ('"Google Workspace"', '{t(\'automation.google\', lang)}'),
        ('"SAML 2.0"', '{t(\'automation.saml\', lang)}'),
        ('"Client ID / Application ID"', '{t(\'automation.clientId\', lang)}'),
        ('"Tenant ID / Organization ID"', '{t(\'automation.tenantId\', lang)}'),
        ('"Redirect URI"', '{t(\'automation.redirectUri\', lang)}'),
        ('"Une fois configuré, utilisez le bouton "Tester SSO" pour vérifier la connexion."', '{t(\'automation.ssoInstruction\', lang)}'),
        ('"Tester SSO"', '{t(\'automation.testSso\', lang)}'),
    ],
    "src/pages/Integrations.jsx": [
        ('"Intégrations"', '{t(\'integrations.title\', lang)}'),
        ('"Configurez les intégrations externes"', '{t(\'integrations.description\', lang)}'),
        ('"Intégrations disponibles"', '{t(\'integrations.available\', lang)}'),
        ('"Les configurations des intégrations se trouvent dans la page "Systèmes de Billetterie & Remédiation"."', '{t(\'integrations.ticketingInfo\', lang)}'),
    ],
    "src/pages/Languages.jsx": [
        ('"Langues"', '{t(\'languages.title\', lang)}'),
        ('"Langue par défaut et gestion des langues disponibles."', '{t(\'languages.description\', lang)}'),
        ('"Langues disponibles:"', '{t(\'languages.available\', lang)}'),
        ('"Langue par défaut"', '{t(\'languages.default\', lang)}'),
        ('"Ajouter une langue"', '{t(\'languages.addLanguage\', lang)}'),
        ('"Ajouter"', '{t(\'languages.add\', lang)}'),
        ('"Gestion des Traductions"', '{t(\'languages.management\', lang)}'),
        ('"Éditez les traductions de l\'application"', '{t(\'languages.editTranslations\', lang)}'),
        ('"Sauvegarder"', '{t(\'languages.save\', lang)}'),
        ('"Annuler"', '{t(\'languages.cancel\', lang)}'),
        ('"Éditer"', '{t(\'languages.edit\', lang)}'),
        ('"Sélectionnez une langue"', '{t(\'languages.selectLanguage\', lang)}'),
        ('"Clé"', '{t(\'languages.key\', lang)}'),
        ('"Traduction"', '{t(\'languages.translation\', lang)}'),
        ('"Aucune traduction disponible pour cette langue"', '{t(\'languages.noTranslations\', lang)}'),
        ('"Seuls les administrateurs peuvent gérer les traductions. Connectez-vous avec un compte administrateur pour accéder à cette section."', '{t(\'languages.adminOnly\', lang)}'),
    ],
    "src/pages/ML.jsx": [
        ('"Centre d\'Apprentissage Machine"', '{t(\'ml.title\', lang)}'),
        ('"Calibration du modèle de risque basé sur les données historiques."', '{t(\'ml.description\', lang)}'),
        ('"Entraînement en cours..."', '{t(\'ml.training\', lang)}'),
        ('"Modèle Optimisé Actif"', '{t(\'ml.optimized\', lang)}'),
        ('"Lancer l\'Optimisation du Modèle"', '{t(\'ml.launchOptimization\', lang)}'),
        ('"Pondération des Caractéristiques"', '{t(\'ml.featureWeighting\', lang)}'),
        ('"Précision du Modèle"', '{t(\'ml.modelAccuracy\', lang)}'),
    ],
    "src/pages/Bloodhound.jsx": [
        ('"Vue BloodHound"', '{t(\'bloodhound.title\', lang)}'),
        ('"Contenu BloodHound à intégrer (à venir)."', '{t(\'bloodhound.content\', lang)}'),
    ],
    "src/pages/Pingcastle.jsx": [
        ('"Vue PingCastle"', '{t(\'pingcastle.title\', lang)}'),
        ('"Contenu PingCastle à intégrer (à venir)."', '{t(\'pingcastle.content\', lang)}'),
    ],
    "src/pages/Rosetta.jsx": [
        ('"Pierre de Rosette"', '{t(\'rosetta.title\', lang)}'),
        ('"Contenu à intégrer (à venir)."', '{t(\'rosetta.content\', lang)}'),
    ],
}

def process_file(filepath, replacements):
    """Traite un fichier avec les remplacements spécifiés."""
    try:
        content = filepath.read_text('utf-8')
        
        # Vérifier si déjà mis à jour
        if "import { t } from '../i18n'" in content:
            print(f"✓ {filepath.relative_to(PROJECT_ROOT)} - déjà mis à jour")
            return True
        
        # Ajouter l'import
        if "import" in content and "from '../i18n'" not in content:
            lines = content.split('\n')
            import_idx = 0
            for i, line in enumerate(lines):
                if 'import' in line and 'from' in line:
                    import_idx = i
            lines.insert(import_idx + 1, "import { t } from '../i18n';")
            content = '\n'.join(lines)
        
        # Appliquer les remplacements
        for old, new in replacements:
            content = content.replace(old, new)
        
        # Écrire le fichier
        filepath.write_text(content, 'utf-8')
        print(f"✓ {filepath.relative_to(PROJECT_ROOT)} - {len(replacements)} remplacements appliqués")
        return True
    except Exception as e:
        print(f"✗ {filepath.relative_to(PROJECT_ROOT)} - Erreur: {e}")
        return False

def main():
    print("=" * 60)
    print("AUTOMATISATION DES TRADUCTIONS")
    print("=" * 60)
    
    success_count = 0
    total_count = len(REPLACEMENTS_MAP)
    
    for relative_path, replacements in REPLACEMENTS_MAP.items():
        filepath = PROJECT_ROOT / relative_path
        if filepath.exists():
            if process_file(filepath, replacements):
                success_count += 1
        else:
            print(f"✗ {relative_path} - Fichier non trouvé")
    
    print("=" * 60)
    print(f"Résumé: {success_count}/{total_count} fichiers traités")
    print("=" * 60)

if __name__ == "__main__":
    main()
