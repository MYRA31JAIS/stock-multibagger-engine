import { NextRequest, NextResponse } from 'next/server'

const PYTHON_BACKEND_URL = process.env.NEXT_PUBLIC_PYTHON_BACKEND_URL || 'http://localhost:5000'

export async function POST(request: NextRequest) {
  try {
    const { stocks } = await request.json()
    
    if (!stocks || stocks.length === 0) {
      return NextResponse.json(
        { error: 'No stocks provided for analysis' },
        { status: 400 }
      )
    }

    console.log(`🔍 Analyzing stocks: ${stocks.join(', ')}`)
    
    // Call the Python Multi-Agent backend
    const response = await fetch(`${PYTHON_BACKEND_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ stocks }),
      // Increase timeout for AI analysis
      signal: AbortSignal.timeout(120000) // 2 minutes
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
      console.error('Python backend error:', errorData)
      
      return NextResponse.json(
        { error: errorData.error || 'Analysis failed' },
        { status: response.status }
      )
    }

    const results = await response.json()
    console.log(`✅ Analysis completed: ${results.analysis_summary?.high_conviction_count || 0} high conviction stocks found`)
    
    return NextResponse.json(results)
    
  } catch (error: any) {
    console.error('Analysis request failed:', error)
    
    // Check if it's a timeout or connection error
    if (error.name === 'AbortError' || error.code === 'ECONNREFUSED') {
      return NextResponse.json(
        { 
          error: 'Python AI system is not running. Please start the backend server.',
          details: 'Run: cd multibagger_webapp/python_bridge && python server.py'
        },
        { status: 503 }
      )
    }
    
    return NextResponse.json(
      { error: `Analysis failed: ${error.message}` },
      { status: 500 }
    )
  }
}