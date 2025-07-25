import os
import json
import tempfile
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
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
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Initialize sentiment analyzer
        try:
            self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                             model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        except:
            logger.warning("Could not load advanced sentiment model, falling back to TextBlob")
            self.sentiment_analyzer = None
        
        # Therapy response templates based on sentiment
        self.therapy_responses = {
            'positive': [
                "I'm so glad to hear that you're feeling positive! It's wonderful when we can recognize and appreciate the good moments in our lives. What specifically is contributing to these positive feelings?",
                "That sounds really encouraging! Positive emotions are so important for our wellbeing. How can we help you maintain and build on these feelings?",
                "It's beautiful to hear the joy in your words. These positive moments are precious - what would you like to explore about this experience?"
            ],
            'negative': [
                "I hear that you're going through a difficult time, and I want you to know that your feelings are completely valid. It takes courage to share when we're struggling. Can you tell me more about what's weighing on your heart?",
                "Thank you for trusting me with these difficult emotions. Sometimes just expressing how we feel can be the first step toward healing. What feels most challenging for you right now?",
                "I can sense the pain in your words, and I'm here to support you through this. Remember that difficult emotions are temporary, even when they feel overwhelming. What would feel most helpful to talk about today?"
            ],
            'neutral': [
                "I appreciate you sharing with me today. Sometimes our emotions can feel complex or mixed. How are you really feeling beneath the surface?",
                "It's okay to feel uncertain or in-between sometimes. That's part of being human. What's on your mind that you'd like to explore together?",
                "Thank you for being here. Sometimes the most important conversations start with simply checking in with ourselves. What would you like to focus on today?"
            ],
            'anxiety': [
                "I can hear some worry in your voice, and that's completely understandable. Anxiety can feel overwhelming, but you're not alone in this. Let's take a moment to breathe together. What's been causing you the most concern?",
                "Anxiety can make everything feel more intense and uncertain. You're brave for reaching out. What thoughts have been cycling through your mind lately?",
                "I recognize that anxious feeling you're describing. It's your mind trying to protect you, but sometimes it can feel like too much. What would help you feel more grounded right now?"
            ],
            'sadness': [
                "I can feel the heaviness in your words, and I want you to know that it's okay to feel sad. Sadness is a natural response to loss, disappointment, or change. What's been weighing on your heart?",
                "Your sadness is valid and important. Sometimes we need to sit with these feelings to understand what they're telling us. What do you think your sadness is trying to communicate?",
                "I'm here with you in this difficult moment. Sadness can feel isolating, but you don't have to carry this alone. What would feel most supportive right now?"
            ]
        }
        
        # Session tracking
        self.session_data = {
            'start_time': datetime.now(),
            'interactions': [],
            'sentiment_history': []
        }

    def analyze_sentiment(self, text):
        """Analyze sentiment of the input text"""
        try:
            if self.sentiment_analyzer:
                # Use transformer model
                result = self.sentiment_analyzer(text)[0]
                label = result['label'].lower()
                confidence = result['score']
                
                # Map labels to our categories
                if 'positive' in label:
                    sentiment = 'positive'
                elif 'negative' in label:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
            else:
                # Fallback to TextBlob
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity
                
                if polarity > 0.1:
                    sentiment = 'positive'
                    confidence = polarity
                elif polarity < -0.1:
                    sentiment = 'negative'
                    confidence = abs(polarity)
                else:
                    sentiment = 'neutral'
                    confidence = 1 - abs(polarity)
            
            # Detect specific emotions
            text_lower = text.lower()
            if any(word in text_lower for word in ['anxious', 'worried', 'nervous', 'panic', 'stress']):
                sentiment = 'anxiety'
            elif any(word in text_lower for word in ['sad', 'depressed', 'down', 'hopeless', 'grief']):
                sentiment = 'sadness'
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'text': text
            }
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'text': text
            }

    def generate_therapeutic_response(self, sentiment_data):
        """Generate appropriate therapeutic response based on sentiment"""
        sentiment = sentiment_data['sentiment']
        user_text = sentiment_data['text']
        
        # Get base response template
        if sentiment in self.therapy_responses:
            import random
            base_response = random.choice(self.therapy_responses[sentiment])
        else:
            base_response = random.choice(self.therapy_responses['neutral'])
        
        # Add personalized elements based on user input
        response = self.personalize_response(base_response, user_text, sentiment)
        
        return response

    def personalize_response(self, base_response, user_text, sentiment):
        """Add personalization to the therapeutic response"""
        # Extract key themes from user input
        blob = TextBlob(user_text)
        key_words = [word for word in blob.words if len(word) > 3]
        
        # Add reflective listening elements
        if len(key_words) > 0:
            reflection = f" I notice you mentioned {', '.join(key_words[:2])}."
            base_response += reflection
        
        # Add coping strategies based on sentiment
        if sentiment == 'anxiety':
            base_response += " Remember, you can try taking slow, deep breaths or grounding yourself by naming 5 things you can see around you."
        elif sentiment == 'sadness':
            base_response += " It's important to be gentle with yourself during this time. Small acts of self-care can make a difference."
        elif sentiment == 'positive':
            base_response += " These positive feelings are worth celebrating and remembering for times when things feel more difficult."
        
        return base_response

    def speech_to_text(self, audio_file_path):
        """Convert speech to text"""
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.UnknownValueError:
            return "I couldn't understand the audio. Could you please try again?"
        except sr.RequestError as e:
            return f"Error with speech recognition service: {e}"
        except Exception as e:
            logger.error(f"Error in speech to text: {e}")
            return "There was an error processing your audio."

    def text_to_speech(self, text):
        """Convert text to speech and return audio file path"""
        try:
            # Create temporary file for audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_file.close()
            
            # Configure and save speech
            self.tts_engine.save_to_file(text, temp_file.name)
            self.tts_engine.runAndWait()
            
            return temp_file.name
        except Exception as e:
            logger.error(f"Error in text to speech: {e}")
            return None

    def log_interaction(self, user_input, sentiment_data, bot_response):
        """Log the interaction for session tracking"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input,
            'sentiment': sentiment_data,
            'bot_response': bot_response
        }
        self.session_data['interactions'].append(interaction)
        self.session_data['sentiment_history'].append(sentiment_data['sentiment'])

# Initialize the therapy bot
therapy_bot = TherapyBot()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/process_audio', methods=['POST'])
def process_audio():
    """Process uploaded audio file"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Save uploaded file temporarily
        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio_file.save(temp_input.name)
        temp_input.close()
        
        # Convert speech to text
        user_text = therapy_bot.speech_to_text(temp_input.name)
        
        # Clean up input file
        os.unlink(temp_input.name)
        
        if "couldn't understand" in user_text or "Error" in user_text:
            return jsonify({'error': user_text}), 400
        
        # Analyze sentiment
        sentiment_data = therapy_bot.analyze_sentiment(user_text)
        
        # Generate therapeutic response
        bot_response = therapy_bot.generate_therapeutic_response(sentiment_data)
        
        # Convert response to speech
        audio_file_path = therapy_bot.text_to_speech(bot_response)
        
        # Log interaction
        therapy_bot.log_interaction(user_text, sentiment_data, bot_response)
        
        response_data = {
            'user_text': user_text,
            'sentiment': sentiment_data,
            'bot_response': bot_response,
            'audio_available': audio_file_path is not None
        }
        
        if audio_file_path:
            # Store audio file path in session or cache for retrieval
            response_data['audio_id'] = os.path.basename(audio_file_path)
            
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

@app.route('/process_text', methods=['POST'])
def process_text():
    """Process text input"""
    try:
        data = request.get_json()
        user_text = data.get('text', '')
        
        if not user_text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze sentiment
        sentiment_data = therapy_bot.analyze_sentiment(user_text)
        
        # Generate therapeutic response
        bot_response = therapy_bot.generate_therapeutic_response(sentiment_data)
        
        # Convert response to speech
        audio_file_path = therapy_bot.text_to_speech(bot_response)
        
        # Log interaction
        therapy_bot.log_interaction(user_text, sentiment_data, bot_response)
        
        response_data = {
            'user_text': user_text,
            'sentiment': sentiment_data,
            'bot_response': bot_response,
            'audio_available': audio_file_path is not None
        }
        
        if audio_file_path:
            response_data['audio_id'] = os.path.basename(audio_file_path)
            
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        return jsonify({'error': 'An error occurred processing your request'}), 500

@app.route('/get_audio/<audio_id>')
def get_audio(audio_id):
    """Serve generated audio file"""
    try:
        # Construct file path (in production, use proper file management)
        audio_path = os.path.join(tempfile.gettempdir(), audio_id)
        
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/wav')
        else:
            return jsonify({'error': 'Audio file not found'}), 404
            
    except Exception as e:
        logger.error(f"Error serving audio: {e}")
        return jsonify({'error': 'Error retrieving audio'}), 500

@app.route('/session_summary')
def session_summary():
    """Get session summary with sentiment analysis"""
    try:
        summary = {
            'session_duration': str(datetime.now() - therapy_bot.session_data['start_time']),
            'total_interactions': len(therapy_bot.session_data['interactions']),
            'sentiment_distribution': {},
            'recent_interactions': therapy_bot.session_data['interactions'][-5:]  # Last 5 interactions
        }
        
        # Calculate sentiment distribution
        sentiments = therapy_bot.session_data['sentiment_history']
        for sentiment in set(sentiments):
            summary['sentiment_distribution'][sentiment] = sentiments.count(sentiment)
        
        return jsonify(summary)
        
    except Exception as e:
        logger.error(f"Error generating session summary: {e}")
        return jsonify({'error': 'Error generating session summary'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)