import os
import json
import tempfile
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
import nltk
from transformers import pipeline
import threading
import time
from datetime import datetime
import logging

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TherapyBot:
    def __init__(self):
        # Initialize sentiment analysis pipeline
        try:
            self.sentiment_pipeline = pipeline("sentiment-analysis")
            logger.info("Sentiment analysis pipeline initialized")
        except Exception as e:
            logger.error(f"Error initializing sentiment pipeline: {e}")
            self.sentiment_pipeline = None
        
        # Session storage
        self.sessions = {}
        
        # Therapeutic response templates
        self.response_templates = {
            'positive': [
                "I'm so glad to hear that you're feeling positive! 😊 It's wonderful when we can find moments of joy and contentment. What specifically is contributing to these good feelings?",
                "That's fantastic! 🌟 Positive emotions are so important for our wellbeing. How can we help you maintain and build on these feelings?",
                "I can sense the positivity in your words, and it's truly uplifting! 💫 What strategies have been working well for you lately?"
            ],
            'negative': [
                "I hear that you're going through a difficult time, and I want you to know that your feelings are completely valid. 💙 Can you tell me more about what's been weighing on your mind?",
                "Thank you for sharing something so personal with me. It takes courage to express difficult emotions. 🤗 Let's work through this together - what would feel most helpful right now?",
                "I'm here to support you through this challenging moment. 🌙 Sometimes when we're struggling, it helps to break things down into smaller, manageable pieces. What feels like the most pressing concern?"
            ],
            'neutral': [
                "I appreciate you taking the time to share with me today. 🌸 Sometimes our emotions can feel complex or mixed. How are you feeling in this moment?",
                "Thank you for being here. It's okay if you're not sure exactly how you're feeling right now. 🍃 Let's explore what's on your mind together.",
                "I'm glad you're reaching out. Whether you're feeling good, bad, or somewhere in between, this is a safe space for you. 💚 What would you like to talk about?"
            ],
            'anxious': [
                "I can sense some anxiety in what you're sharing, and I want you to know that anxiety is a very common and treatable experience. 🌊 Let's try some grounding techniques - can you name 5 things you can see around you right now?",
                "Anxiety can feel overwhelming, but you're not alone in this. 🕊️ One helpful technique is deep breathing - try breathing in for 4 counts, holding for 4, and exhaling for 6. How does that feel?",
                "When anxiety strikes, remember that feelings are temporary, even when they feel intense. 🌈 What usually helps you feel more grounded and centered?"
            ],
            'sad': [
                "I can feel the sadness in your words, and I want you to know that it's okay to feel this way. 🌧️ Sadness is a natural human emotion, and acknowledging it is the first step toward healing. What's been making you feel this way?",
                "Your sadness is valid, and I'm here to listen without judgment. 💙 Sometimes talking through our feelings can help lighten the emotional load. Would you like to share what's been on your heart?",
                "It takes strength to reach out when you're feeling sad. 🌙 Remember that this feeling won't last forever, even though it might feel overwhelming right now. What small thing could bring you a moment of comfort today?"
            ]
        }

    def analyze_sentiment(self, text):
        """Analyze sentiment using multiple approaches"""
        results = {}
        
        # TextBlob analysis
        blob = TextBlob(text)
        results['textblob'] = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        
        # Transformers analysis
        if self.sentiment_pipeline:
            try:
                transformer_result = self.sentiment_pipeline(text)[0]
                results['transformer'] = transformer_result
            except Exception as e:
                logger.error(f"Error in transformer analysis: {e}")
                results['transformer'] = None
        
        # Determine overall sentiment
        sentiment_score = results['textblob']['polarity']
        
        if sentiment_score > 0.3:
            primary_sentiment = 'positive'
        elif sentiment_score < -0.3:
            primary_sentiment = 'negative'
        elif 'anxiety' in text.lower() or 'anxious' in text.lower() or 'worried' in text.lower():
            primary_sentiment = 'anxious'
        elif 'sad' in text.lower() or 'depressed' in text.lower() or 'down' in text.lower():
            primary_sentiment = 'sad'
        else:
            primary_sentiment = 'neutral'
        
        results['primary_sentiment'] = primary_sentiment
        results['confidence'] = abs(sentiment_score)
        
        return results

    def generate_response(self, text, sentiment_analysis, session_id=None):
        """Generate therapeutic response based on sentiment"""
        primary_sentiment = sentiment_analysis['primary_sentiment']
        
        # Get appropriate response template
        templates = self.response_templates.get(primary_sentiment, self.response_templates['neutral'])
        
        # Simple template selection (could be more sophisticated)
        import random
        response = random.choice(templates)
        
        # Add session tracking
        if session_id:
            if session_id not in self.sessions:
                self.sessions[session_id] = {
                    'start_time': datetime.now(),
                    'messages': [],
                    'sentiment_history': []
                }
            
            self.sessions[session_id]['messages'].append({
                'user_input': text,
                'bot_response': response,
                'sentiment': sentiment_analysis,
                'timestamp': datetime.now().isoformat()
            })
            
            self.sessions[session_id]['sentiment_history'].append({
                'sentiment': primary_sentiment,
                'score': sentiment_analysis['confidence'],
                'timestamp': datetime.now().isoformat()
            })
        
        return response

# Initialize the therapy bot
therapy_bot = TherapyBot()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Analyze sentiment
        sentiment_analysis = therapy_bot.analyze_sentiment(user_message)
        
        # Generate response
        bot_response = therapy_bot.generate_response(
            user_message, 
            sentiment_analysis, 
            session_id
        )
        
        return jsonify({
            'response': bot_response,
            'sentiment': sentiment_analysis,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get session history"""
    session = therapy_bot.sessions.get(session_id, {})
    return jsonify(session)

@app.route('/sessions', methods=['GET'])
def get_all_sessions():
    """Get all sessions (for analytics)"""
    return jsonify(therapy_bot.sessions)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'sentiment_pipeline_available': therapy_bot.sentiment_pipeline is not None
    })

if __name__ == '__main__':
    print("🧠💬 AI Speech-to-Speech Therapy Assistant")
    print("=" * 50)
    print("🌟 Compassionate AI-powered therapy support")
    print("🔍 Advanced sentiment analysis with NLP")
    print("💙 Safe space for emotional wellness")
    print("=" * 50)
    print("🚀 Starting server...")
    print("📱 Open http://localhost:5000 in your browser")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)