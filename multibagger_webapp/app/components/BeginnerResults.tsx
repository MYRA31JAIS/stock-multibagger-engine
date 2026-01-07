'use client'

import { motion } from 'framer-motion'
import { TrendingUp, Clock, DollarSign, Target, AlertCircle } from 'lucide-react'

interface BeginnerResultsProps {
  results: any
}

export default function BeginnerResults({ results }: BeginnerResultsProps) {
  const calculatePotentialReturns = (probability: number, timeframe: string) => {
    const baseMultiplier = probability > 0.8 ? 8 : probability > 0.6 ? 5 : 3
    const years = timeframe.includes('2-4') ? 3 : timeframe.includes('3-5') ? 4 : 5
    
    return {
      conservative: baseMultiplier * 0.6,
      realistic: baseMultiplier,
      optimistic: baseMultiplier * 1.5,
      years
    }
  }

  return (
    <div className="space-y-8">
      {/* Investment Calculator */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-card p-6"
      >
        <h2 className="text-2xl font-bold mb-4 flex items-center space-x-3">
          <DollarSign className="w-6 h-6 text-green-400" />
          <span>💰 Your Potential Returns</span>
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-green-500/20 p-4 rounded-lg text-center">
            <h3 className="font-semibold text-green-300">Small Investment</h3>
            <p className="text-2xl font-bold text-green-400">₹10,000</p>
            <p className="text-sm text-green-200">Starting amount</p>
          </div>
          <div className="bg-blue-500/20 p-4 rounded-lg text-center">
            <h3 className="font-semibold text-blue-300">Medium Investment</h3>
            <p className="text-2xl font-bold text-blue-400">₹50,000</p>
            <p className="text-sm text-blue-200">After 1 year SIP</p>
          </div>
          <div className="bg-purple-500/20 p-4 rounded-lg text-center">
            <h3 className="font-semibold text-purple-300">Large Investment</h3>
            <p className="text-2xl font-bold text-purple-400">₹1,00,000</p>
            <p className="text-sm text-purple-200">After 2 years SIP</p>
          </div>
        </div>
      </motion.div>

      {/* High Conviction Stocks */}
      {results.high_probability_multibaggers?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-center space-x-3 mb-6">
            <TrendingUp className="w-6 h-6 text-green-400" />
            <h2 className="text-2xl font-bold">🚀 Best Investment Opportunities</h2>
            <div className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm font-medium">
              {results.high_probability_multibaggers.length} Top Picks
            </div>
          </div>

          <div className="space-y-6">
            {results.high_probability_multibaggers.map((stock: any, index: number) => {
              const returns = calculatePotentialReturns(stock.multibagger_probability, stock.expected_timeframe)
              
              return (
                <motion.div
                  key={stock.symbol}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="glass-card p-6 border-l-4 border-green-500"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="text-2xl font-bold text-green-400">#{index + 1}</span>
                        <div>
                          <h3 className="text-xl font-bold">{stock.symbol}</h3>
                          <p className="text-dark-400">{stock.sector}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-4 text-sm">
                        <span className="bg-green-500/20 text-green-300 px-2 py-1 rounded">
                          {(stock.multibagger_probability * 100).toFixed(0)}% Confidence
                        </span>
                        <span className="text-dark-300">
                          Expected: {stock.expected_timeframe}
                        </span>
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-3xl font-bold text-green-400">
                        {returns.realistic}x
                      </div>
                      <p className="text-sm text-dark-400">Potential Multiplier</p>
                    </div>
                  </div>

                  {/* Potential Returns Table */}
                  <div className="bg-dark-800/50 rounded-lg p-4 mb-4">
                    <h4 className="font-semibold mb-3 text-green-300">💵 What Your Money Could Become:</h4>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div className="text-center">
                        <p className="text-dark-400">Conservative</p>
                        <p className="font-bold text-yellow-400">{returns.conservative.toFixed(1)}x</p>
                      </div>
                      <div className="text-center">
                        <p className="text-dark-400">Realistic</p>
                        <p className="font-bold text-green-400">{returns.realistic}x</p>
                      </div>
                      <div className="text-center">
                        <p className="text-dark-400">Optimistic</p>
                        <p className="font-bold text-blue-400">{returns.optimistic.toFixed(1)}x</p>
                      </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-dark-600">
                      <div className="grid grid-cols-3 gap-4 text-xs">
                        <div className="text-center">
                          <p className="text-dark-400">₹10,000 →</p>
                          <p className="font-bold text-yellow-400">₹{(10000 * returns.conservative).toLocaleString()}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-dark-400">₹10,000 →</p>
                          <p className="font-bold text-green-400">₹{(10000 * returns.realistic).toLocaleString()}</p>
                        </div>
                        <div className="text-center">
                          <p className="text-dark-400">₹10,000 →</p>
                          <p className="font-bold text-blue-400">₹{(10000 * returns.optimistic).toLocaleString()}</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Why This Stock */}
                  <div className="mb-4">
                    <h5 className="font-semibold mb-2 text-green-300">🎯 Why This Could Be a Winner:</h5>
                    <div className="flex flex-wrap gap-2">
                      {stock.key_triggers?.slice(0, 3).map((trigger: string, idx: number) => (
                        <span 
                          key={idx}
                          className="bg-green-500/20 text-green-200 px-3 py-1 rounded-full text-sm"
                        >
                          {trigger}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Simple Action Plan */}
                  <div className="bg-primary-500/20 p-4 rounded-lg">
                    <h5 className="font-semibold mb-2 text-primary-300">📋 Simple Action Plan:</h5>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                      <div className="flex items-center space-x-2">
                        <Target className="w-4 h-4 text-primary-400" />
                        <span>Start with ₹5,000-10,000</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Clock className="w-4 h-4 text-primary-400" />
                        <span>Hold for {returns.years}+ years</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <TrendingUp className="w-4 h-4 text-primary-400" />
                        <span>Add more on dips</span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </motion.div>
      )}

      {/* Learning Stocks (Watchlist) */}
      {results.early_watchlist?.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center space-x-3 mb-6">
            <AlertCircle className="w-6 h-6 text-yellow-400" />
            <h2 className="text-2xl font-bold">📚 Learning Opportunities</h2>
            <div className="bg-yellow-500/20 text-yellow-400 px-3 py-1 rounded-full text-sm font-medium">
              Practice Stocks
            </div>
          </div>

          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mb-4">
            <p className="text-yellow-200 text-sm">
              <strong>💡 Tip:</strong> These stocks have potential but need more time to develop. 
              Great for learning and small investments while you watch how they perform.
            </p>
          </div>

          <div className="grid gap-4">
            {results.early_watchlist.map((stock: any, index: number) => (
              <div key={stock.symbol} className="glass-card p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-semibold">{stock.symbol}</h4>
                    <p className="text-sm text-dark-400">{stock.sector}</p>
                    <p className="text-xs text-yellow-400 mt-1">
                      {(stock.multibagger_probability * 100).toFixed(0)}% confidence • {stock.expected_timeframe}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-yellow-400">
                      3-5x potential
                    </div>
                    <p className="text-xs text-dark-400">₹10,000 → ₹30,000-50,000</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* No Results Message */}
      {(!results.high_probability_multibaggers?.length && !results.early_watchlist?.length) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass-card p-8 text-center"
        >
          <AlertCircle className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No Strong Opportunities Right Now</h3>
          <p className="text-dark-300 mb-4">
            The AI system is being very careful with your money. Try different stock sets or check back later.
          </p>
          <div className="bg-blue-500/20 p-4 rounded-lg">
            <p className="text-blue-200 text-sm">
              <strong>💡 This is actually good!</strong> It means the system won't recommend risky investments. 
              Quality multibaggers are rare - that's what makes them special.
            </p>
          </div>
        </motion.div>
      )}
    </div>
  )
}