import React, { useEffect } from 'react';
import { Card } from '../components';
import { Users, RefreshCw, Plus, Shield, ShieldCheck, Trash2 } from 'lucide-react';

export default function UsersPage({ ctx }) {
  const { users = [], loadUsers, setActiveView, authService } = ctx;

  useEffect(() => {
    loadUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center">
            <Users className="mr-2 text-indigo-600" size={28} />
            Gestion des Utilisateurs
          </h2>
          <p className="text-slate-500 mt-1 text-sm">Utilisateurs locaux, rôles et authentification (SSO optionnel).</p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setActiveView('register')}
            className="inline-flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-medium shadow-sm"
          >
            <Plus size={16} />
            <span>Créer un utilisateur</span>
          </button>
          <button
            onClick={() => loadUsers()}
            className="inline-flex items-center space-x-2 bg-slate-800 hover:bg-slate-900 text-white px-3 py-2 rounded-lg text-sm font-medium shadow-sm"
          >
            <RefreshCw size={16} />
            <span>Rafraîchir</span>
          </button>
          <button
            onClick={async () => {
              const r = await authService.startSSO();
              alert(JSON.stringify(r));
            }}
            className="inline-flex items-center space-x-2 bg-slate-100 hover:bg-slate-200 text-slate-800 px-3 py-2 rounded-lg text-sm font-medium border border-slate-200"
          >
            <Shield size={16} />
            <span>Tester SSO</span>
          </button>
        </div>
      </div>

      <Card className="border-t-4 border-t-blue-500">
        <div className="p-4">
          <h3 className="text-lg font-bold text-slate-800 mb-3">Utilisateurs</h3>
          {users.length === 0 ? (
            <div className="text-sm text-slate-500 flex items-center space-x-2">
              <ShieldCheck size={16} className="text-green-500" />
              <span>Aucun utilisateur trouvé. Lancez un rafraîchissement ou créez un compte.</span>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="text-xs text-slate-500 uppercase">
                  <tr>
                    <th className="p-2 text-left">ID</th>
                    <th className="p-2 text-left">Nom</th>
                    <th className="p-2 text-left">Rôles</th>
                    <th className="p-2 text-left">Auth</th>
                    <th className="p-2 text-left"></th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((u) => (
                    <tr key={u.id} className="border-t">
                      <td className="p-2 align-middle">{u.id}</td>
                      <td className="p-2 align-middle">{u.displayName || u.firstName || u.id}</td>
                      <td className="p-2 align-middle">{(u.roles || []).join(', ')}</td>
                      <td className="p-2 align-middle">
                        <select
                          value={u.authMode || 'local'}
                          onChange={async (e) => {
                            const m = e.target.value;
                            await authService.updateUser(u.id, { ...u, authMode: m });
                            loadUsers();
                          }}
                          className="p-1 border rounded text-sm bg-white"
                        >
                          <option value="local">Local</option>
                          <option value="sso">SSO</option>
                        </select>
                      </td>
                      <td className="p-2 align-middle text-right">
                        <button
                          className="inline-flex items-center space-x-1 text-red-600 hover:text-red-700"
                          onClick={async () => {
                            await authService.deleteUser(u.id);
                            loadUsers();
                          }}
                        >
                          <Trash2 size={14} />
                          <span>Suppr</span>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
