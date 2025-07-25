#!/usr/bin/env python3

"""
Demo script for AI Speech-to-Speech Therapy Assistant
Showcases the sentiment analysis and therapeutic response capabilities
"""

import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.getcwd())

def print_banner():
    """Print demo banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🧠💬 AI Speech-to-Speech Therapy Assistant            ║
    ║                                                              ║
    ║              Interactive Demo & Showcase                     ║
    ║                                                              ║
    ║        🔍 Advanced NLP + 💙 Compassionate Responses          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def demo_sentiment_analysis():
    """Demonstrate sentiment analysis capabilities"""
    print("\n🔍 SENTIMENT ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    from app_simple import TherapyBot
    bot = TherapyBot()
    
    # Demo messages with different sentiments
    demo_messages = [
        {
            'text': "I just got promoted at work and I'm feeling amazing!",
            'expected': 'positive'
        },
        {
            'text': "I've been feeling really down and depressed lately.",
            'expected': 'sad'
        },
        {
            'text': "I'm so worried about my health and can't stop thinking about it.",
            'expected': 'anxious'
        },
        {
            'text': "Everything in my life is falling apart and I don't know what to do.",
            'expected': 'negative'
        },
        {
            'text': "I'm not really sure how I'm feeling today.",
            'expected': 'neutral'
        }
    ]
    
    for i, demo in enumerate(demo_messages, 1):
        print(f"\n📝 Example {i}: {demo['text']}")
        print("-" * 60)
        
        # Analyze sentiment
        analysis = bot.analyze_sentiment(demo['text'])
        
        print(f"🎯 Detected Sentiment: {analysis['primary_sentiment'].upper()}")
        print(f"📊 Confidence Score: {analysis['confidence']:.2f}")
        print(f"📈 TextBlob Polarity: {analysis['textblob']['polarity']:.2f}")
        print(f"📈 TextBlob Subjectivity: {analysis['textblob']['subjectivity']:.2f}")
        
        if analysis['transformer']:
            print(f"🤖 Transformer Result: {analysis['transformer']['label']} ({analysis['transformer']['score']:.2f})")
        
        # Generate therapeutic response
        response = bot.generate_response(demo['text'], analysis, f"demo_session_{i}")
        print(f"\n💙 Therapeutic Response:")
        print(f"   {response}")
        
        # Small delay for readability
        time.sleep(1)

def demo_session_tracking():
    """Demonstrate session tracking capabilities"""
    print("\n\n📊 SESSION TRACKING DEMONSTRATION")
    print("=" * 60)
    
    from app_simple import TherapyBot
    bot = TherapyBot()
    
    # Simulate a therapy session
    session_messages = [
        "I've been having trouble sleeping lately.",
        "Work has been really stressful and overwhelming.",
        "I think I'm starting to feel a bit better after talking.",
        "Thank you for listening and helping me process these feelings."
    ]
    
    session_id = "demo_therapy_session"
    
    for i, message in enumerate(session_messages, 1):
        print(f"\n💬 Message {i}: {message}")
        
        # Process message
        analysis = bot.analyze_sentiment(message)
        response = bot.generate_response(message, analysis, session_id)
        
        print(f"   🎯 Sentiment: {analysis['primary_sentiment']}")
        print(f"   🤖 Response: {response[:80]}...")
    
    # Show session summary
    session = bot.sessions[session_id]
    print(f"\n📈 Session Summary:")
    print(f"   📅 Total Messages: {len(session['messages'])}")
    print(f"   🎯 Sentiment Progression:")
    
    for i, sentiment_data in enumerate(session['sentiment_history'], 1):
        print(f"      {i}. {sentiment_data['sentiment']} (confidence: {sentiment_data['score']:.2f})")

def interactive_demo():
    """Interactive demo where user can input their own messages"""
    print("\n\n💬 INTERACTIVE THERAPY SESSION")
    print("=" * 60)
    print("You can now have a conversation with the AI therapy assistant!")
    print("Type your messages below (or 'quit' to exit):")
    print("-" * 60)
    
    from app_simple import TherapyBot
    bot = TherapyBot()
    session_id = "interactive_demo"
    
    while True:
        try:
            user_input = input("\n🗣️  You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n💙 Thank you for trying the AI Therapy Assistant!")
                print("Take care of yourself! 🌟")
                break
            
            if not user_input:
                continue
            
            # Process the message
            analysis = bot.analyze_sentiment(user_input)
            response = bot.generate_response(user_input, analysis, session_id)
            
            # Show analysis
            print(f"\n🔍 Analysis: {analysis['primary_sentiment']} (confidence: {analysis['confidence']:.2f})")
            print(f"🤖 AI Therapist: {response}")
            
        except KeyboardInterrupt:
            print("\n\n💙 Session ended. Take care! 🌟")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def main():
    """Main demo function"""
    print_banner()
    
    print("🌟 Welcome to the AI Speech-to-Speech Therapy Assistant Demo!")
    print("\nThis demo showcases:")
    print("   🔍 Advanced sentiment analysis using NLP")
    print("   💙 Compassionate therapeutic responses")
    print("   📊 Session tracking and analytics")
    print("   🤖 Real-time emotional intelligence")
    
    try:
        # Run demonstrations
        demo_sentiment_analysis()
        demo_session_tracking()
        
        # Ask if user wants interactive demo
        print("\n" + "=" * 60)
        choice = input("Would you like to try the interactive demo? (y/n): ").strip().lower()
        
        if choice in ['y', 'yes']:
            interactive_demo()
        
        print("\n" + "=" * 60)
        print("🎉 Demo completed! The AI Therapy Assistant is ready for use.")
        print("🚀 To start the web server, run: python app_simple.py")
        print("📱 Then open http://localhost:5000 in your browser")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()