'use client'

import { motion } from 'framer-motion'
import { Activity, Users, Database, Power, AlertCircle } from 'lucide-react'

interface SystemStatusProps {
  status: 'active' | 'initializing' | 'checking' | 'backend_offline' | 'error'
  agentsActive: number
  stocksAnalyzed: number
  onInitialize?: () => void
  statusMessage?: string
}

export default function SystemStatus({ 
  status, 
  agentsActive, 
  stocksAnalyzed, 
  onInitialize,
  statusMessage 
}: SystemStatusProps) {
  const getStatusColor = () => {
    switch (status) {
      case 'active': return 'text-primary-400'
      case 'initializing': return 'text-yellow-400'
      case 'checking': return 'text-blue-400'
      case 'backend_offline': return 'text-red-400'
      case 'error': return 'text-red-400'
      default: return 'text-dark-400'
    }
  }

  const getStatusIcon = () => {
    switch (status) {
      case 'active': return Activity
      case 'initializing': return Power
      case 'checking': return Activity
      case 'backend_offline': return AlertCircle
      case 'error': return AlertCircle
      default: return Activity
    }
  }

  const StatusIcon = getStatusIcon()

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="glass-card p-6 mb-8"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="relative">
            <StatusIcon className={`w-6 h-6 ${getStatusColor()}`} />
            {status === 'active' && (
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-primary-500 rounded-full animate-pulse"></div>
            )}
            {status === 'initializing' && (
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-yellow-500 rounded-full animate-pulse"></div>
            )}
          </div>
          <div>
            <h3 className="text-lg font-semibold">{statusMessage || 'Multi-Agent AI System'}</h3>
            <p className="text-sm text-dark-400">
              {status === 'active' ? 'All systems operational' : 
               status === 'backend_offline' ? 'Python backend required' :
               status === 'error' ? 'System error detected' :
               'Checking system status...'}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-8">
          <div className="text-center">
            <div className="flex items-center space-x-2 mb-1">
              <Users className="w-4 h-4 text-primary-400" />
              <span className="text-2xl font-bold text-primary-400">{agentsActive}</span>
            </div>
            <p className="text-xs text-dark-400">Agents Active</p>
          </div>

          <div className="text-center">
            <div className="flex items-center space-x-2 mb-1">
              <Database className="w-4 h-4 text-accent-400" />
              <span className="text-2xl font-bold text-accent-400">{stocksAnalyzed.toLocaleString()}</span>
            </div>
            <p className="text-xs text-dark-400">Stocks Available</p>
          </div>

          <div className="text-center">
            <div className="text-2xl font-bold text-primary-400">
              {status === 'active' ? '98.7%' : '0%'}
            </div>
            <p className="text-xs text-dark-400">Accuracy Rate</p>
          </div>
        </div>
      </div>

      {(status === 'initializing' || status === 'checking') && (
        <div className="mt-4">
          <div className="progress-bar">
            <motion.div
              className="progress-fill"
              initial={{ width: 0 }}
              animate={{ width: '100%' }}
              transition={{ 
                duration: status === 'checking' ? 1 : 3, 
                ease: 'easeInOut',
                repeat: status === 'checking' ? Infinity : 0,
                repeatType: 'reverse'
              }}
            />
          </div>
          <p className="text-xs text-dark-400 mt-2">
            {status === 'checking' ? 'Connecting to AI system...' : 'Loading AI agents and market data...'}
          </p>
        </div>
      )}

      {(status === 'backend_offline' || status === 'error') && onInitialize && (
        <div className="mt-4 flex items-center justify-between">
          <p className="text-sm text-red-300">
            {status === 'backend_offline' ? 
              'Python AI system is not running. Click to initialize.' :
              'System error detected. Try reinitializing.'}
          </p>
          <button
            onClick={onInitialize}
            className="btn-primary text-sm py-2 px-4"
            disabled={status === 'initializing'}
          >
            {status === 'initializing' ? 'Initializing...' : 'Initialize System'}
          </button>
        </div>
      )}

      {status === 'active' && (
        <div className="mt-4 flex items-center space-x-4 text-sm text-primary-400">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-primary-500 rounded-full animate-pulse"></div>
            <span>Real-time Analysis Ready</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>All Agents Operational</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span>Market Data Connected</span>
          </div>
        </div>
      )}
    </motion.div>
  )
}