'use client'

import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  Users, 
  BarChart3, 
  DollarSign, 
  Building, 
  Banknote,
  FileText,
  PieChart,
  Globe,
  Brain
} from 'lucide-react'

interface AgentGridProps {
  systemStatus: string
}

const agents = [
  {
    id: 1,
    name: 'Fundamental Agent',
    status: 'Active',
    icon: TrendingUp,
    description: 'Analyzes 10-year financial data for inflection signals',
    metrics: ['Revenue CAGR', 'PAT Growth', 'ROCE/ROE', 'Cash Flow'],
    color: 'from-blue-500 to-blue-600'
  },
  {
    id: 2,
    name: 'Management Agent',
    status: 'Active',
    icon: Users,
    description: 'Evaluates promoter quality and governance changes',
    metrics: ['Promoter Holding', 'PE Entry', 'Governance Score'],
    color: 'from-purple-500 to-purple-600'
  },
  {
    id: 3,
    name: 'Technical Agent',
    status: 'Active',
    icon: BarChart3,
    description: 'Identifies base formations and breakout patterns',
    metrics: ['Price Stage', 'Relative Strength', 'Volume Profile'],
    color: 'from-green-500 to-green-600'
  },
  {
    id: 4,
    name: 'Smart Money Agent',
    status: 'Active',
    icon: DollarSign,
    description: 'Tracks institutional flows and smart money signals',
    metrics: ['FII Flow', 'DII Activity', 'Bulk Deals'],
    color: 'from-yellow-500 to-yellow-600'
  },
  {
    id: 5,
    name: 'Policy Agent',
    status: 'Active',
    icon: Building,
    description: 'Maps government policies to sector beneficiaries',
    metrics: ['PLI Schemes', 'Budget Allocation', 'Regulatory Changes'],
    color: 'from-indigo-500 to-indigo-600'
  },
  {
    id: 6,
    name: 'RBI & Macro Agent',
    status: 'Active',
    icon: Banknote,
    description: 'Analyzes monetary cycles and liquidity conditions',
    metrics: ['Rate Cycle', 'Credit Growth', 'Liquidity'],
    color: 'from-red-500 to-red-600'
  },
  {
    id: 7,
    name: 'Earnings Agent',
    status: 'Active',
    icon: FileText,
    description: 'Monitors quarterly results and guidance upgrades',
    metrics: ['Earnings Ratio', 'Margin Trends', 'Order Book'],
    color: 'from-teal-500 to-teal-600'
  },
  {
    id: 8,
    name: 'Global Demand Agent',
    status: 'Active',
    icon: Globe,
    description: 'Tracks geopolitics and global demand patterns',
    metrics: ['China+1', 'Export Demand', 'Trade Routes'],
    color: 'from-orange-500 to-orange-600'
  },
  {
    id: 9,
    name: 'Synthesis Agent',
    status: 'Supervising',
    icon: Brain,
    description: 'Aggregates all agent outputs with weighted scoring to conclude final multibagger candidates',
    metrics: ['Scoring Weights', 'Final Ranking', 'Risk Assessment'],
    color: 'from-emerald-500 to-emerald-600'
  }
]

export default function AgentGrid({ systemStatus }: AgentGridProps) {
  const isActive = systemStatus === 'active'

  return (
    <div className="mb-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">Research Agents</h2>
        <div className="text-sm text-dark-400">
          {isActive ? '9 agents • Real-time analysis' : 'Initializing...'}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent, index) => {
          const Icon = agent.icon
          
          return (
            <motion.div
              key={agent.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="agent-card group"
            >
              <div className="flex items-start justify-between mb-4">
                <div className={`p-3 rounded-lg bg-gradient-to-r ${agent.color}`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex items-center space-x-2">
                  <div className={`status-indicator ${isActive ? 'status-active' : 'status-inactive'}`}></div>
                  <span className="text-xs text-dark-400">{isActive ? agent.status : 'Inactive'}</span>
                </div>
              </div>

              <h3 className="text-lg font-semibold mb-2 group-hover:text-primary-400 transition-colors">
                {agent.name}
              </h3>
              
              <p className="text-sm text-dark-300 mb-4 leading-relaxed">
                {agent.description}
              </p>

              <div className="space-y-2">
                {agent.metrics.map((metric, idx) => (
                  <div key={idx} className="flex items-center space-x-2">
                    <div className="w-1 h-1 bg-primary-500 rounded-full"></div>
                    <span className="text-xs text-dark-400">{metric}</span>
                  </div>
                ))}
              </div>

              {agent.id === 9 && (
                <div className="mt-4 pt-4 border-t border-dark-700">
                  <div className="text-xs text-primary-400 font-medium">SUPERVISING</div>
                  <div className="mt-2 space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="text-dark-400">Fundamentals</span>
                      <span className="text-primary-400">35%</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-dark-400">Policy & Macro</span>
                      <span className="text-primary-400">20%</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-dark-400">Management</span>
                      <span className="text-primary-400">15%</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-dark-400">Smart Money</span>
                      <span className="text-primary-400">15%</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-dark-400">Technicals</span>
                      <span className="text-primary-400">15%</span>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}