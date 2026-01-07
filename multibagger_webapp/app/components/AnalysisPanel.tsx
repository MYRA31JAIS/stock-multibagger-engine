'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Play, Loader2, Search, TrendingUp } from 'lucide-react'

interface AnalysisPanelProps {
  onAnalyze: (stocks: string[]) => void
  isAnalyzing: boolean
  systemStatus: string
}

const predefinedSets = [
  {
    name: 'Historical Multibaggers',
    stocks: ['TANLA.NS', 'DIXON.NS', 'TRENT.NS', 'KPIT.NS', 'CGPOWER.NS'],
    description: 'Proven 5x-20x performers'
  },
  {
    name: 'Defense & Aerospace',
    stocks: ['HAL.NS', 'BEL.NS', 'KPIT.NS', 'IRFC.NS'],
    description: 'Defense modernization plays'
  },
  {
    name: 'Green Energy',
    stocks: ['KPIGREEN.NS', 'WAAREE.NS', 'PRAJIND.NS'],
    description: 'Renewable energy leaders'
  },
  {
    name: 'High Growth Potential',
    stocks: ['RELIANCE.NS', 'ADANIPORTS.NS', 'BAJFINANCE.NS'],
    description: 'Large caps with multibagger potential'
  }
]

export default function AnalysisPanel({ onAnalyze, isAnalyzing, systemStatus }: AnalysisPanelProps) {
  const [selectedSet, setSelectedSet] = useState('')
  const [customStocks, setCustomStocks] = useState('')
  const [analysisType, setAnalysisType] = useState('predefined')

  const handleAnalyze = () => {
    let stocks: string[] = []
    
    if (analysisType === 'predefined' && selectedSet) {
      const set = predefinedSets.find(s => s.name === selectedSet)
      stocks = set?.stocks || []
    } else if (analysisType === 'custom' && customStocks) {
      stocks = customStocks.split('\n').map(s => s.trim()).filter(s => s)
    }
    
    if (stocks.length > 0) {
      onAnalyze(stocks)
    }
  }

  const canAnalyze = systemStatus === 'active' && !isAnalyzing && 
    ((analysisType === 'predefined' && selectedSet) || 
     (analysisType === 'custom' && customStocks.trim()))

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6 }}
      className="glass-card p-6 sticky top-24"
    >
      <div className="flex items-center space-x-3 mb-6">
        <Search className="w-5 h-5 text-primary-500" />
        <h3 className="text-xl font-semibold">Run Analysis</h3>
      </div>

      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium mb-3">Analysis Type</label>
          <div className="space-y-2">
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="radio"
                name="analysisType"
                value="predefined"
                checked={analysisType === 'predefined'}
                onChange={(e) => setAnalysisType(e.target.value)}
                className="text-primary-500"
              />
              <span>Predefined Sets</span>
            </label>
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="radio"
                name="analysisType"
                value="custom"
                checked={analysisType === 'custom'}
                onChange={(e) => setAnalysisType(e.target.value)}
                className="text-primary-500"
              />
              <span>Custom Stocks</span>
            </label>
          </div>
        </div>

        {analysisType === 'predefined' && (
          <div>
            <label className="block text-sm font-medium mb-3">Select Stock Set</label>
            <div className="space-y-3">
              {predefinedSets.map((set) => (
                <div
                  key={set.name}
                  onClick={() => setSelectedSet(set.name)}
                  className={`p-4 rounded-lg border cursor-pointer transition-all ${
                    selectedSet === set.name
                      ? 'border-primary-500 bg-primary-500/10'
                      : 'border-dark-600 hover:border-dark-500'
                  }`}
                >
                  <div className="font-medium mb-1">{set.name}</div>
                  <div className="text-sm text-dark-400 mb-2">{set.description}</div>
                  <div className="text-xs text-primary-400">
                    {set.stocks.join(', ')}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {analysisType === 'custom' && (
          <div>
            <label className="block text-sm font-medium mb-3">Enter Stock Symbols</label>
            <textarea
              value={customStocks}
              onChange={(e) => setCustomStocks(e.target.value)}
              placeholder="RELIANCE.NS&#10;TCS.NS&#10;INFY.NS"
              className="w-full h-32 p-3 bg-dark-800 border border-dark-600 rounded-lg text-white placeholder-dark-400 focus:border-primary-500 focus:outline-none"
            />
            <p className="text-xs text-dark-400 mt-2">
              Enter one symbol per line (e.g., RELIANCE.NS)
            </p>
          </div>
        )}

        <button
          onClick={handleAnalyze}
          disabled={!canAnalyze}
          className={`w-full py-4 rounded-lg font-semibold transition-all flex items-center justify-center space-x-2 ${
            canAnalyze
              ? 'btn-primary'
              : 'bg-dark-700 text-dark-400 cursor-not-allowed'
          }`}
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Play className="w-5 h-5" />
              <span>Run AI Analysis</span>
            </>
          )}
        </button>

        {systemStatus !== 'active' && (
          <div className="text-center text-sm text-yellow-400">
            System initializing... Please wait.
          </div>
        )}
      </div>
    </motion.div>
  )
}