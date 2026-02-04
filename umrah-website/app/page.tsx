'use client';

import { useState } from 'react';
import { TripRequest } from '@/lib/types';

export default function Home() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [tripData, setTripData] = useState<Partial<TripRequest>>({});
  const [tripPlan, setTripPlan] = useState<any>(null);

  const steps = [
    'Travel Dates',
    'Traveler Details',
    'Hotel Preferences',
    'Budget & Requirements',
    'Review & Generate',
    'Trip Options'
  ];

  const handleGenerateTrip = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/generate-trip', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tripData),
      });

      const result = await response.json();

      if (result.success) {
        setTripPlan(result.data);
        setStep(6);
      } else {
        alert('Error generating trip: ' + result.error);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate trip plan');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-4xl font-bold text-green-700 text-center">
            🕋 Umrah Trip Creator
          </h1>
          <p className="text-center text-gray-600 mt-2">
            Plan your blessed journey with AI-powered assistance
          </p>
        </div>
      </header>

      {/* Progress Bar */}
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="flex justify-between items-center">
            {steps.map((stepName, index) => (
              <div key={index} className="flex items-center">
                <div className="flex flex-col items-center">
                  <div
                    className={`step-indicator ${
                      index + 1 === step
                        ? 'active'
                        : index + 1 < step
                        ? 'completed'
                        : ''
                    }`}
                  >
                    {index + 1}
                  </div>
                  <span className="text-sm mt-2 text-center max-w-[100px]">
                    {stepName}
                  </span>
                </div>
                {index < steps.length - 1 && (
                  <div
                    className={`h-1 w-16 mx-2 ${
                      index + 1 < step ? 'bg-green-700' : 'bg-gray-300'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          {step === 1 && (
            <div>
              <h2 className="text-2xl font-bold text-green-700 mb-6">
                📅 Step 1: Travel Dates
              </h2>
              <p className="text-gray-600 mb-8">
                This is a simplified demo. In production, you would have full forms here.
              </p>
              <button
                onClick={() => {
                  setTripData({
                    ...tripData,
                    travel_dates: {
                      departure_country: 'United Kingdom',
                      departure_airport: 'Manchester (MAN)',
                      departure: '2026-03-15',
                      return: '2026-03-22',
                      duration: 7,
                      arrival_city: 'Jeddah (JED)',
                      departure_city: 'Jeddah (JED)',
                    },
                  });
                  setStep(2);
                }}
                className="btn-primary"
              >
                Next: Traveler Details →
              </button>
            </div>
          )}

          {step === 2 && (
            <div>
              <h2 className="text-2xl font-bold text-green-700 mb-6">
                👥 Step 2: Traveler Details
              </h2>
              <button
                onClick={() => {
                  setTripData({
                    ...tripData,
                    num_travelers: 2,
                    travelers: [
                      {
                        name: 'John Doe',
                        nationality: 'United Kingdom',
                        age: 35,
                        gender: 'Male',
                      },
                      {
                        name: 'Jane Doe',
                        nationality: 'United Kingdom',
                        age: 32,
                        gender: 'Female',
                      },
                    ],
                  });
                  setStep(3);
                }}
                className="btn-primary mr-4"
              >
                Next: Hotel Preferences →
              </button>
              <button
                onClick={() => setStep(1)}
                className="px-6 py-3 bg-gray-300 rounded-lg"
              >
                ← Back
              </button>
            </div>
          )}

          {step === 3 && (
            <div>
              <h2 className="text-2xl font-bold text-green-700 mb-6">
                🏨 Step 3: Hotel Preferences
              </h2>
              <button
                onClick={() => {
                  setTripData({
                    ...tripData,
                    hotel_preferences: {
                      makkah: {
                        proximity: 'Walking Distance (<500m)',
                        star_rating: 4,
                        haram_view: false,
                        amenities: ['WiFi', 'Breakfast'],
                      },
                      madinah: {
                        proximity: 'Walking Distance (<500m)',
                        star_rating: 4,
                        haram_view: false,
                        amenities: ['WiFi', 'Breakfast'],
                      },
                      room_type: 'Double',
                    },
                  });
                  setStep(4);
                }}
                className="btn-primary mr-4"
              >
                Next: Budget →
              </button>
              <button
                onClick={() => setStep(2)}
                className="px-6 py-3 bg-gray-300 rounded-lg"
              >
                ← Back
              </button>
            </div>
          )}

          {step === 4 && (
            <div>
              <h2 className="text-2xl font-bold text-green-700 mb-6">
                💰 Step 4: Budget & Requirements
              </h2>
              <button
                onClick={() => {
                  setTripData({
                    ...tripData,
                    budget: {
                      currency: 'USD',
                      per_person: 3000,
                      total: 6000,
                      flexibility: 'Moderate',
                    },
                    special_requirements: {
                      wheelchair_access: false,
                      elderly_travelers: false,
                      dietary_requirements: false,
                      female_only_group: false,
                      first_time_umrah: true,
                      group_coordinator: false,
                      additional_notes: '',
                      custom_itinerary: '',
                    },
                    flight_preferences: {
                      cabin_class: 'Economy',
                      direct_flights: false,
                      preferred_airlines: [],
                      baggage_extra: false,
                    },
                  });
                  setStep(5);
                }}
                className="btn-primary mr-4"
              >
                Next: Review →
              </button>
              <button
                onClick={() => setStep(3)}
                className="px-6 py-3 bg-gray-300 rounded-lg"
              >
                ← Back
              </button>
            </div>
          )}

          {step === 5 && (
            <div>
              <h2 className="text-2xl font-bold text-green-700 mb-6">
                📋 Step 5: Review & Generate Plan
              </h2>
              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
                <p className="text-blue-700">
                  🤖 <strong>AI-Powered Planning:</strong> Our agents will search
                  real-time data and create a personalized Umrah plan for you.
                </p>
              </div>
              <button
                onClick={handleGenerateTrip}
                disabled={loading}
                className="btn-primary mr-4"
              >
                {loading ? '⏳ Generating...' : '🚀 Generate My Umrah Trip Plan'}
              </button>
              <button
                onClick={() => setStep(4)}
                className="px-6 py-3 bg-gray-300 rounded-lg"
                disabled={loading}
              >
                ← Back
              </button>
            </div>
          )}

          {step === 6 && tripPlan && (
            <div>
              <h2 className="text-2xl font-bold text-green-700 mb-6">
                ✨ Your Umrah Trip Plan
              </h2>
              <div className="bg-green-50 border-l-4 border-green-500 p-4 mb-6">
                <p className="text-green-700">
                  ✅ <strong>Trip plan generated successfully!</strong>
                </p>
              </div>
              <div className="bg-white border rounded-lg p-6 mb-6">
                <h3 className="text-xl font-bold mb-4">AI Response:</h3>
                <pre className="whitespace-pre-wrap text-sm bg-gray-50 p-4 rounded">
                  {tripPlan.ai_response}
                </pre>
              </div>
              <button
                onClick={() => {
                  setStep(1);
                  setTripPlan(null);
                  setTripData({});
                }}
                className="btn-primary"
              >
                🔄 Start Over
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white shadow-md mt-12">
        <div className="container mx-auto px-4 py-6 text-center text-gray-600">
          <p>© 2026 Umrah Trip Creator. Powered by AWS Bedrock AgentCore.</p>
        </div>
      </footer>
    </div>
  );
}
