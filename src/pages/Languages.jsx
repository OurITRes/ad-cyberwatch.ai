import React from 'react';
import { Card } from '../components';
import { Globe, PlusCircle } from 'lucide-react';

export default function LanguagesPage({ ctx }) {
  const { config, setConfig, supportedLanguages, addSupportedLanguage } = ctx;

  return (
    <div className="animate-in fade-in duration-300 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center">
            <Globe className="mr-2 text-emerald-600" size={28} />
            Langues
          </h2>
          <p className="text-slate-500 mt-1 text-sm">Langue par défaut et gestion des langues disponibles.</p>
        </div>
      </div>

      <Card className="border-t-4 border-t-emerald-500">
        <div className="flex items-center space-x-3 mb-6">
          <div className="p-2 bg-emerald-100 rounded-lg">
            <Globe className="text-emerald-600" size={24} />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-800">Langues</h3>
            <p className="text-sm text-slate-500">Langue par défaut et gestion des langues</p>
          </div>
        </div>
        <div className="space-y-6">
          <div className="p-4 bg-slate-50 rounded border border-slate-200">
            <h4 className="font-semibold text-slate-800 mb-3 flex items-center"><span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>Langues</h4>
            <div className="text-xs text-slate-400 flex">Langues disponibles: {supportedLanguages.join(', ').toUpperCase()}</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-500 uppercase">Langue par défaut</label>
                <select value={config.defaultLanguage} onChange={(e) => setConfig({ ...config, defaultLanguage: e.target.value })} className="w-full p-2 border border-slate-300 rounded text-sm">
                  {supportedLanguages.map((lang) => (<option key={lang} value={lang}>{lang.toUpperCase()}</option>))}
                </select>
              </div>
              <div className="space-y-1">
                <label className="text-xs font-semibold text-slate-500 uppercase">Ajouter une langue</label>
                <div className="flex items-center space-x-2">
                  <input id="newLang" type="text" placeholder="fr" className="w-full p-2 border border-slate-300 rounded text-sm w-24" />
                  <button onClick={() => { const el = document.getElementById('newLang'); if (!el) return; const val = el.value.trim().toLowerCase(); if (!val) return; addSupportedLanguage(val); el.value = ''; }} className="px-3 py-1 bg-slate-800 text-white rounded text-sm inline-flex items-center space-x-1">
                    <PlusCircle size={14} />
                    <span>Ajouter</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
