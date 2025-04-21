'use client';

import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface Issue {
  severity: string;
  message: string;
}

interface IssuesBreakdownProps {
  issues: Issue[];
}

export function IssuesBreakdown({ issues }: IssuesBreakdownProps) {
  const severityCounts = {
    high: issues.filter(i => i.severity === 'high').length,
    medium: issues.filter(i => i.severity === 'medium').length,
    low: issues.filter(i => i.severity === 'low').length,
  };

  const data = {
    labels: ['High', 'Medium', 'Low'],
    datasets: [
      {
        label: 'Number of Issues',
        data: [severityCounts.high, severityCounts.medium, severityCounts.low],
        backgroundColor: ['#ef4444', '#eab308', '#3b82f6'],
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return <Bar data={data} options={options} />;
} 