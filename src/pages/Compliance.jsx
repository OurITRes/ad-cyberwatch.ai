import React from 'react';
import { Card } from '../components';

export default function CompliancePage({ ctx }) {
  return (
    <div className="space-y-6">
      <p className="px-4 text-xs font-bold text-slate-500 uppercase tracking-wider mt-2 mb-2">Conformité</p>
      <Card>
        <div className="p-4">
          <h3 className="text-lg font-bold text-slate-800">Radar de Conformité</h3>
          <p className="text-slate-500 text-sm mt-2">Sélectionnez votre modèle, y compris un modèle personnalisé (à venir).</p>
        </div>
      </Card>
    </div>
  );
}
