#!/bin/bash

# Run Streamlit frontend for Umrah Trip Creator

echo "🕋 Starting Umrah Trip Creator Frontend..."
echo ""

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "Creating virtual environment..."
    cd ..
    uv venv
    cd frontend
fi

# Activate virtual environment and install dependencies
echo "Installing dependencies..."
source ../.venv/bin/activate
pip install -r requirements.txt

# Run Streamlit
echo ""
echo "🚀 Launching Streamlit app..."
echo "📱 Open your browser at: http://localhost:8501"
echo ""

streamlit run streamlit_app.py --server.port 8501 --server.address localhost
