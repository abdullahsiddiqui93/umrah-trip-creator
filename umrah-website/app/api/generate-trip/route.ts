import { NextRequest, NextResponse } from 'next/server';
import { invokeOrchestrator } from '@/lib/agentcore';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    console.log('Generating trip plan for:', body);
    
    // Invoke the orchestrator agent
    const aiResponse = await invokeOrchestrator(body);
    
    console.log('AI Response received');
    
    // Parse the response (you can add more sophisticated parsing here)
    const tripPlan = {
      ai_response: aiResponse,
      user_data: body,
      generated_at: new Date().toISOString(),
    };
    
    return NextResponse.json({
      success: true,
      data: tripPlan,
    });
    
  } catch (error: any) {
    console.error('Error generating trip:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: error.message || 'Failed to generate trip plan',
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Trip generation API',
    status: 'healthy',
  });
}
