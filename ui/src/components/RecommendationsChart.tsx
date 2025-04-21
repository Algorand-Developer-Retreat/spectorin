'use client';

import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

interface RecommendationsChartProps {
  recommendations: string[];
}

export function RecommendationsChart({ recommendations }: RecommendationsChartProps) {
  const categories = {
    Security: recommendations.filter(r => r.toLowerCase().includes('security')).length,
    'Best Practices': recommendations.filter(r => r.toLowerCase().includes('practice')).length,
    Performance: recommendations.filter(r => r.toLowerCase().includes('performance')).length,
    Other: recommendations.filter(r => 
      !r.toLowerCase().includes('security') && 
      !r.toLowerCase().includes('practice') && 
      !r.toLowerCase().includes('performance')
    ).length,
  };

  const data = {
    labels: Object.keys(categories),
    datasets: [
      {
        data: Object.values(categories),
        backgroundColor: [
          '#22c55e',
          '#3b82f6',
          '#eab308',
          '#94a3b8',
        ],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom' as const,
      },
    },
  };

  return <Pie data={data} options={options} />;
} 