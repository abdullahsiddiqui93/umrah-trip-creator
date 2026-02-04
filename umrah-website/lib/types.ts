// TypeScript type definitions for the Umrah Trip Creator

export interface TravelDates {
  departure_country: string;
  departure_airport: string;
  departure: string;
  return: string;
  duration: number;
  arrival_city: string;
  departure_city: string;
}

export interface Traveler {
  name: string;
  nationality: string;
  age: number;
  gender: string;
}

export interface HotelPreferences {
  makkah: {
    proximity: string;
    star_rating: number;
    haram_view: boolean;
    amenities: string[];
  };
  madinah: {
    proximity: string;
    star_rating: number;
    haram_view: boolean;
    amenities: string[];
  };
  room_type: string;
}

export interface Budget {
  currency: string;
  per_person: number;
  total: number;
  flexibility: string;
}

export interface FlightPreferences {
  cabin_class: string;
  direct_flights: boolean;
  preferred_airlines: string[];
  baggage_extra: boolean;
}

export interface SpecialRequirements {
  wheelchair_access: boolean;
  elderly_travelers: boolean;
  dietary_requirements: boolean;
  female_only_group: boolean;
  first_time_umrah: boolean;
  group_coordinator: boolean;
  additional_notes: string;
  custom_itinerary: string;
}

export interface TripRequest {
  travel_dates: TravelDates;
  num_travelers: number;
  travelers: Traveler[];
  hotel_preferences: HotelPreferences;
  budget: Budget;
  flight_preferences: FlightPreferences;
  special_requirements: SpecialRequirements;
}

export interface TripPlan {
  ai_response: string;
  user_data: TripRequest;
  generated_at: string;
}
