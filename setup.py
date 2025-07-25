#!/usr/bin/env python3
"""
Setup script for AI Speech-to-Speech Therapy Assistant
Handles installation, dependency management, and basic configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        AI Speech-to-Speech Therapy Assistant Setup          ║
    ║                                                              ║
    ║        🧠 Advanced NLP + 💬 Compassionate AI                 ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version.split()[0]} (Compatible)")

def install_system_dependencies():
    """Install system-level dependencies"""
    print("\n🔧 Checking system dependencies...")
    
    system = platform.system().lower()
    
    if system == "linux":
        print("📦 Installing Linux audio dependencies...")
        try:
            # Check if apt is available
            subprocess.run(["which", "apt"], check=True, capture_output=True)
            
            # Install audio dependencies
            subprocess.run([
                "sudo", "apt", "update"
            ], check=True)
            
            subprocess.run([
                "sudo", "apt", "install", "-y",
                "portaudio19-dev",
                "python3-pyaudio",
                "espeak",
                "espeak-data",
                "libespeak1",
                "libespeak-dev",
                "ffmpeg"
            ], check=True)
            
            print("✅ Linux dependencies installed successfully")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Could not install some system dependencies automatically")
            print("   Please install manually: portaudio19-dev, espeak, ffmpeg")
    
    elif system == "darwin":  # macOS
        print("📦 Installing macOS audio dependencies...")
        try:
            # Check if brew is available
            subprocess.run(["which", "brew"], check=True, capture_output=True)
            
            subprocess.run([
                "brew", "install", "portaudio", "espeak", "ffmpeg"
            ], check=True)
            
            print("✅ macOS dependencies installed successfully")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Homebrew not found or installation failed")
            print("   Please install manually: portaudio, espeak, ffmpeg")
    
    elif system == "windows":
        print("📦 Windows detected - most dependencies should work out of the box")
        print("   If you encounter audio issues, install Visual C++ Build Tools")
    
    else:
        print(f"⚠️  Unsupported system: {system}")
        print("   Manual dependency installation may be required")

def install_python_dependencies():
    """Install Python dependencies"""
    print("\n📚 Installing Python dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True)
        
        # Install requirements
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        
        print("✅ Python dependencies installed successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing Python dependencies: {e}")
        print("   Try running: pip install -r requirements.txt")
        sys.exit(1)

def download_nltk_data():
    """Download required NLTK data"""
    print("\n📥 Downloading NLTK data...")
    
    try:
        import nltk
        
        # Download required NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('stopwords', quiet=True)
        
        print("✅ NLTK data downloaded successfully")
        
    except ImportError:
        print("⚠️  NLTK not installed - will download data on first run")
    except Exception as e:
        print(f"⚠️  Error downloading NLTK data: {e}")
        print("   Data will be downloaded automatically on first run")

def test_installation():
    """Test if installation was successful"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import flask
        import speech_recognition
        import pyttsx3
        import textblob
        import transformers
        import torch
        import numpy
        import pandas
        import sklearn
        
        print("✅ All core dependencies imported successfully")
        
        # Test basic functionality
        from textblob import TextBlob
        test_text = "I feel happy today"
        blob = TextBlob(test_text)
        sentiment = blob.sentiment.polarity
        
        print(f"✅ Sentiment analysis test: '{test_text}' -> {sentiment:.2f}")
        
        # Test TTS engine
        import pyttsx3
        engine = pyttsx3.init()
        print("✅ Text-to-speech engine initialized")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_env_file():
    """Create environment file if it doesn't exist"""
    print("\n📝 Setting up environment configuration...")
    
    env_file = Path(".env")
    
    if not env_file.exists():
        env_content = """# AI Therapy Assistant Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=therapy-assistant-secret-key-change-in-production

# Optional: OpenAI API Key for enhanced responses
# OPENAI_API_KEY=your-api-key-here

# Optional: Custom model configurations
# SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
# TTS_RATE=150
# TTS_VOLUME=0.9
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Environment file created (.env)")
    else:
        print("✅ Environment file already exists")

def print_usage_instructions():
    """Print usage instructions"""
    instructions = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                        🎉 Setup Complete!                    ║
    ╠══════════════════════════════════════════════════════════════╣
    ║                                                              ║
    ║  To start the AI Therapy Assistant:                         ║
    ║                                                              ║
    ║    python app.py                                             ║
    ║                                                              ║
    ║  Then open your browser to: http://localhost:5000           ║
    ║                                                              ║
    ║  🎤 Make sure to allow microphone access for voice features ║
    ║  🔊 Check your speakers/headphones for audio responses      ║
    ║                                                              ║
    ║  For help and documentation, see README.md                  ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    
    📋 Quick Start Checklist:
    ✅ Python 3.8+ installed
    ✅ Dependencies installed  
    ✅ NLTK data downloaded
    ✅ Environment configured
    ✅ Ready to run!
    
    🆘 If you encounter issues:
    - Check microphone permissions in your browser
    - Ensure speakers/headphones are working
    - Review the README.md for troubleshooting
    - Check the console for error messages
    
    💡 Tips:
    - Use Chrome or Firefox for best compatibility
    - Speak clearly for better speech recognition
    - Try both voice and text input modes
    - Check the session summary for insights
    """
    print(instructions)

def main():
    """Main setup function"""
    print_banner()
    
    try:
        # Check Python version
        check_python_version()
        
        # Install system dependencies
        install_system_dependencies()
        
        # Install Python dependencies
        install_python_dependencies()
        
        # Download NLTK data
        download_nltk_data()
        
        # Create environment file
        create_env_file()
        
        # Test installation
        if test_installation():
            print("\n✅ Installation completed successfully!")
            print_usage_instructions()
        else:
            print("\n❌ Installation completed with warnings")
            print("   The application may still work, but some features might be limited")
            print("   Check the error messages above and install missing dependencies")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        print("   Please check the error message and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()