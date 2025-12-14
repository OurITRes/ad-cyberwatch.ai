#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour remplacer les textes hardcódés dans Details, Profile, Remediation et composants.
"""

import os
from pathlib import Path

PROJECT_ROOT = Path("c:\\Users\\philippe\\source\\repos\\ad-cyberwatch.ai")

REPLACEMENTS_MAP = {
    "src/pages/Details.jsx": [
        ('"Retour au Command Center"', '{t(\'details.backToCommandCenter\', lang)}'),
        ('"Sélectionner Vulnérabilité:"', '{t(\'details.selectVulnerability\', lang)}'),
        ('"Critical Risk"', '{t(\'details.criticalRisk\', lang)}'),
        ('"ID:"', '{t(\'details.id\', lang)}'),
        ('"Générer un Ticket Jira"', '{t(\'details.generateJiraTicket\', lang)}'),
        ('"Plan non validé"', '{t(\'details.planNotValidated\', lang)}'),
        ('"Validez le plan de remédiation d\'abord"', '{t(\'details.validateFirst\', lang)}'),
        ('"Visualisation du Chemin d\'Attaque (BloodHound Data)"', '{t(\'details.attackPathVisualization\', lang)}'),
        ('"Analyse de Conformité (Mapping Complet)"', '{t(\'details.complianceAnalysis\', lang)}'),
        ('"NIST CSF"', '{t(\'details.nistCsf\', lang)}'),
        ('"Version 2.0 (2024)"', '{t(\'details.version20\', lang)}'),
        ('"Version 1.1"', '{t(\'details.version11\', lang)}'),
        ('"CIS Controls"', '{t(\'details.cisControls\', lang)}'),
        ('"Version v8"', '{t(\'details.versionV8\', lang)}'),
        ('"Version v7"', '{t(\'details.versionV7\', lang)}'),
        ('"Modèle Custom (Interne)"', '{t(\'details.customModel\', lang)}'),
        ('"Gain de Remédiation"', '{t(\'details.remediationGain\', lang)}'),
        ('"Impact estimé sur le score global"', '{t(\'details.estimatedImpact\', lang)}'),
        ('"De réduction de surface d\'attaque"', '{t(\'details.reductionAttackSurface\', lang)}'),
        ('"Criticité:"', '{t(\'details.criticality\', lang)}'),
        ('"Coût:"', '{t(\'details.cost\', lang)}'),
        ('"Actions Techniques Recommandées"', '{t(\'details.recommendedActions\', lang)}'),
        ('"1 - Rotation du mot de passe"', '{t(\'details.passwordRotation\', lang)}'),
        ('"Changer immédiatement le mot de passe du compte de service impacté (min 25 chars)."', '{t(\'details.passwordRotationDescription\', lang)}'),
        ('"2 - AES Encryption"', '{t(\'details.aesEncryption\', lang)}'),
        ('"Activer le support AES pour Kerberos afin de rendre le cracking plus difficile."', '{t(\'details.aesEncryptionDescription\', lang)}'),
    ],
    "src/pages/Profile.jsx": [
        ('"Mon Profil"', '{t(\'profile.title\', lang)}'),
        ('"Email / ID"', '{t(\'profile.email\', lang)}'),
        ('"Prénom"', '{t(\'profile.firstName\', lang)}'),
        ('"Nom"', '{t(\'profile.lastName\', lang)}'),
        ('"Nom complet (auto-généré)"', '{t(\'profile.fullName\', lang)}'),
        ('"Rôle métier (optionnel)"', '{t(\'profile.businessRole\', lang)}'),
        ('"-- Aucun --"', '{t(\'profile.none\', lang)}'),
        ('"Roles techniques"', '{t(\'profile.technicalRoles\', lang)}'),
        ('"Avatar"', '{t(\'profile.avatar\', lang)}'),
        ('"Aperçu de la photo"', '{t(\'profile.preview\', lang)}'),
        ('"Sauvegarder position"', '{t(\'profile.savePosition\', lang)}'),
        ('"Centrer"', '{t(\'profile.center\', lang)}'),
        ('"Supprimer l\'image"', '{t(\'profile.removeImage\', lang)}'),
        ('"Changer le mot de passe"', '{t(\'profile.changePassword\', lang)}'),
        ('"Nouveau mot de passe (optionnel)"', '{t(\'profile.newPassword\', lang)}'),
        ('"Laisser vide pour garder le mot de passe actuel"', '{t(\'profile.keepCurrent\', lang)}'),
        ('"Confirmer le mot de passe"', '{t(\'profile.confirmPassword\', lang)}'),
        ('"Confirmer le nouveau mot de passe"', '{t(\'profile.confirmNew\', lang)}'),
        ('"Enregistrement..."', '{t(\'profile.saving\', lang)}'),
        ('"Enregistrer les modifications"', '{t(\'profile.saveChanges\', lang)}'),
        ('"Annuler"', '{t(\'profile.cancel\', lang)}'),
    ],
    "src/pages/Remediation.jsx": [
        ('"Plan Global de Remédiation"', '{t(\'remediation.title\', lang)}'),
        ('"Validez la stratégie globale avant d\'autoriser la création de tickets unitaires."', '{t(\'remediation.description\', lang)}'),
        ('"Liste"', '{t(\'remediation.list\', lang)}'),
        ('"Matrice"', '{t(\'remediation.matrix\', lang)}'),
        ('"Plan Validé"', '{t(\'remediation.planValidated\', lang)}'),
        ('"Valider le Plan"', '{t(\'remediation.validatePlan\', lang)}'),
        ('"Matrice Complexité vs Criticité (Quick Wins)"', '{t(\'remediation.complexityMatrix\', lang)}'),
        ('"Effort / Complexité"', '{t(\'remediation.effort\', lang)}'),
        ('"Impact / Criticité"', '{t(\'remediation.impact\', lang)}'),
        ('"Actions de remédiation"', '{t(\'remediation.actions\', lang)}'),
        ('"Zone en haut à gauche : Priorité absolue (Fort Impact, Faible Effort)"', '{t(\'remediation.quickWinsZone\', lang)}'),
        ('"Détail des Actions & Synchronisation JIRA"', '{t(\'remediation.detailActions\', lang)}'),
        ('"ID"', '{t(\'remediation.id\', lang)}'),
        ('"Action Requise"', '{t(\'remediation.requiredAction\', lang)}'),
        ('"Priorité"', '{t(\'remediation.priority\', lang)}'),
        ('"Dépendances"', '{t(\'remediation.dependencies\', lang)}'),
        ('"Responsable (JIRA Suggest)"', '{t(\'remediation.responsible\', lang)}'),
        ('"Statut (JIRA Sync)"', '{t(\'remediation.status\', lang)}'),
        ('"Requiert #"', '{t(\'remediation.requires\', lang)}'),
        ('"Suggéré par JIRA..."', '{t(\'remediation.suggestedByJira\', lang)}'),
        ('"To Do"', '{t(\'remediation.todo\', lang)}'),
        ('"In Progress"', '{t(\'remediation.inProgress\', lang)}'),
        ('"Done"', '{t(\'remediation.done\', lang)}'),
        ('"Validation"', '{t(\'remediation.validation\', lang)}'),
    ],
    "src/components/Login.jsx": [
        ('"— Plateforme de Défense AD"', '{t(\'login.title\', lang)}'),
        ('"Connexion locale"', '{t(\'login.local\', lang)}'),
        ('"Email ou UPN (ex: user@domain.com)"', '{t(\'login.email\', lang)}'),
        ('"Password"', '{t(\'login.password\', lang)}'),
        ('"Se connecter"', '{t(\'login.signIn\', lang)}'),
        ('"Vous n\'avez pas de compte local ?"', '{t(\'login.noAccount\', lang)}'),
        ('"Créer un utilisateur"', '{t(\'login.createUser\', lang)}'),
        ('"Serveur d\'authentification indisponible — l\'application utilisera la configuration locale (fallback)."', '{t(\'login.authUnavailable\', lang)}'),
        ('"Single Sign-On (SSO)"', '{t(\'login.sso\', lang)}'),
        ('"Utilisez votre fournisseur d\'identité d\'entreprise (Azure AD, Okta, Keycloak...). Ceci est un stub local."', '{t(\'login.ssoDescription\', lang)}'),
        ('"Se connecter via SSO"', '{t(\'login.ssoSignIn\', lang)}'),
        ('"Si le serveur SSO n\'est pas disponible, créez un compte local via la page de création."', '{t(\'login.ssoNote\', lang)}'),
    ],
    "src/components/Register.jsx": [
        ('"Create local user"', '{t(\'register.title\', lang)}'),
        ('"Email or UPN"', '{t(\'register.email\', lang)}'),
        ('"First name"', '{t(\'register.firstName\', lang)}'),
        ('"Last name"', '{t(\'register.lastName\', lang)}'),
        ('"Password"', '{t(\'register.password\', lang)}'),
        ('"Business role (optional)"', '{t(\'register.businessRole\', lang)}'),
        ('"-- none --"', '{t(\'register.none\', lang)}'),
        ('"Create"', '{t(\'register.create\', lang)}'),
        ('"Cancel"', '{t(\'register.cancel\', lang)}'),
    ],
}

def process_file(filepath, replacements):
    """Traite un fichier avec les remplacements spécifiés."""
    try:
        content = filepath.read_text('utf-8')
        
        # Vérifier si déjà mis à jour
        if "import { t } from" in content or "const { t }" in content:
            print(f"✓ {filepath.relative_to(PROJECT_ROOT)} - déjà mis à jour")
            return True
        
        # Ajouter l'import si nécessaire
        if "import" in content and "from '../i18n'" not in content and "from '../../i18n'" not in content:
            lines = content.split('\n')
            import_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('import'):
                    import_idx = i + 1
            # Déterminer le chemin relatif correct
            if "components" in str(filepath):
                import_line = "import { t } from '../i18n';"
            else:
                import_line = "import { t } from '../i18n';"
            lines.insert(import_idx, import_line)
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
    print("AUTOMATISATION DES TRADUCTIONS (Suite)")
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
