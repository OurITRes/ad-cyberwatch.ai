#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour traduire les termes français en anglais dans la section EN du fichier i18n
"""

# Mapping des traductions FR -> EN
translations_map = {
    # Dashboard
    "Score de Sécurité AD": "AD Security Score",
    "depuis le mois dernier": "since last month",
    "Chemins Critiques (Tier 0)": "Critical Paths (Tier 0)",
    "Identifiés par BloodHound": "Identified by BloodHound",
    "Contrôles NIST 2.0 Actifs": "NIST 2.0 Active Controls",
    "Plan d'Action": "Remediation Plan",
    "Plan Validé - En cours": "Plan Validated - In Progress",
    "En attente de validation": "Awaiting Validation",
    "Évolution de la Posture & Risques": "Evolution of Posture & Risks",
    "6 derniers mois": "6 last months",
    "Cette année": "This Year",
    "Score de Conformité": "Compliance Score",
    "Risques Détectés": "Detected Risks",
    "Top Failles Identifiées": "Top Identified Flaws",
    "Voir tout": "View All",
    "Faille": "Flaw",
    "Priorité IA": "AI Priority",
    "Analyser": "Analyze",
    "Couverture NIST CSF 2.0": "NIST CSF 2.0 Coverage",
    "Voir l'analyse prédictive": "View Predictive Analysis",
    
    # Connectors
    "Connecteurs": "Connectors",
    "Gérez les connexions aux sources de données": "Manage connections to data sources",
    "Configuration de l'accès API pour la récupération des graphes d'attaque.": "API access configuration for attack graph retrieval.",
    "URL de l'API / Instance": "API URL / Instance",
    "PingCastle (Analyse Statique)": "PingCastle (Static Analysis)",
    "Emplacement des rapports d'audit XML et des fichiers de règles.": "Location of XML audit reports and rules files.",
    "Dossier des Rapports XML": "XML Report Folder",
    "Fichier Catalog des Règles": "Rules Catalog File",
    "Fréquences de Synchronisation": "Synchronization Frequencies",
    "Intervalles de polling et de rafraîchissement des données.": "Polling intervals and data refresh rates.",
    "Polling BloodHound (heures)": "BloodHound Polling (hours)",
    "Fréquence de récupération des données BloodHound": "Frequency of BloodHound data retrieval",
    "Polling PingCastle (jours)": "PingCastle Polling (days)",
    "Fréquence de lecture des rapports PingCastle": "Frequency of PingCastle report reading",
    "Refresh Application (secondes)": "App Refresh (seconds)",
    "Intervalle de mise à jour de l'interface": "UI update interval",
    
    # Automation
    "Automatisation": "Automation",
    "Connexion aux outils ITSM pour la création automatique de tickets.": "ITSM system connections for automatic ticket creation.",
    "Systèmes de Billetterie": "Ticketing Systems",
    "Connexions aux API de ces systèmes pour la création automatique de tickets.": "API connections to these systems for automatic ticket creation.",
    "Clé Projet (ex: SEC, IT)": "Project Key (ex: SEC, IT)",
    "Mot de Passe / Token": "Password / Token",
    "Remédiations": "Remediations",
    "Configuration des conditions d'automatisation du workflow": "Automatic workflow automation conditions configuration",
    "Configuration Workflow Remédiation": "Remediation Workflow Configuration",
    "Auto-Approbation si Risque <": "Auto-Approval if Risk <",
    "Assigné par défaut": "Assigned by default",
    "Approbation CAB requise pour Tier 0": "CAB Approval required for Tier 0",
    "Configuration SSO": "SSO Configuration",
    "Paramètres d'authentification unique (Single Sign-On)": "Single Sign-On (SSO) authentication parameters",
    "Sauvegarder SSO": "Save SSO",
    "Provider SSO": "SSO Provider",
    "URI de redirection": "Redirect URI",
    "Une fois configuré, utilisez le bouton \"Tester SSO\" pour vérifier la connexion.": "Once configured, use the \"Test SSO\" button to verify the connection.",
    "Tester SSO": "Test SSO",
    "Bas": "Low",
    "Haut": "High",
    
    # Compliance
    "Radar de Conformité": "Compliance Radar",
    "Analysez votre posture de conformité selon différents modèles": "Analyze your compliance posture according to different models",
    "Sélectionnez votre modèle de conformité": "Select your compliance model",
    "Choisissez le framework qui correspond à vos besoins": "Choose the framework that matches your needs",
    "Modèle Personnalisé": "Custom Model",
    "Basé sur votre contexte métier": "Based on your business context",
    "Couverture": "Coverage",
    "Score Global": "Overall Score",
    "Détails par catégorie": "Details by category",
    "Score Actuel": "Current Score",
    "Objectif": "Target",
    
    # Details
    "Retour au Command Center": "Back to Command Center",
    "Sélectionner Vulnérabilité:": "Select Vulnerability:",
    "Générer un Ticket Jira": "Generate a Jira Ticket",
    "Plan non validé": "Plan not validated",
    "Validez le plan de remédiation d'abord": "Validate the remediation plan first",
    "Visualisation du Chemin d'Attaque (BloodHound Data)": "Attack Path Visualization (BloodHound Data)",
    "Analyse de Conformité (Mapping Complet)": "Compliance Analysis (Complete Mapping)",
    "Modèle Custom (Interne)": "Custom Model (Internal)",
    "Gain de Remédiation": "Remediation Gain",
    "Impact estimé sur le score global": "Estimated impact on overall score",
    "De réduction de surface d'attaque": "Surface area reduction",
    "Criticité:": "Criticality:",
    "Coût:": "Cost:",
    "Actions Techniques Recommandées": "Recommended Technical Actions",
    "1 - Rotation du mot de passe": "1 - Password Rotation",
    "Changer immédiatement le mot de passe du compte de service impacté (min 25 chars).": "Immediately change the password of the impacted service account (min 25 chars).",
    
    # Integrations
    "Intégrations": "Integrations",
    "Configurez les intégrations externes": "Configure external integrations",
    "Intégrations disponibles": "Available Integrations",
    "Les configurations des intégrations se trouvent dans la page \"Systèmes de Billetterie & Remédiation\".": "Ticketing system configurations are in the \"Automation\" page.",
    
    # Languages
    "Langues": "Languages",
    "Langue par défaut et gestion des langues disponibles.": "Default language and management of available languages.",
    "Langues disponibles:": "Available Languages",
    "Langue par défaut": "Default Language",
    "Ajouter une langue": "Add a Language",
    "Ajouter": "Add",
    "Gestion des Traductions": "Translation Management",
    "Éditez les traductions de l'application": "Edit application translations",
    "Sauvegarder": "Save",
    "Annuler": "Cancel",
    "Éditer": "Edit",
    "Sélectionnez une langue": "Select a language",
    "Clé": "Key",
    "Traduction": "Translation",
    "Aucune traduction disponible pour cette langue": "No translations available for this language",
    "Seuls les administrateurs peuvent gérer les traductions. Connectez-vous avec un compte administrateur pour accéder à cette section.": "Only administrators can manage translations. Please log in with an administrator account to access this section.",
    "Rôles actuels:": "Current Roles:",
    "OUI": "YES",
    "NON": "NO",
    
    # ML
    "Centre d'Apprentissage Machine": "Machine Learning Center",
    "Calibration du modèle de risque basé sur les données historiques.": "Risk model calibration based on historical data.",
    "Entraînement en cours...": "Training in progress...",
    "Modèle Optimisé Actif": "Optimized Model Active",
    "Lancer l'Optimisation du Modèle": "Launch Model Optimization",
    "Pondération des Caractéristiques": "Feature Weighting",
    "Précision du Modèle": "Model Accuracy",
    
    # Bloodhound
    "Vue BloodHound": "BloodHound View",
    "Contenu BloodHound à intégrer (à venir).": "BloodHound content to integrate (coming soon).",
    
    # Pingcastle
    "Vue PingCastle": "PingCastle View",
    "Contenu PingCastle à intégrer (à venir).": "PingCastle content to integrate (coming soon).",
    
    # Profile
    "Mon Profil": "My Profile",
    "Prénom": "First Name",
    "Nom": "Last Name",
    "Nom complet (auto-généré)": "Full Name (auto-generated)",
    "Rôle métier (optionnel)": "Business Role (optional)",
    "-- Aucun --": "-- None --",
    "Roles techniques": "Technical Roles",
    "Aperçu de la photo": "Photo Preview",
    "Sauvegarder position": "Save Position",
    "Centrer": "Center",
    "Supprimer l'image": "Remove Image",
    "Changer le mot de passe": "Change Password",
    "Nouveau mot de passe (optionnel)": "New Password (optional)",
    "Laisser vide pour garder le mot de passe actuel": "Leave blank to keep current password",
    "Confirmer le mot de passe": "Confirm Password",
    "Confirmer le nouveau mot de passe": "Confirm new password",
    "Enregistrement...": "Saving...",
    "Enregistrer les modifications": "Save Changes",
    
    # Remediation
    "Plan Global de Remédiation": "Global Remediation Plan",
    "Validez la stratégie globale avant d'autoriser la création de tickets unitaires.": "Validate the overall strategy before authorizing unit ticket creation.",
    "Liste": "List",
    "Matrice": "Matrix",
    "Plan Validé": "Plan Validated",
    "Valider le Plan": "Validate Plan",
    "Matrice Complexité vs Criticité (Quick Wins)": "Complexity vs Criticality Matrix (Quick Wins)",
    "Effort / Complexité": "Effort / Complexity",
    "Impact / Criticité": "Impact / Criticality",
    "Actions de remédiation": "Remediation Actions",
    "Zone en haut à gauche : Priorité absolue (Fort Impact, Faible Effort)": "Top left area: Absolute Priority (High Impact, Low Effort)",
    "Détail des Actions & Synchronisation JIRA": "Detail of Actions & JIRA Synchronization",
    "Action Requise": "Required Action",
    "Priorité": "Priority",
    "Dépendances": "Dependencies",
    "Responsable (JIRA Suggest)": "Responsible (JIRA Suggest)",
    "Statut (JIRA Sync)": "Status (JIRA Sync)",
    "Requiert #": "Requires #",
    "Suggéré par JIRA...": "Suggested by JIRA...",
    
    # Rosetta
    "Pierre de Rosette": "Rosetta Stone",
    "Contenu à intégrer (à venir).": "Content to integrate (coming soon).",
    
    # Users
    "Gestion des Utilisateurs": "User Management",
    "Liste des Utilisateurs": "Users List",
    "Utilisateurs locaux, rôles et authentification (SSO optionnel).": "Local users, roles and authentication (optional SSO).",
    "Créer un utilisateur": "Create User",
    "Rafraîchir": "Refresh",
    "Aucun utilisateur trouvé. Lancez un rafraîchissement ou créez un compte.": "No users found. Launch a refresh or create an account.",
    "Rôles": "Roles",
    "Suppr": "Delete",
    "Rôles de l'Application": "Application Roles",
    "Définissez les rôles disponibles pour les utilisateurs": "Define available roles for users",
    "Sauvegarder Rôles": "Save Roles",
    "Nom du nouveau rôle (ex: security-admin)": "New role name (ex: security-admin)",
    "Les rôles définis ici seront disponibles lors de la création ou modification des utilisateurs.": "Roles defined here will be available when creating or modifying users.",
    
    # Forms
    "Entrez un email/UPN valide et un mot de passe": "Enter a valid email/UPN",
    "Position sauvegardée": "Position saved",
    "Erreur sauvegarde position:": "Position save error:",
    "Photo supprimée": "Photo removed",
    "Erreur suppression:": "Photo removal error:",
    "Profil mis à jour": "Profile updated",
    "Erreur sauvegarde profil:": "Profile save error:",
    
    # Login
    "Plateforme de Défense AD": "AD Defense Platform",
    "Connexion locale": "Local Login",
    "Se connecter": "Sign In",
    "Créer un utilisateur": "Create a User",
    "Serveur d'authentification indisponible — l'application utilisera la configuration locale (fallback).": "Authentication server unavailable — the application will use local configuration (fallback).",
    "Utilisez votre fournisseur d'identité d'entreprise (Azure AD, Okta, Keycloak...). Ceci est un stub local.": "Use your enterprise identity provider (Azure AD, Okta, Keycloak...). This is a local stub.",
    "Se connecter via SSO": "Sign In via SSO",
    "Si le serveur SSO n'est pas disponible, créez un compte local via la page de création.": "If the SSO server is not available, create a local account via the creation page.",
    
    # Register
    "Créer un utilisateur local": "Create local user",
    "Email ou UPN": "Email or UPN",
}

def fix_english_translations():
    """Lit le fichier i18n et remplace les termes français par leur traduction anglaise"""
    import re
    
    file_path = 'src/i18n/index.js'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les remplacements
    replacements_made = 0
    
    # Pour chaque traduction
    for french, english in translations_map.items():
        # Échapper les caractères spéciaux pour le regex
        french_escaped = re.escape(french)
        english_escaped = english.replace("\\", "\\\\").replace("'", "\\'")
        
        # Chercher dans la section EN uniquement (avant le "fr: {")
        pattern = f"(en:\\s*{{[^}}]*?)'([^']*?)':\\s*'{french_escaped}'"
        replacement = f"\\1'\\2': '{english_escaped}'"
        
        new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
        
        if count > 0:
            content = new_content
            replacements_made += count
            print(f"✓ Remplacé '{french}' par '{english}' ({count} occurrence(s))")
    
    # Sauvegarder le fichier
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n{'='*60}")
    print(f"Total: {replacements_made} remplacement(s) effectué(s)")
    print(f"{'='*60}")

if __name__ == '__main__':
    fix_english_translations()
