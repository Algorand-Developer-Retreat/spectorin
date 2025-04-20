// ui/pages/index.tsx
import { useState } from 'react'

export default function Home() {
  const [code, setCode] = useState('')
  const [result, setResult] = useState('')

  async function analyze() {
    const res = await fetch('/api/analyze', {
      method: 'POST',
      body: JSON.stringify({ code }),
      headers: { 'Content-Type': 'application/json' },
    })
    const json = await res.json()
    setResult(json.explanation)
  }

  return (
    <div className="p-10">
      <textarea onChange={(e) => setCode(e.target.value)} />
      <button onClick={analyze}>Analyze</button>
      <pre>{result}</pre>
    </div>
  )
}
