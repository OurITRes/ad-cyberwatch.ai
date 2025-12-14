import React, { useState } from 'react';
import { Card } from '../components';
import { Radar, BarChart3, Settings } from 'lucide-react';
import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar as RechartsRadar, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

export default function CompliancePage({ ctx }) {
  const { complianceScore } = ctx;
  const [selectedFramework, setSelectedFramework] = useState('nist');

  // Données pour les différents modèles de conformité
  const complianceFrameworks = {
    nist: {
      name: 'NIST CSF 2.0',
      description: 'National Institute of Standards and Technology Cybersecurity Framework',
      color: '#3b82f6',
      data: [
        { category: 'Govern', score: 72, max: 100 },
        { category: 'Identify', score: 85, max: 100 },
        { category: 'Protect', score: 45, max: 100 },
        { category: 'Detect', score: 60, max: 100 },
        { category: 'Respond', score: 70, max: 100 },
        { category: 'Recover', score: 90, max: 100 },
      ]
    },
    cis: {
      name: 'CIS Controls v8',
      description: 'Center for Internet Security Controls',
      color: '#10b981',
      data: [
        { category: 'Inventory', score: 75, max: 100 },
        { category: 'Access', score: 55, max: 100 },
        { category: 'Configuration', score: 65, max: 100 },
        { category: 'Threats', score: 50, max: 100 },
        { category: 'Recovery', score: 80, max: 100 },
        { category: 'Response', score: 68, max: 100 },
      ]
    },
    iso: {
      name: 'ISO/IEC 27001',
      description: 'Information Security Management Systems',
      color: '#8b5cf6',
      data: [
        { category: 'Governance', score: 72, max: 100 },
        { category: 'Humains', score: 58, max: 100 },
        { category: 'Processus', score: 63, max: 100 },
        { category: 'Technologie', score: 76, max: 100 },
        { category: 'Incidents', score: 82, max: 100 },
      ]
    },
    custom: {
      name: 'Modèle Personnalisé',
      description: 'Basé sur votre contexte métier',
      color: '#f59e0b',
      data: [
        { category: 'Infrastructure', score: 68, max: 100 },
        { category: 'Applications', score: 72, max: 100 },
        { category: 'Données', score: 80, max: 100 },
        { category: 'Identité', score: 55, max: 100 },
        { category: 'Sécurité', score: 74, max: 100 },
      ]
    }
  };

  const currentFramework = complianceFrameworks[selectedFramework];
  const overallScore = Math.round(
    currentFramework.data.reduce((sum, item) => sum + item.score, 0) / currentFramework.data.length
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center">
            <BarChart3 className="mr-2 text-blue-600" size={28} />
            Radar de Conformité
          </h2>
          <p className="text-slate-500 mt-1">Analysez votre posture de conformité selon différents modèles</p>
        </div>
      </div>

      <Card className="border-t-4 border-t-blue-500">
        <div className="flex items-center justify-between mb-6 pb-6 border-b border-slate-200">
          <div>
            <h3 className="text-lg font-bold text-slate-800">Sélectionnez votre modèle de conformité</h3>
            <p className="text-sm text-slate-500 mt-1">Choisissez le framework qui correspond à vos besoins</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(complianceFrameworks).map(([key, framework]) => (
            <button
              key={key}
              onClick={() => setSelectedFramework(key)}
              className={`p-4 rounded-lg border-2 transition-all text-left ${
                selectedFramework === key
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-slate-200 bg-white hover:border-slate-300'
              }`}
            >
              <h4 className="font-semibold text-slate-800">{framework.name}</h4>
              <p className="text-xs text-slate-500 mt-2">{framework.description}</p>
            </button>
          ))}
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <Card className="h-full">
            <div className="flex justify-between items-center mb-6 pb-6 border-b border-slate-200">
              <div>
                <h3 className="font-bold text-slate-700 flex items-center">
                  <Radar className="mr-2 text-blue-500" size={20}/>
                  {currentFramework.name} - Couverture
                </h3>
                <p className="text-xs text-slate-500 mt-1">{currentFramework.description}</p>
              </div>
            </div>
            <div style={{ display: 'block', height: '400px', width: '100%', overflow: 'hidden' }}>
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="75%" data={currentFramework.data}>
                  <PolarGrid strokeDasharray="3 3" />
                  <PolarAngleAxis dataKey="category" tick={{ fill: '#64748b', fontSize: 12 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} />
                  <RechartsRadar 
                    name="Score Actuel" 
                    dataKey="score" 
                    stroke={currentFramework.color} 
                    fill={currentFramework.color} 
                    fillOpacity={0.5} 
                  />
                  <RechartsRadar 
                    name="Objectif" 
                    dataKey="max" 
                    stroke="#cbd5e1" 
                    fill="none" 
                    strokeDasharray="5 5"
                  />
                  <Legend wrapperStyle={{ paddingTop: '20px' }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <div className="text-center">
              <p className="text-slate-500 text-sm font-medium">Score Global</p>
              <h3 className="text-5xl font-bold text-slate-800 mt-2">{overallScore}</h3>
              <p className="text-slate-500 text-sm mt-2">/ 100</p>
              <div className="mt-4 w-full bg-slate-100 rounded-full h-2">
                <div 
                  className="h-2 rounded-full transition-all" 
                  style={{
                    width: `${overallScore}%`,
                    backgroundColor: currentFramework.color
                  }}
                ></div>
              </div>
            </div>
          </Card>

          <Card>
            <h3 className="font-bold text-slate-800 mb-4">Détails par catégorie</h3>
            <div className="space-y-3">
              {currentFramework.data.map((item, idx) => (
                <div key={idx}>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-sm font-medium text-slate-700">{item.category}</span>
                    <span className="text-sm font-bold text-slate-900">{item.score}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2">
                    <div 
                      className="h-2 rounded-full transition-all" 
                      style={{
                        width: `${item.score}%`,
                        backgroundColor: currentFramework.color
                      }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
