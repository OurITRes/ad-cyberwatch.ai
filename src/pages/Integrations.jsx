import React from 'react';
import { Card } from '../components';
import { Zap } from 'lucide-react';
import { t } from '../i18n';

export default function IntegrationsPage({ ctx }) {
  return (
    <div className="animate-in fade-in duration-300 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center">
            <Zap className="mr-2 text-blue-600" size={28} />
            Intégrations
          </h2>
          <p className="text-slate-500 mt-1">Configurez les intégrations externes</p>
        </div>
      </div>

      <Card className="border-t-4 border-t-blue-500">
        <div className="p-4">
          <h3 className="text-lg font-bold text-slate-800">Intégrations disponibles</h3>
          <p className="text-sm text-slate-500 mt-2">Les configurations des intégrations se trouvent dans la page "Systèmes de Billetterie & Remédiation".</p>
        </div>
      </Card>
    </div>
  );
}
