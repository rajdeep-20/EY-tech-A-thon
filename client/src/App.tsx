import { useState, useEffect } from 'react'
import './App.css'

function App() {
    const [count, setCount] = useState(0)
    const [healthStatus, setHealthStatus] = useState<string>('Checking...')

    useEffect(() => {
        fetch('http://localhost:8081/api/health')
            .then(res => res.json())
            .then(data => setHealthStatus(data.message))
            .catch(() => setHealthStatus('Backend not reachable'))
    }, [])

    return (
        <>
            <h1>Vite + React</h1>
            <div className="card">
                <p>Backend Status: <strong>{healthStatus}</strong></p>
                <button onClick={() => setCount((count) => count + 1)}>
                    count is {count}
                </button>
            </div>
        </>
    )
}

export default App
