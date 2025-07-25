#!/bin/bash

# AI Speech-to-Speech Therapy Assistant Startup Script

echo "🧠💬 AI Speech-to-Speech Therapy Assistant"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "therapy_env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup first: python3 setup.py"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source therapy_env/bin/activate

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python -c "import flask, textblob, transformers, torch" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependencies not properly installed!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencies verified"
echo ""

# Ask user which mode to run
echo "Select mode:"
echo "1) 🌐 Web Server (Full UI)"
echo "2) 🧪 Demo Mode"
echo "3) ⚡ Quick Test"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Starting web server..."
        echo "📱 Open http://localhost:5000 in your browser"
        echo "Press Ctrl+C to stop"
        echo ""
        python app_simple.py
        ;;
    2)
        echo ""
        echo "🧪 Running demo..."
        python demo.py
        ;;
    3)
        echo ""
        echo "⚡ Running quick test..."
        python quick_test.py
        ;;
    *)
        echo "❌ Invalid choice. Please run again."
        exit 1
        ;;
esac