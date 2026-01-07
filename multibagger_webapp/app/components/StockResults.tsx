'use client'

import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, AlertTriangle, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'

interface StockResultsProps {
  results: any
}

export default function StockResults({ results }: StockResultsProps) {
  const [expandedStock, setExpandedStock] = useState<string | null>(null)

  const toggleExpanded = (symbol: string) => {
    setExpandedStock(expandedStock === symbol ? null : symbol)
  }

  const getProbabilityColor = (probability: number) => {
    if (probability >= 0.8) return 'text-green-400'
    if (probability >= 0.6) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getProbabilityBg = (probability: number) => {
    if (probability >= 0.8) return 'bg-green-500'
    if (probability >= 0.6) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className="space-y-8">
      {/* High Probability Multibaggers */}
      {results.high_probability_multibaggers?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <div className="flex items-center space-x-3 mb-6">
            <TrendingUp className="w-6 h-6 text-green-400" />
            <h2 className="text-2xl font-bold">High Probability Multibaggers</h2>
            <div className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm font-medium">
              {results.high_probability_multibaggers.length} Candidates
            </div>
          </div>

          <div className="grid gap-6">
            {results.high_probability_multibaggers.map((stock: any, index: number) => (
              <motion.div
                key={stock.symbol}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="stock-card"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4 mb-2">
                      <h3 className="text-xl font-bold text-green-400">#{index + 1}</h3>
                      <div>
                        <h4 className="text-lg font-semibold">{stock.symbol}</h4>
                        <p className="text-sm text-dark-400">{stock.sector}</p>
                      </div>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                      <div>
                        <p className="text-xs text-dark-400">Market Cap</p>
                        <p className="font-semibold">{stock.market_cap}</p>
                      </div>
                      <div>
                        <p className="text-xs text-dark-400">Timeframe</p>
                        <p className="font-semibold">{stock.expected_timeframe}</p>
                      </div>
                      <div>
                        <p className="text-xs text-dark-400">Current Price</p>
                        <p className="font-semibold">₹{stock.current_price}</p>
                      </div>
                      <div>
                        <p className="text-xs text-dark-400">Consensus</p>
                        <p className="font-semibold text-green-400">{stock.agent_consensus}</p>
                      </div>
                    </div>
                  </div>

                  <div className="text-right">
                    <div className="text-3xl font-bold text-green-400 mb-1">
                      {(stock.multibagger_probability * 100).toFixed(0)}%
                    </div>
                    <p className="text-sm text-dark-400">Multibagger Probability</p>
                    
                    <div className="mt-3 w-32">
                      <div className="progress-bar">
                        <div 
                          className="h-full bg-green-500 rounded-full transition-all duration-1000"
                          style={{ width: `${stock.multibagger_probability * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mb-4">
                  <h5 className="text-sm font-semibold mb-2 text-green-400">Key Triggers</h5>
                  <div className="flex flex-wrap gap-2">
                    {stock.key_triggers?.map((trigger: string, idx: number) => (
                      <span 
                        key={idx}
                        className="bg-green-500/20 text-green-300 px-3 py-1 rounded-full text-sm"
                      >
                        {trigger}
                      </span>
                    ))}
                  </div>
                </div>

                <button
                  onClick={() => toggleExpanded(stock.symbol)}
                  className="flex items-center space-x-2 text-primary-400 hover:text-primary-300 transition-colors"
                >
                  <span>Agent Analysis</span>
                  {expandedStock === stock.symbol ? 
                    <ChevronUp className="w-4 h-4" /> : 
                    <ChevronDown className="w-4 h-4" />
                  }
                </button>

                {expandedStock === stock.symbol && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mt-4 pt-4 border-t border-dark-700"
                  >
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                      <div className="text-center">
                        <div className="text-lg font-bold text-blue-400">
                          {stock.detailed_scores?.fundamental_score}/10
                        </div>
                        <p className="text-xs text-dark-400">Fundamental</p>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-purple-400">
                          {stock.detailed_scores?.management_score}/10
                        </div>
                        <p className="text-xs text-dark-400">Management</p>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-green-400">
                          {stock.detailed_scores?.technical_stage}
                        </div>
                        <p className="text-xs text-dark-400">Technical</p>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-yellow-400">
                          {stock.detailed_scores?.smart_money_score}/10
                        </div>
                        <p className="text-xs text-dark-400">Smart Money</p>
                      </div>
                      <div className="text-center">
                        <div className="text-lg font-bold text-indigo-400">
                          {stock.detailed_scores?.policy_strength}
                        </div>
                        <p className="text-xs text-dark-400">Policy</p>
                      </div>
                    </div>

                    <div>
                      <h6 className="text-sm font-semibold mb-2 text-red-400">Major Risks</h6>
                      <div className="flex flex-wrap gap-2">
                        {stock.major_risks?.map((risk: string, idx: number) => (
                          <span 
                            key={idx}
                            className="bg-red-500/20 text-red-300 px-3 py-1 rounded-full text-sm"
                          >
                            {risk}
                          </span>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Early Watchlist */}
      {results.early_watchlist?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="flex items-center space-x-3 mb-6">
            <AlertTriangle className="w-6 h-6 text-yellow-400" />
            <h2 className="text-2xl font-bold">Early Watchlist</h2>
            <div className="bg-yellow-500/20 text-yellow-400 px-3 py-1 rounded-full text-sm font-medium">
              {results.early_watchlist.length} Stocks
            </div>
          </div>

          <div className="space-y-4">
            {results.early_watchlist.map((stock: any, index: number) => (
              <div key={stock.symbol} className="stock-card">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-4 mb-2">
                      <h4 className="text-lg font-semibold">{stock.symbol}</h4>
                      <span className="text-sm text-dark-400">{stock.sector}</span>
                    </div>
                    <div className="flex space-x-6 text-sm">
                      <span>Cap: {stock.market_cap}</span>
                      <span>Timeframe: {stock.expected_timeframe}</span>
                      <span className="text-yellow-400">{stock.agent_consensus}</span>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-xl font-bold text-yellow-400">
                      {(stock.multibagger_probability * 100).toFixed(0)}%
                    </div>
                    <div className="w-24 mt-2">
                      <div className="progress-bar">
                        <div 
                          className="h-full bg-yellow-500 rounded-full"
                          style={{ width: `${stock.multibagger_probability * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Rejected Stocks */}
      {results.rejected_stocks?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <div className="flex items-center space-x-3 mb-6">
            <TrendingDown className="w-6 h-6 text-red-400" />
            <h2 className="text-2xl font-bold">Rejected Stocks</h2>
            <div className="bg-red-500/20 text-red-400 px-3 py-1 rounded-full text-sm font-medium">
              {results.rejected_stocks.length} Stocks
            </div>
          </div>

          <div className="space-y-3">
            {results.rejected_stocks.slice(0, 3).map((stock: any, index: number) => (
              <div key={stock.symbol} className="glass-card p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-semibold">{stock.symbol}</span>
                    <span className="text-sm text-dark-400 ml-3">{stock.sector}</span>
                  </div>
                  <div className="text-right">
                    <div className="text-red-400 font-semibold">
                      {(stock.multibagger_probability * 100).toFixed(0)}%
                    </div>
                    <div className="text-xs text-dark-400">{stock.rejection_reason}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  )
}