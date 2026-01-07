'use client'

import { motion } from 'framer-motion'
import { Brain, TrendingUp, Shield } from 'lucide-react'

export default function Header() {
  return (
    <motion.header 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="border-b border-dark-800/50 bg-dark-900/30 backdrop-blur-xl sticky top-0 z-50"
    >
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <Brain className="w-8 h-8 text-primary-500" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-primary-500 rounded-full animate-pulse"></div>
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">Multi-Agent Stock Research</h1>
              <p className="text-sm text-dark-400">AI • ML • Multibagger Discovery System</p>
            </div>
          </div>

          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-sm">
              <div className="status-indicator status-active"></div>
              <span className="text-primary-400 font-medium">9 Agents Active</span>
            </div>
            
            <div className="flex items-center space-x-2 text-sm">
              <TrendingUp className="w-4 h-4 text-accent-400" />
              <span className="text-dark-300">2,847 Stocks Analyzed</span>
            </div>
            
            <div className="flex items-center space-x-2 text-sm">
              <Shield className="w-4 h-4 text-primary-400" />
              <span className="text-dark-300">Sync Data</span>
            </div>
          </div>
        </div>
      </div>
    </motion.header>
  )
}