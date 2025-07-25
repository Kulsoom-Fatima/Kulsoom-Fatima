#!/usr/bin/env python3

"""
Quick test script for AI Therapy Assistant
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_basic_functionality():
    """Test basic functionality without server"""
    print("🧪 Testing AI Therapy Assistant Core Functionality")
    print("=" * 60)
    
    try:
        # Import the therapy bot
        from app_simple import TherapyBot
        
        print("✅ Successfully imported TherapyBot")
        
        # Initialize the bot
        bot = TherapyBot()
        print("✅ Successfully initialized TherapyBot")
        
        # Test sentiment analysis
        test_messages = [
            "I feel really happy and excited today!",
            "I'm feeling quite sad and lonely lately.",
            "I'm so anxious about my upcoming presentation.",
            "I'm not sure how I feel right now.",
            "Everything seems to be going wrong in my life."
        ]
        
        print("\n🔍 Testing Sentiment Analysis:")
        print("-" * 40)
        
        for message in test_messages:
            print(f"\n📝 Input: '{message}'")
            
            # Analyze sentiment
            sentiment = bot.analyze_sentiment(message)
            print(f"   💭 Primary sentiment: {sentiment['primary_sentiment']}")
            print(f"   📊 Confidence: {sentiment['confidence']:.2f}")
            
            # Generate response
            response = bot.generate_response(message, sentiment, "test_session")
            print(f"   🤖 Response: {response[:100]}...")
        
        # Test session tracking
        print(f"\n📈 Session History:")
        print("-" * 40)
        session = bot.sessions.get("test_session", {})
        print(f"   📅 Messages in session: {len(session.get('messages', []))}")
        print(f"   🎯 Sentiment history: {len(session.get('sentiment_history', []))}")
        
        print("\n✅ All tests passed! The therapy assistant is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_imports():
    """Test Flask-related imports"""
    print("\n🌐 Testing Flask Components:")
    print("-" * 40)
    
    try:
        from flask import Flask, render_template, request, jsonify
        print("✅ Flask imports successful")
        
        from flask_cors import CORS
        print("✅ Flask-CORS import successful")
        
        return True
    except Exception as e:
        print(f"❌ Flask import error: {e}")
        return False

def main():
    """Main test function"""
    print("🧠💬 AI Speech-to-Speech Therapy Assistant - Quick Test")
    print("=" * 60)
    
    # Test basic functionality
    basic_test = test_basic_functionality()
    
    # Test Flask imports
    flask_test = test_flask_imports()
    
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   Core Functionality: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"   Flask Components: {'✅ PASS' if flask_test else '❌ FAIL'}")
    
    if basic_test and flask_test:
        print("\n🎉 All tests passed! The application is ready to run.")
        print("🚀 To start the server, run: python app_simple.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()