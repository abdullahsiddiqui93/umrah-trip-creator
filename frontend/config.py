"""
Configuration file for Streamlit frontend
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Configuration
APP_TITLE = "Umrah Trip Creator"
APP_ICON = "🕋"
APP_LAYOUT = "wide"

# Agent Models
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "anthropic.claude-sonnet-4-5-20250929-v1:0")
FLIGHT_AGENT_MODEL = os.getenv("FLIGHT_AGENT_MODEL", "gpt-4o-2024-08-06")
HOTEL_AGENT_MODEL = os.getenv("HOTEL_AGENT_MODEL", "anthropic.claude-sonnet-4-5-20250929-v1:0")
VISA_AGENT_MODEL = os.getenv("VISA_AGENT_MODEL", "gpt-4o-2024-08-06")
ITINERARY_AGENT_MODEL = os.getenv("ITINERARY_AGENT_MODEL", "anthropic.claude-sonnet-4-5-20250929-v1:0")

# API Keys
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY", "")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET", "")
BOOKING_API_KEY = os.getenv("BOOKING_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID", "")

# Deployment Configuration
STACK_PREFIX = os.getenv("STACK_PREFIX", "umrah-trip")
S3_BUCKET_PREFIX = os.getenv("S3_BUCKET_PREFIX", "umrah-trip-creator")

# UI Configuration
THEME = {
    "primaryColor": "#1e7e34",
    "backgroundColor": "#ffffff",
    "secondaryBackgroundColor": "#f0f2f6",
    "textColor": "#262730",
    "font": "sans serif"
}

# Supported Nationalities
NATIONALITIES = [
    "United States", "United Kingdom", "Canada", "Australia", 
    "India", "Pakistan", "Bangladesh", "Malaysia", "Indonesia",
    "Turkey", "Egypt", "Nigeria", "South Africa", "UAE",
    "Saudi Arabia", "Kuwait", "Qatar", "Bahrain", "Oman",
    "Jordan", "Lebanon", "Morocco", "Algeria", "Tunisia",
    "France", "Germany", "Italy", "Spain", "Netherlands",
    "Other"
]

# Hotel Amenities
HOTEL_AMENITIES = [
    "WiFi",
    "Breakfast Included",
    "Airport Shuttle",
    "Laundry Service",
    "Restaurant",
    "Elevator",
    "Prayer Facilities",
    "Zamzam Water",
    "24/7 Reception",
    "Room Service",
    "Air Conditioning",
    "Safe Deposit Box"
]

# Airlines
PREFERRED_AIRLINES = [
    "Saudi Airlines",
    "Emirates",
    "Qatar Airways",
    "Etihad Airways",
    "Turkish Airlines",
    "British Airways",
    "Lufthansa",
    "Air France",
    "KLM",
    "Any"
]

# Currencies
CURRENCIES = [
    "USD", "EUR", "GBP", "SAR", "AED", 
    "INR", "PKR", "MYR", "IDR", "TRY",
    "EGP", "ZAR", "CAD", "AUD"
]

# Validation Rules
MIN_TRIP_DURATION = 7  # days
MAX_TRIP_DURATION = 90  # days
MIN_ADVANCE_BOOKING = 30  # days
MAX_TRAVELERS = 20
MIN_BUDGET_PER_PERSON = 500  # USD equivalent
MAX_BUDGET_PER_PERSON = 50000  # USD equivalent

# Demo Mode
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"

# Feature Flags
ENABLE_REAL_TIME_PRICING = os.getenv("ENABLE_REAL_TIME_PRICING", "false").lower() == "true"
ENABLE_PAYMENT_PROCESSING = os.getenv("ENABLE_PAYMENT_PROCESSING", "false").lower() == "true"
ENABLE_EMAIL_NOTIFICATIONS = os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").lower() == "true"
