// AgentCore client for invoking agents

import { BedrockAgentRuntimeClient, InvokeAgentCommand } from '@aws-sdk/client-bedrock-agent-runtime';

const client = new BedrockAgentRuntimeClient({
  region: process.env.BEDROCK_REGION || 'us-west-2',
});

export async function invokeOrchestrator(userData: any): Promise<string> {
  const sessionId = crypto.randomUUID();
  
  // Format the prompt for the orchestrator
  const prompt = formatPromptForOrchestrator(userData);
  
  try {
    const command = new InvokeAgentCommand({
      agentId: process.env.ORCHESTRATOR_ARN!,
      agentAliasId: 'TSTALIASID',
      sessionId: sessionId,
      inputText: prompt,
    });
    
    const response = await client.send(command);
    
    // Parse the streaming response
    let fullResponse = '';
    
    if (response.completion) {
      for await (const event of response.completion) {
        if (event.chunk && event.chunk.bytes) {
          const chunk = new TextDecoder().decode(event.chunk.bytes);
          fullResponse += chunk;
        }
      }
    }
    
    return fullResponse;
  } catch (error) {
    console.error('Error invoking orchestrator:', error);
    throw new Error(`Failed to generate trip plan: ${error}`);
  }
}

function formatPromptForOrchestrator(userData: any): string {
  const { travel_dates, num_travelers, travelers, hotel_preferences, budget, special_requirements, flight_preferences } = userData;
  
  let prompt = `I need help planning an Umrah trip with the following details:\n\n`;
  
  // Travel dates
  prompt += `TRAVEL DATES:\n`;
  prompt += `- Departure from: ${travel_dates.departure_airport}\n`;
  prompt += `- Departure date: ${travel_dates.departure}\n`;
  prompt += `- Return date: ${travel_dates.return}\n`;
  prompt += `- Duration: ${travel_dates.duration} days\n`;
  prompt += `- Arrival city: ${travel_dates.arrival_city}\n\n`;
  
  // Travelers
  prompt += `TRAVELERS (${num_travelers} people):\n`;
  travelers.forEach((t: any, i: number) => {
    prompt += `${i + 1}. ${t.name} - ${t.nationality}, Age ${t.age}, ${t.gender}\n`;
  });
  prompt += `\n`;
  
  // Hotel preferences
  prompt += `HOTEL PREFERENCES:\n`;
  prompt += `- Makkah: ${hotel_preferences.makkah.star_rating}-star, ${hotel_preferences.makkah.proximity}\n`;
  prompt += `- Madinah: ${hotel_preferences.madinah.star_rating}-star, ${hotel_preferences.madinah.proximity}\n\n`;
  
  // Budget
  prompt += `BUDGET:\n`;
  prompt += `- Total budget: ${budget.currency} ${budget.total}\n`;
  prompt += `- Per person: ${budget.currency} ${budget.per_person}\n`;
  prompt += `- Flexibility: ${budget.flexibility}\n\n`;
  
  // Flight preferences
  prompt += `FLIGHT PREFERENCES:\n`;
  prompt += `- Cabin class: ${flight_preferences.cabin_class}\n`;
  prompt += `- Direct flights preferred: ${flight_preferences.direct_flights ? 'Yes' : 'No'}\n\n`;
  
  // Special requirements
  if (special_requirements.custom_itinerary) {
    prompt += `CUSTOM ITINERARY:\n${special_requirements.custom_itinerary}\n\n`;
  }
  
  if (special_requirements.additional_notes) {
    prompt += `ADDITIONAL NOTES:\n${special_requirements.additional_notes}\n\n`;
  }
  
  prompt += `Please provide:\n`;
  prompt += `1. Multiple flight options (2-3) with real prices\n`;
  prompt += `2. Multiple hotel options for both Makkah and Madinah (2-3 each)\n`;
  prompt += `3. Visa requirements\n`;
  prompt += `4. Detailed day-by-day itinerary\n`;
  prompt += `5. Total cost breakdown\n`;
  
  return prompt;
}
