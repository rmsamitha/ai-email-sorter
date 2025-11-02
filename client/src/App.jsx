import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { backendKeepAlive } from './utils'

function App() {
  // Set up automatic health check to keep backend alive
  backendKeepAlive()

  const [apiResponse, setApiResponse] = useState('')

  const callFastAPI = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/`)
      const data = await response.json()
      setApiResponse(JSON.stringify(data, null, 2))
    } catch (error) {
      setApiResponse(`Error: ${error.message}`)
    }
  }
  return (
    <>
      <div>
        <a  target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a  target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>AI Email Sorter</h1>
      <div className="card">
        <button onClick={callFastAPI}>
          Call FastAPI Root Endpoint
        </button>
        {apiResponse && (
          <textarea
            readOnly
            value={apiResponse}
            style={{
              width: '100%',
              minHeight: '100px',
              marginTop: '20px',
              padding: '10px',
              fontFamily: 'monospace',
              fontSize: '14px'
            }}
          />
        )}
      </div>
  
    </>
  )
}

export default App
