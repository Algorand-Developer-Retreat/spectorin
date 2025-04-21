'use client';

import React, { useState } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

// Mock components for demo
function SecurityScoreGauge({ score }) {
  const data = {
    labels: ['Score', 'Remaining'],
    datasets: [
      {
        data: [score, 100 - score],
        backgroundColor: [
          score >= 80 ? '#22c55e' : score >= 60 ? '#eab308' : '#ef4444',
          '#e5e7eb',
        ],
        borderWidth: 0,
      },
    ],
  };

  const options = {
    cutout: '70%',
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return (
    <div className="relative w-48 h-48">
      <Doughnut data={data} options={options} />
      <div className="absolute inset-0 flex items-center justify-center">
        <span className="text-3xl font-bold">{score}</span>
      </div>
    </div>
  );
}

function IssuesBreakdown({ issues }) {
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

export default function Home() {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('solidity');
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [error, setError] = useState(null);

  const analyzeCode = async () => {
    setAnalyzing(true);
    setError(null);
    
    try {
      console.log("Sending analysis request:", { code, language });
      
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code, language }),
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("Analysis response:", data);
      setResults(data);
    } catch (err) {
      console.error('Error analyzing code:', err);
      setError(err.message);
      setResults(null);
    } finally {
      setAnalyzing(false);
    }
  };
  
  const handleFileUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    
    setUploadedFile(file);
    
    const reader = new FileReader();
    reader.onload = (e) => {
      setCode(e.target?.result);
    };
    reader.readAsText(file);
    
    // Detect language from file extension
    const extension = file.name.split('.').pop()?.toLowerCase();
    if (extension === 'sol') setLanguage('solidity');
    else if (extension === 'rs') setLanguage('rust');
    else if (extension === 'move') setLanguage('move');
    else if (extension === 'py' || extension === 'teal') setLanguage('pyteal');
  };
  
  return (
    <div className="min-h-screen p-6">
      <header className="mb-8">
        <h1 className="text-3xl font-bold">Spectorin</h1>
        <p className="text-gray-600">Smart Contract Analyzer</p>
      </header>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Input Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Smart Contract Code</h2>
          
          <div className="flex gap-4 mb-4">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="border p-2 rounded"
            >
              <option value="solidity">Solidity</option>
              <option value="pyteal">PyTeal</option>
              <option value="move">Move</option>
              <option value="rust">Rust</option>
            </select>
            
            <input 
              type="file" 
              onChange={handleFileUpload}
              className="border p-2"
            />
          </div>
          
          <textarea
            rows={12}
            className="w-full border p-2 rounded mb-4"
            placeholder={`Enter your ${language} code...`}
            value={code}
            onChange={(e) => setCode(e.target.value)}
          />
          
          <button
            onClick={analyzeCode}
            disabled={analyzing || !code.trim()}
            className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            {analyzing ? 'Analyzing...' : 'Analyze Code'}
          </button>
        </div>
        
        {/* Results Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 p-4 rounded mb-4">
              {error}
            </div>
          )}
          
          {results ? (
            <div>
              <div className="flex justify-center mb-6">
                <SecurityScoreGauge score={results.score} />
              </div>
              
              {results.issues.length > 0 && (
                <>
                  <h3 className="font-semibold mt-6 mb-2">Issues Distribution</h3>
                  <IssuesBreakdown issues={results.issues} />
                  
                  <h3 className="font-semibold mt-6 mb-2">Detailed Issues</h3>
                  <ul className="divide-y">
                    {results.issues.map((issue, i) => (
                      <li key={i} className="py-2">
                        <div className="flex items-start">
                          <span 
                            className={`inline-block w-3 h-3 rounded-full mr-2 mt-1 ${
                              issue.severity === 'high' ? 'bg-red-500' : 
                              issue.severity === 'medium' ? 'bg-yellow-500' : 'bg-blue-500'
                            }`}
                          />
                          <div>
                            <p>{issue.message}</p>
                            {issue.line > 0 && <p className="text-sm text-gray-500">Line: {issue.line}</p>}
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                </>
              )}
              
              {results.recommendations.length > 0 && (
                <>
                  <h3 className="font-semibold mt-6 mb-2">Recommendations</h3>
                  <ul className="list-disc pl-5">
                    {results.recommendations.map((rec, i) => (
                      <li key={i} className="mb-1">{rec}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          ) : (
            <p className="text-gray-500">Enter your code and click "Analyze Code" to get results.</p>
          )}
        </div>
      </div>
    </div>
  );
}
