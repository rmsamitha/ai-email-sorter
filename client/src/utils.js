import { useEffect } from 'react'

// Health check utility to keep backend alive
// This hook automatically sets up a health check that runs every 15 minutes
export const backendKeepAlive = () => {
  useEffect(() => {
    // Health check call to the backend
    const healthCheck = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const response = await fetch(`${apiUrl}/health`)
        const data = await response.json()
        console.log('backendKeepAlive Health check:', data)
      } catch (error) {
        console.error('backendKeepAlive Health check error:', error.message)
      }
    }

    // Call immediately on mount
    healthCheck()
    
    // Set up interval to call every 15 minutes (900000 milliseconds)
    const intervalId = setInterval(() => {
      healthCheck()
    }, 15 * 60 * 1000) // 15 minutes in milliseconds

    // Cleanup interval on component unmount
    return () => {
      clearInterval(intervalId)
    }
  }, [])
}

