import React from 'react';
import { Card } from '../components';
import { t } from '../i18n';

export default function PingcastlePage({ ctx }) {
  return (
    <div className="space-y-6">
      <Card>
        <div className="p-4">
          <h3 className="text-lg font-bold text-slate-800">Vue PingCastle</h3>
          <p className="text-slate-500 text-sm mt-2">Contenu PingCastle à intégrer (à venir).</p>
        </div>
      </Card>
    </div>
  );
}
