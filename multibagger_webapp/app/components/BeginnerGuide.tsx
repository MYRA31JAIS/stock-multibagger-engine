'use client'

import { motion } from 'framer-motion'
import { TrendingUp, AlertTriangle, BookOpen, Target, Clock, DollarSign } from 'lucide-react'

export default function BeginnerGuide() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6 mb-8"
    >
      <div className="flex items-center space-x-3 mb-6">
        <BookOpen className="w-6 h-6 text-primary-500" />
        <h2 className="text-2xl font-bold">Beginner's Guide to Multibagger Investing</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* What are Multibaggers */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-primary-400 flex items-center space-x-2">
            <Target className="w-5 h-5" />
            <span>What are Multibaggers?</span>
          </h3>
          <div className="space-y-3 text-sm">
            <div className="bg-green-500/20 p-3 rounded-lg">
              <p className="font-medium text-green-300">5x Multibagger Example:</p>
              <p className="text-green-200">₹10,000 → ₹50,000 (in 3-5 years)</p>
            </div>
            <div className="bg-blue-500/20 p-3 rounded-lg">
              <p className="font-medium text-blue-300">10x Multibagger Example:</p>
              <p className="text-blue-200">₹10,000 → ₹1,00,000 (in 5-7 years)</p>
            </div>
            <div className="bg-purple-500/20 p-3 rounded-lg">
              <p className="font-medium text-purple-300">20x Multibagger Example:</p>
              <p className="text-purple-200">₹10,000 → ₹2,00,000 (in 7-10 years)</p>
            </div>
          </div>
        </div>

        {/* Realistic Timeline */}
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-yellow-400 flex items-center space-x-2">
            <Clock className="w-5 h-5" />
            <span>Realistic Timeline</span>
          </h3>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between items-center p-2 bg-dark-800 rounded">
              <span>1 Week:</span>
              <span className="text-red-400">-5% to +15% (Normal)</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-dark-800 rounded">
              <span>1 Year:</span>
              <span className="text-yellow-400">20% to 100% (Good)</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-dark-800 rounded">
              <span>3-5 Years:</span>
              <span className="text-green-400">300% to 1000% (Multibagger)</span>
            </div>
            <div className="flex justify-between items-center p-2 bg-dark-800 rounded">
              <span>5-10 Years:</span>
              <span className="text-primary-400">1000%+ (Life Changing)</span>
            </div>
          </div>
        </div>
      </div>

      {/* Investment Strategy for Beginners */}
      <div className="mt-6 p-4 bg-gradient-to-r from-primary-500/20 to-accent-500/20 rounded-lg">
        <h3 className="text-lg font-semibold mb-3 flex items-center space-x-2">
          <DollarSign className="w-5 h-5" />
          <span>Smart Investment Strategy for Beginners</span>
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="bg-dark-800/50 p-3 rounded">
            <h4 className="font-medium text-green-400 mb-2">Start Small & Learn</h4>
            <ul className="space-y-1 text-dark-300">
              <li>• Begin with ₹1,000-5,000</li>
              <li>• Pick 1-2 high conviction stocks</li>
              <li>• Learn from experience</li>
              <li>• Don't invest borrowed money</li>
            </ul>
          </div>
          
          <div className="bg-dark-800/50 p-3 rounded">
            <h4 className="font-medium text-blue-400 mb-2">Build Gradually</h4>
            <ul className="space-y-1 text-dark-300">
              <li>• Add ₹2,000-5,000 monthly</li>
              <li>• Use SIP approach</li>
              <li>• Diversify across 5-8 stocks</li>
              <li>• Reinvest profits</li>
            </ul>
          </div>
          
          <div className="bg-dark-800/50 p-3 rounded">
            <h4 className="font-medium text-purple-400 mb-2">Stay Patient</h4>
            <ul className="space-y-1 text-dark-300">
              <li>• Hold for 3-5 years minimum</li>
              <li>• Ignore daily price movements</li>
              <li>• Focus on company growth</li>
              <li>• Review quarterly results</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Warning Section */}
      <div className="mt-6 p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
        <div className="flex items-start space-x-3">
          <AlertTriangle className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-semibold text-red-300 mb-2">⚠️ Important Reality Check</h3>
            <div className="text-sm text-red-200 space-y-2">
              <p><strong>IMPOSSIBLE:</strong> ₹1 → ₹10 in 1 week (1000% return)</p>
              <p><strong>REALISTIC:</strong> ₹10,000 → ₹50,000 in 3-5 years (400% return)</p>
              <p><strong>REMEMBER:</strong> Stock markets have risks. You can lose money too.</p>
              <p><strong>ADVICE:</strong> Never invest money you can't afford to lose.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Success Stories */}
      <div className="mt-6">
        <h3 className="text-lg font-semibold mb-3 text-primary-400">🏆 Real Multibagger Examples (Historical)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="bg-dark-800/30 p-3 rounded">
            <h4 className="font-medium text-green-400">TANLA Solutions</h4>
            <p className="text-dark-300">₹10 → ₹1,200 (120x in 5 years)</p>
            <p className="text-xs text-dark-400">Investment: ₹10,000 → ₹12,00,000</p>
          </div>
          <div className="bg-dark-800/30 p-3 rounded">
            <h4 className="font-medium text-green-400">Dixon Technologies</h4>
            <p className="text-dark-300">₹1,500 → ₹15,000 (10x in 4 years)</p>
            <p className="text-xs text-dark-400">Investment: ₹10,000 → ₹1,00,000</p>
          </div>
        </div>
        <p className="text-xs text-dark-400 mt-2">
          * Past performance doesn't guarantee future results. These are exceptional cases.
        </p>
      </div>
    </motion.div>
  )
}