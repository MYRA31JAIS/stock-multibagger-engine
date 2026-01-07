'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import AgentGrid from './components/AgentGrid'
import StockResults from './components/StockResults'
import AnalysisPanel from './components/AnalysisPanel'
import SystemStatus from './components/SystemStatus'
import BeginnerGuide from './components/BeginnerGuide'

// Get API URL from environment or use default
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

export default function Home() {
  const [systemStatus, setSystemStatus] = useState('checking')
  const [analysisResults, setAnalysisResults] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [selectedStocks, setSelectedStocks] = useState([])
  const [error, setError] = useState('')
  const [systemInfo, setSystemInfo] = useState(null)

  useEffect(() => {
    checkSystemStatus()
    // Check status every 30 seconds
    const interval = setInterval(checkSystemStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  const checkSystemStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/api/status`)
      const status = await response.json()
      
      if (status.status === 'operational') {
        setSystemStatus('active')
        setSystemInfo(status)
        setError('')
      } else if (status.backend_running === false) {
        setSystemStatus('backend_offline')
        setError('Python AI system is not running. Please start the backend server.')
      } else {
        setSystemStatus('error')
        setError(status.message || 'System error')
      }
    } catch (err) {
      setSystemStatus('backend_offline')
      setError('Cannot connect to Python AI system')
    }
  }

  const initializeSystem = async () => {
    setSystemStatus('initializing')
    setError('')
    
    try {
      const response = await fetch(`${API_URL}/api/initialize`, {
        method: 'POST'
      })
      
      const result = await response.json()
      
      if (response.ok && result.success) {
        setSystemStatus('active')
        setSystemInfo(result.status)
        setError('')
      } else {
        setSystemStatus('error')
        setError(result.error || 'Initialization failed')
      }
    } catch (err: any) {
      setSystemStatus('error')
      setError(err.message || 'Failed to initialize system')
    }
  }

  const handleAnalysis = async (stocks: string[]) => {
    if (systemStatus !== 'active') {
      setError('System must be initialized before running analysis')
      return
    }

    setIsAnalyzing(true)
    setSelectedStocks(stocks)
    setError('')
    
    try {
      const response = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stocks })
      })
      
      const results = await response.json()
      
      if (response.ok) {
        setAnalysisResults(results)
        setError('')
      } else {
        setError(results.error || 'Analysis failed')
        setAnalysisResults(null)
      }
    } catch (err: any) {
      setError(err.message || 'Analysis request failed')
      setAnalysisResults(null)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getStatusMessage = () => {
    switch (systemStatus) {
      case 'checking': return 'Checking system status...'
      case 'backend_offline': return 'Python AI system offline'
      case 'initializing': return 'Initializing AI agents...'
      case 'active': return 'System operational'
      case 'error': return 'System error'
      default: return 'Unknown status'
    }
  }

  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="container mx-auto px-6 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold mb-4">
              Discover <span className="gradient-text">Multibagger</span> Opportunities
            </h1>
            <p className="text-xl text-dark-300 max-w-4xl mx-auto">
              9 specialized AI agents analyze 2,800+ NSE/BSE stocks across fundamentals, 
              technicals, policy, and smart money signals to identify high-probability 5x-20x 
              candidates.
            </p>
          </div>

          <SystemStatus 
            status={systemStatus}
            agentsActive={systemInfo?.agents ? Object.keys(systemInfo.agents).length : 0}
            stocksAnalyzed={2847}
            onInitialize={initializeSystem}
            statusMessage={getStatusMessage()}
          />

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-red-500/20 border border-red-500/50 rounded-lg p-4 mb-6"
            >
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                <p className="text-red-300 font-medium">System Error</p>
              </div>
              <p className="text-red-200 text-sm mt-1">{error}</p>
              {systemStatus === 'backend_offline' && (
                <div className="mt-3 p-3 bg-dark-800 rounded border-l-4 border-yellow-500">
                  <p className="text-yellow-300 text-sm font-medium">Backend URL: {API_URL}</p>
                  <p className="text-yellow-200 text-xs mt-1">
                    Make sure the backend is running and accessible
                  </p>
                </div>
              )}
            </motion.div>
          )}
        </motion.div>

        <BeginnerGuide />

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          <div className="xl:col-span-2">
            <AgentGrid systemStatus={systemStatus} systemInfo={systemInfo} />
            
            {analysisResults && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
                className="mt-8"
              >
                <StockResults results={analysisResults} />
              </motion.div>
            )}
          </div>

          <div className="xl:col-span-1">
            <AnalysisPanel 
              onAnalyze={handleAnalysis}
              isAnalyzing={isAnalyzing}
              systemStatus={systemStatus}
            />
          </div>
        </div>
      </main>
    </div>
  )
}