import { NextRequest, NextResponse } from 'next/server'

const PYTHON_BACKEND_URL = process.env.NEXT_PUBLIC_PYTHON_BACKEND_URL || 'http://localhost:5000'

export async function GET(request: NextRequest) {
  try {
    const response = await fetch(`${PYTHON_BACKEND_URL}/api/system-status`, {
      method: 'GET',
      signal: AbortSignal.timeout(10000) // 10 seconds timeout
    })

    if (!response.ok) {
      return NextResponse.json(
        { 
          status: 'error',
          message: 'Failed to get system status',
          agents_active: 0
        },
        { status: response.status }
      )
    }

    const status = await response.json()
    return NextResponse.json(status)
    
  } catch (error: any) {
    console.error('Status check failed:', error)
    
    if (error.name === 'AbortError' || error.code === 'ECONNREFUSED') {
      return NextResponse.json({
        status: 'offline',
        message: 'Python AI system is not running',
        agents_active: 0,
        backend_running: false
      })
    }
    
    return NextResponse.json({
      status: 'error',
      message: `Status check failed: ${error.message}`,
      agents_active: 0
    })
  }
}