import React from 'react';
import { Card } from '../components';
import { Settings as SettingsIcon, RefreshCw, Save, Users, Ticket, Folder, Database, Server, Lock, FileText, Network, Cable, Clock } from 'lucide-react';
import ResponsiveGuard from '../components/ResponsiveGuard';
import { t } from '../i18n';

export default function SettingsView({ ctx }) {
  const { config, setConfig, handleSaveConfig, isSaving, supportedLanguages, addSupportedLanguage, loadUsers, setActiveView, authService } = ctx;
  return (
    <div className="animate-in fade-in duration-300 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center">
            <Cable className="mr-2 text-indigo-600" size={28} />Connecteurs
          </h2>
          <p className="text-slate-500 mt-1">Gérez les connexions aux sources de données</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="space-y-1 mr-4"></div>
          <button onClick={handleSaveConfig} className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium transition-colors shadow-sm">
            {isSaving ? <RefreshCw className="animate-spin" size={18} /> : <Save size={18} />}
            <span>{t('settings.save', config.language)}</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-8">
        <Card className="border-t-4 border-t-purple-500">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Network className="text-purple-600" size={24} />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-800">BloodHound Enterprise</h3>
              <p className="text-sm text-slate-500">Configuration de l'accès API pour la récupération des graphes d'attaque.</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-700">URL de l'API / Instance</label>
              <div className="relative">
                <Server className="absolute left-3 top-2.5 text-slate-400" size={16} />
                <input type="text" value={config.bhUrl} onChange={(e) => setConfig({...config, bhUrl: e.target.value})} className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-sm" />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-700">Token API</label>
              <div className="relative">
                <Lock className="absolute left-3 top-2.5 text-slate-400" size={16} />
                <input type="password" value={config.bhToken} onChange={(e) => setConfig({...config, bhToken: e.target.value})} className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-sm font-mono" />
              </div>
            </div>
          </div>
        </Card>

        <Card className="border-t-4 border-t-blue-500">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-blue-100 rounded-lg">
              <FileText className="text-blue-600" size={24} />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-800">PingCastle (Analyse Statique)</h3>
              <p className="text-sm text-slate-500">Emplacement des rapports d'audit XML et des fichiers de règles.</p>
            </div>
          </div>
          <div className="space-y-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-700">Dossier des Rapports XML</label>
              <div className="relative">
                <Folder className="absolute left-3 top-2.5 text-slate-400" size={16} />
                <input type="text" value={config.pcReportPath} onChange={(e) => setConfig({...config, pcReportPath: e.target.value})} className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-sm font-mono" />
              </div>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-700">Fichier Catalog des Règles</label>
              <div className="relative">
                <Database className="absolute left-3 top-2.5 text-slate-400" size={16} />
                <input type="text" value={config.pcCatalogPath} onChange={(e) => setConfig({...config, pcCatalogPath: e.target.value})} className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-sm font-mono" />
              </div>
            </div>
          </div>
        </Card>

        <Card className="border-t-4 border-t-emerald-500">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-emerald-100 rounded-lg">
              <Clock className="text-emerald-600" size={24} />
            </div>
            <div>
              <h3 className="text-lg font-bold text-slate-800">Fréquences de Synchronisation</h3>
              <p className="text-sm text-slate-500">Intervalles de polling et de rafraîchissement des données.</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-700">Polling BloodHound (heures)</label>
              <div className="relative">
                <RefreshCw className="absolute left-3 top-2.5 text-slate-400" size={16} />
                <input 
                  type="number" 
                  min="1" 
                  value={config.bhPollingInterval || 24} 
                  onChange={(e) => setConfig({...config, bhPollingInterval: parseInt(e.target.value) || 24})} 
                  className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-sm" 
                />
              </div>
              <p className="text-xs text-slate-500">Fréquence de récupération des données BloodHound</p>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-700">Polling PingCastle (jours)</label>
              <div className="relative">
                <RefreshCw className="absolute left-3 top-2.5 text-slate-400" size={16} />
                <input 
                  type="number" 
                  min="1" 
                  value={config.pcPollingInterval || 7} 
                  onChange={(e) => setConfig({...config, pcPollingInterval: parseInt(e.target.value) || 7})} 
                  className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-sm" 
                />
              </div>
              <p className="text-xs text-slate-500">Fréquence de lecture des rapports PingCastle</p>
            </div>
            <div className="space-y-1">
              <label className="text-sm font-medium text-slate-700">Refresh Application (secondes)</label>
              <div className="relative">
                <RefreshCw className="absolute left-3 top-2.5 text-slate-400" size={16} />
                <input 
                  type="number" 
                  min="5" 
                  value={config.appRefreshInterval || 30} 
                  onChange={(e) => setConfig({...config, appRefreshInterval: parseInt(e.target.value) || 30})} 
                  className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg text-sm" 
                />
              </div>
              <p className="text-xs text-slate-500">Intervalle de mise à jour de l'interface</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
