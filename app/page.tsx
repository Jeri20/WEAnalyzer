'use client';

import { useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function Home() {
  const [url, setUrl] = useState('');
  const [analysis, setAnalysis] = useState<any>(null);

  const handleSubmit = async () => {
    try {
      const res = await fetch('http://localhost:8000/analyze-website', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });
      if (!res.ok) throw new Error('Failed to fetch');
      const data = await res.json();
      setAnalysis([data]);
    } catch (error) {
      console.error('Error fetching analysis:', error);
      alert('Failed to connect to backend. Please check if FastAPI server is running.');
    }
  };

  const chartData = analysis ? {
    labels: analysis[0].entities_found.concat(analysis[0].missing_entities),
    datasets: [{
      label: 'Entities Detected',
      data: analysis[0].entities_found.map(() => 1).concat(analysis[0].missing_entities.map(() => 0)),
      borderColor: '#0070f3',
      backgroundColor: 'rgba(0, 112, 243, 0.2)',
      tension: 0.4,
    }],
  } : null;

  return (
    <div className="p-5 font-sans text-center">
      <h1 className="text-2xl font-bold mb-4">Website Entity & Intent Analyzer</h1>
      <input
        className="p-2 border rounded w-1/2"
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter Website URL"
      />
      <button className="ml-2 p-2 bg-blue-500 text-white rounded" onClick={handleSubmit}>Analyze</button>
      {analysis && (
        <div className="mt-6 text-left">
          {analysis.map((item: any, index: number) => (
            <div key={index} className="mb-4 border p-4 rounded">
              <h2 className="font-semibold">{item.title}</h2>
              <p><strong>Entities Found:</strong> {item.entities_found.join(', ')}</p>
              <p><strong>Missing Entities:</strong> {item.missing_entities.join(', ')}</p>
              <p><strong>Search Intent:</strong> {item.search_intent}</p>
            </div>
          ))}
          {chartData && (
            <div className="mt-6">
              <h3 className="mb-2 font-semibold">Entity Detection Chart</h3>
              <Line data={chartData} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
