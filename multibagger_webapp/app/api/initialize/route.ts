import { NextRequest, NextResponse } from 'next/server'

const PYTHON_BACKEND_URL = process.env.NEXT_PUBLIC_PYTHON_BACKEND_URL || 'http://localhost:5000'

export async function POST(request: NextRequest) {
  try {
    console.log('🚀 Initializing Multi-Agent AI System...')
    
    const response = await fetch(`${PYTHON_BACKEND_URL}/api/initialize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      signal: AbortSignal.timeout(30000) // 30 seconds timeout
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      console.error('System initialization failed:', errorData)
      
      return NextResponse.json(
        { error: errorData.message || 'System initialization failed' },
        { status: response.status }
      )
    }

    const results = await response.json()
    console.log('✅ Multi-Agent AI System initialized successfully')
    
    return NextResponse.json(results)
    
  } catch (error: any) {
    console.error('Initialization request failed:', error)
    
    if (error.name === 'AbortError' || error.code === 'ECONNREFUSED') {
      return NextResponse.json(
        { 
          error: 'Python AI system is not running',
          details: 'Please start the Python backend: cd multibagger_webapp/python_bridge && python server.py'
        },
        { status: 503 }
      )
    }
    
    return NextResponse.json(
      { error: `Initialization failed: ${error.message}` },
      { status: 500 }
    )
  }
}