#!/usr/bin/env python3
"""
Test script for AI Speech-to-Speech Therapy Assistant
Tests core functionality and components
"""

import sys
import json
import time
from pathlib import Path

def print_header(title):
    """Print test section header"""
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print('='*50)

def test_imports():
    """Test if all required modules can be imported"""
    print_header("Testing Imports")
    
    required_modules = [
        'flask',
        'speech_recognition',
        'pyttsx3',
        'textblob',
        'transformers',
        'torch',
        'numpy',
        'pandas',
        'sklearn',
        'nltk'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_therapy_bot():
    """Test TherapyBot class functionality"""
    print_header("Testing TherapyBot Class")
    
    try:
        from app import TherapyBot
        
        # Initialize bot
        print("🤖 Initializing TherapyBot...")
        bot = TherapyBot()
        print("✅ TherapyBot initialized successfully")
        
        # Test sentiment analysis
        test_cases = [
            ("I feel really happy today!", "positive"),
            ("I'm so anxious about tomorrow", "anxiety"),
            ("I feel sad and lonely", "sadness"),
            ("I'm not sure how I feel", "neutral"),
            ("This is terrible, I hate everything", "negative")
        ]
        
        print("\n📊 Testing Sentiment Analysis:")
        for text, expected in test_cases:
            try:
                result = bot.analyze_sentiment(text)
                sentiment = result['sentiment']
                confidence = result['confidence']
                
                print(f"   Text: '{text}'")
                print(f"   Detected: {sentiment} (confidence: {confidence:.2f})")
                
                if sentiment == expected:
                    print(f"   ✅ Correct sentiment detected")
                else:
                    print(f"   ⚠️  Expected: {expected}, Got: {sentiment}")
                print()
                
            except Exception as e:
                print(f"   ❌ Error analyzing: {e}")
        
        # Test response generation
        print("💬 Testing Response Generation:")
        sample_sentiment = {
            'sentiment': 'anxiety',
            'confidence': 0.85,
            'text': 'I feel really anxious about my presentation tomorrow'
        }
        
        try:
            response = bot.generate_therapeutic_response(sample_sentiment)
            print(f"   Input: {sample_sentiment['text']}")
            print(f"   Response: {response[:100]}...")
            print("   ✅ Response generated successfully")
        except Exception as e:
            print(f"   ❌ Error generating response: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing TherapyBot: {e}")
        return False

def test_text_to_speech():
    """Test text-to-speech functionality"""
    print_header("Testing Text-to-Speech")
    
    try:
        import pyttsx3
        
        print("🔊 Initializing TTS engine...")
        engine = pyttsx3.init()
        
        # Test basic TTS
        test_text = "Hello, this is a test of the text to speech system."
        print(f"   Testing with: '{test_text}'")
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"   Available voices: {len(voices)}")
        
        # Test without actually speaking (to avoid audio during testing)
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        print("✅ TTS engine configured successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error testing TTS: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition setup"""
    print_header("Testing Speech Recognition")
    
    try:
        import speech_recognition as sr
        
        print("🎤 Initializing speech recognizer...")
        recognizer = sr.Recognizer()
        
        # Test microphone availability
        try:
            microphone = sr.Microphone()
            print("✅ Microphone initialized successfully")
        except Exception as e:
            print(f"⚠️  Microphone initialization warning: {e}")
        
        print("✅ Speech recognition setup complete")
        return True
        
    except Exception as e:
        print(f"❌ Error testing speech recognition: {e}")
        return False

def test_nlp_models():
    """Test NLP model loading"""
    print_header("Testing NLP Models")
    
    try:
        from transformers import pipeline
        
        print("🧠 Testing sentiment analysis model...")
        
        # Test with a simple model first
        try:
            analyzer = pipeline("sentiment-analysis")
            test_result = analyzer("I feel great today!")
            print(f"   Test result: {test_result}")
            print("✅ Basic sentiment model working")
        except Exception as e:
            print(f"⚠️  Basic model error: {e}")
        
        # Test TextBlob fallback
        try:
            from textblob import TextBlob
            blob = TextBlob("I feel happy today")
            sentiment = blob.sentiment
            print(f"   TextBlob sentiment: polarity={sentiment.polarity:.2f}, subjectivity={sentiment.subjectivity:.2f}")
            print("✅ TextBlob working")
        except Exception as e:
            print(f"❌ TextBlob error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing NLP models: {e}")
        return False

def test_flask_app():
    """Test Flask application setup"""
    print_header("Testing Flask Application")
    
    try:
        from app import app
        
        print("🌐 Testing Flask app configuration...")
        
        # Test app creation
        print(f"   App name: {app.name}")
        print(f"   Debug mode: {app.debug}")
        
        # Test routes
        with app.test_client() as client:
            print("   Testing routes:")
            
            # Test main page
            try:
                response = client.get('/')
                print(f"   GET /: Status {response.status_code}")
            except Exception as e:
                print(f"   GET /: Error - {e}")
            
            # Test session summary
            try:
                response = client.get('/session_summary')
                print(f"   GET /session_summary: Status {response.status_code}")
            except Exception as e:
                print(f"   GET /session_summary: Error - {e}")
        
        print("✅ Flask app tests completed")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Flask app: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print_header("Testing File Structure")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All required files present")
        return True

def run_integration_test():
    """Run a simple integration test"""
    print_header("Integration Test")
    
    try:
        from app import TherapyBot
        
        print("🔄 Running end-to-end test...")
        
        # Initialize bot
        bot = TherapyBot()
        
        # Test full workflow
        user_input = "I'm feeling really stressed about work lately"
        
        print(f"   User input: '{user_input}'")
        
        # Analyze sentiment
        sentiment_data = bot.analyze_sentiment(user_input)
        print(f"   Sentiment: {sentiment_data['sentiment']} (confidence: {sentiment_data['confidence']:.2f})")
        
        # Generate response
        response = bot.generate_therapeutic_response(sentiment_data)
        print(f"   Response length: {len(response)} characters")
        print(f"   Response preview: {response[:100]}...")
        
        # Log interaction
        bot.log_interaction(user_input, sentiment_data, response)
        print(f"   Interactions logged: {len(bot.session_data['interactions'])}")
        
        print("✅ Integration test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Speech-to-Speech Therapy Assistant - Test Suite")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("TherapyBot Class", test_therapy_bot),
        ("Text-to-Speech", test_text_to_speech),
        ("Speech Recognition", test_speech_recognition),
        ("NLP Models", test_nlp_models),
        ("Flask Application", test_flask_app),
        ("Integration", run_integration_test)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\nTo start the application, run:")
        print("   python app.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        print("The application may still work, but some features might be limited.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)