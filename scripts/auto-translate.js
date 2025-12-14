/**
 * Script d'automatisation de traduction des fichiers JSX
 * Remplace les textes hardcodes par des appels à t(key, lang)
 */

const fs = require('fs');
const path = require('path');

// Mapping des fichiers et leurs traductions
const FILES_TRANSLATIONS = {
  'src/pages/Dashboard.jsx': {
    langVar: 'lang',
    replacements: [
      // Score de Sécurité AD
      { old: '"Score de Sécurité AD"', new: '{t(\'dashboard.adSecurityScore\', lang)}' },
      { old: '"/100"', new: '{t(\'dashboard.outOf\', lang)}' },
      { old: '"depuis le mois dernier"', new: '{t(\'dashboard.since\', lang)}' },
      { old: '"+12%"', new: '{t(\'dashboard.increase\', lang)}' },
      
      // Chemins Critiques
      { old: '"Chemins Critiques (Tier 0)"', new: '{t(\'dashboard.criticalPaths\', lang)}' },
      { old: '"Identifiés par BloodHound"', new: '{t(\'dashboard.identifiedByBloodhound\', lang)}' },
      
      // NIST Controls
      { old: '"Contrôles NIST 2.0 Actifs"', new: '{t(\'dashboard.nistControls\', lang)}' },
      { old: '"64%"', new: '64{t(\'dashboard.percent\', lang)}' },
      
      // Remediation Plan
      { old: '"Plan d\'Action"', new: '{t(\'dashboard.remediationPlan\', lang)}' },
      { old: '"Plan Validé - En cours"', new: '{t(\'dashboard.planValidated\', lang)}' },
      { old: '"En attente de validation"', new: '{t(\'dashboard.awaitingValidation\', lang)}' },
      
      // Evolution Chart
      { old: '"Évolution de la Posture & Risques"', new: '{t(\'dashboard.evolution\', lang)}' },
      { old: '"6 derniers mois"', new: '{t(\'dashboard.lastMonths\', lang)}' },
      { old: '"Cette année"', new: '{t(\'dashboard.thisYear\', lang)}' },
      
      // Chart names
      { old: 'name="Score de Conformité"', new: 'name={t(\'dashboard.compliance\', lang)}' },
      { old: 'name="Risques Détectés"', new: 'name={t(\'dashboard.detectedRisks\', lang)}' },
      
      // Top Flaws Table
      { old: '"Top Failles Identifiées"', new: '{t(\'dashboard.topFlaws\', lang)}' },
      { old: '"Voir tout"', new: '{t(\'dashboard.viewAll\', lang)}' },
      
      // Table Headers
      { old: '{"Source"}', new: '{t(\'dashboard.source\', lang)}' },
      { old: '{"Faille"}', new: '{t(\'dashboard.flaw\', lang)}' },
      { old: '{"Asset"}', new: '{t(\'dashboard.asset\', lang)}' },
      { old: '{"Priorité IA"}', new: '{t(\'dashboard.priorityAI\', lang)}' },
      { old: '{"Action"}', new: '{t(\'dashboard.action\', lang)}' },
      { old: '"Analyser"', new: '{t(\'dashboard.analyze\', lang)}' },
      
      // NIST Coverage
      { old: '"Couverture NIST CSF 2.0"', new: '{t(\'dashboard.nistCoverage\', lang)}' },
      
      // AI Insight
      { old: '"IA Insight"', new: '{t(\'dashboard.aiInsight\', lang)}' },
      { old: '"Voir l\'analyse prédictive"', new: '{t(\'dashboard.viewAnalysis\', lang)}' }
    ]
  },
  'src/pages/Connectors.jsx': {
    langVar: 'lang',
    replacements: [
      { old: '"Connecteurs"', new: '{t(\'connectors.title\', lang)}' },
      { old: '"Gérez les connexions aux sources de données"', new: '{t(\'connectors.description\', lang)}' },
      { old: '"BloodHound Enterprise"', new: '{t(\'connectors.bloodhound\', lang)}' },
      { old: '"Configuration de l\'accès API pour la récupération des graphes d\'attaque."', new: '{t(\'connectors.bloodhoundDescription\', lang)}' },
      { old: '"URL de l\'API / Instance"', new: '{t(\'connectors.apiUrl\', lang)}' },
      { old: '"Token API"', new: '{t(\'connectors.apiToken\', lang)}' },
      { old: '"PingCastle (Analyse Statique)"', new: '{t(\'connectors.pingcastle\', lang)}' },
      { old: '"Emplacement des rapports d\'audit XML et des fichiers de règles."', new: '{t(\'connectors.pingcastleDescription\', lang)}' },
      { old: '"Dossier des Rapports XML"', new: '{t(\'connectors.xmlReportFolder\', lang)}' },
      { old: '"Fichier Catalog des Règles"', new: '{t(\'connectors.rulesCatalogFile\', lang)}' },
      { old: '"Fréquences de Synchronisation"', new: '{t(\'connectors.frequencies\', lang)}' },
      { old: '"Intervalles de polling et de rafraîchissement des données."', new: '{t(\'connectors.frequenciesDescription\', lang)}' },
      { old: '"Polling BloodHound (heures)"', new: '{t(\'connectors.bhPolling\', lang)}' },
      { old: '"Fréquence de récupération des données BloodHound"', new: '{t(\'connectors.bhPollingDescription\', lang)}' },
      { old: '"Polling PingCastle (jours)"', new: '{t(\'connectors.pcPolling\', lang)}' },
      { old: '"Fréquence de lecture des rapports PingCastle"', new: '{t(\'connectors.pcPollingDescription\', lang)}' },
      { old: '"Refresh Application (secondes)"', new: '{t(\'connectors.appRefresh\', lang)}' },
      { old: '"Intervalle de mise à jour de l\'interface"', new: '{t(\'connectors.appRefreshDescription\', lang)}' }
    ]
  }
};

// Fonction pour mettre à jour un fichier
function updateFile(filePath, translations) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Vérifier si déjà mise à jour
    if (content.includes('import { t } from \'../i18n\'')) {
      console.log(`✓ ${filePath} déjà mis à jour`);
      return;
    }
    
    // Ajouter l'import si manquant
    if (!content.includes('import { t }')) {
      const importMatch = content.match(/import\s+.*\s+from\s+['"][^'"]+['"]/);
      if (importMatch) {
        content = content.replace(
          importMatch[0],
          importMatch[0] + `;\nimport { t } from '../i18n'`
        );
      }
    }
    
    // Appliquer les replacements
    translations.replacements.forEach(({ old, new: newVal }) => {
      content = content.split(old).join(newVal);
    });
    
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`✓ ${filePath} mis à jour`);
  } catch (err) {
    console.error(`✗ Erreur avec ${filePath}:`, err.message);
  }
}

// Exécuter
console.log('Démarrage de l\'automatisation des traductions...\n');
Object.entries(FILES_TRANSLATIONS).forEach(([filePath, config]) => {
  const fullPath = path.join(__dirname, '..', filePath);
  updateFile(fullPath, config);
});
console.log('\n✓ Traductions automatisées terminées!');
