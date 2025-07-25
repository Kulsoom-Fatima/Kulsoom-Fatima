# AI Speech-to-Speech Therapy Assistant 🧠💬

A compassionate AI-powered therapy assistant that uses Natural Language Processing (NLP) and Flask to provide personalized therapeutic responses based on user sentiment analysis. The application features complete speech-to-speech functionality, real-time emotion detection, and adaptive therapeutic interventions.

## 🌟 Features

### Core Functionality
- **Speech-to-Speech Interaction**: Complete voice-based therapy sessions
- **Real-time Sentiment Analysis**: Advanced NLP using Transformers and TextBlob
- **Adaptive Therapeutic Responses**: Personalized responses based on detected emotions
- **Session Tracking**: Comprehensive analytics and progress monitoring
- **Multi-Modal Input**: Both voice and text input supported

### Sentiment Categories
- **Positive**: Celebration and reinforcement strategies
- **Negative**: Supportive interventions and coping mechanisms
- **Anxiety**: Grounding techniques and breathing exercises
- **Sadness**: Compassionate support and self-care guidance
- **Neutral**: Exploratory and check-in conversations

### Technical Features
- **Advanced NLP**: Uses Cardiff NLP RoBERTa model for sentiment analysis
- **Speech Recognition**: Google Speech Recognition API integration
- **Text-to-Speech**: Both server-side (pyttsx3) and client-side synthesis
- **Real-time Analytics**: Live sentiment tracking and session insights
- **Responsive Design**: Modern, accessible UI with calming aesthetics
- **Session Management**: Persistent conversation history and analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (recommended: Python 3.9-3.13)
- Modern web browser
- Internet connection (for downloading NLP models)

### Installation

1. **Install system dependencies** (Linux/Ubuntu):
```bash
sudo apt update
sudo apt install python3-dev portaudio19-dev espeak espeak-data libespeak1 libespeak-dev ffmpeg python3-venv
```

2. **Create virtual environment and install dependencies**:
```bash
python3 -m venv therapy_env
source therapy_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Test the installation**:
```bash
python quick_test.py
```

4. **Start the application**:
```bash
python app_simple.py
```

5. **Access the application**
Open your browser and navigate to `http://localhost:5000`

### Easy Startup Script

Use the provided startup script for easy launching:

```bash
chmod +x start.sh
./start.sh
```

This will give you options to:
- 🌐 Start the web server
- 🧪 Run the interactive demo  
- ⚡ Run quick tests

### Demo Mode

Try the interactive demo to see the sentiment analysis in action:

```bash
source therapy_env/bin/activate
python demo.py
```

## 🏗️ Architecture

### Backend Components
- **Flask Application** (`app.py`): Main server and API endpoints
- **TherapyBot Class**: Core therapy logic and NLP processing
- **Sentiment Analysis**: Multi-layered emotion detection
- **Audio Processing**: Speech-to-text and text-to-speech conversion
- **Session Management**: Interaction logging and analytics

### Frontend Components
- **Modern UI** (`templates/index.html`): Responsive therapy interface
- **Real-time Dashboard** (`static/css/style.css`): Sentiment visualization
- **Interactive JavaScript** (`static/js/app.js`): Voice recording and chat logic

### API Endpoints
- `GET /`: Main therapy interface
- `POST /process_audio`: Handle voice input
- `POST /process_text`: Handle text input
- `GET /get_audio/<audio_id>`: Serve generated audio responses
- `GET /session_summary`: Retrieve session analytics

## 🎯 Usage Guide

### Starting a Session
1. **Grant Microphone Permission**: Allow browser access to your microphone
2. **Choose Input Method**: Use voice recording or text input
3. **Begin Conversation**: Share your thoughts and feelings

### Voice Interaction
- **Click "Click to speak"** to start recording
- **Speak naturally** about your feelings or concerns
- **Click again** to stop recording and process your input
- **Listen** to the AI therapist's spoken response

### Text Interaction
- **Type your message** in the text area
- **Press Enter** or click send to submit
- **Read or listen** to the therapeutic response

### Session Features
- **Real-time Sentiment**: View your emotional state analysis
- **Coping Strategies**: Receive personalized techniques
- **Session Summary**: Access detailed analytics
- **Audio Playback**: Replay any response

## 🧠 NLP and Sentiment Analysis

### Sentiment Detection
The system uses a multi-layered approach:

1. **Primary Analysis**: Cardiff NLP RoBERTa model for advanced sentiment classification
2. **Fallback Analysis**: TextBlob for reliable sentiment scoring
3. **Keyword Detection**: Pattern matching for specific emotions (anxiety, sadness)
4. **Confidence Scoring**: Reliability metrics for each analysis

### Therapeutic Response Generation
- **Template-based Responses**: Curated therapeutic interventions
- **Personalization**: Reflection of user's specific language
- **Coping Strategy Integration**: Contextual self-help techniques
- **Professional Tone**: Empathetic and supportive communication

## 🎨 UI/UX Design

### Design Principles
- **Calming Aesthetics**: Soft gradients and soothing colors
- **Accessibility**: High contrast support and keyboard navigation
- **Responsive Layout**: Mobile-friendly design
- **Intuitive Interface**: Clear visual hierarchy and feedback

### Key Features
- **Animated Elements**: Smooth transitions and micro-interactions
- **Visual Feedback**: Recording indicators and loading states
- **Sentiment Visualization**: Real-time emotion tracking
- **Session Analytics**: Comprehensive progress charts

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for custom configurations:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

### Audio Settings
Modify audio quality in `app.py`:
```python
# TTS Configuration
self.tts_engine.setProperty('rate', 150)  # Speech rate
self.tts_engine.setProperty('volume', 0.9)  # Volume level
```

### Sentiment Model
Switch sentiment analysis models:
```python
# Use different model
self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                 model="your-preferred-model")
```

## 📊 Session Analytics

### Tracked Metrics
- **Session Duration**: Total conversation time
- **Interaction Count**: Number of exchanges
- **Sentiment Distribution**: Emotion frequency analysis
- **Conversation History**: Complete session transcript
- **Confidence Scores**: Analysis reliability metrics

### Data Visualization
- **Emotion Charts**: Visual sentiment distribution
- **Progress Tracking**: Session-over-session improvements
- **Interaction Timeline**: Chronological conversation flow

## 🔒 Privacy and Ethics

### Data Handling
- **Local Processing**: All analysis performed on your device
- **No Data Storage**: Conversations are not permanently saved
- **Session-only Memory**: Data cleared when session ends
- **No External Sharing**: Your conversations remain private

### Ethical Considerations
- **Not a Replacement**: This tool supplements, not replaces, professional therapy
- **Crisis Support**: Includes resources for emergency situations
- **Informed Consent**: Clear communication about AI limitations
- **Professional Referrals**: Encourages seeking human support when needed

## 🛠️ Development

### Project Structure
```
ai-therapy-assistant/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main UI template
├── static/
│   ├── css/
│   │   └── style.css     # Styling and animations
│   └── js/
│       └── app.js        # Client-side functionality
└── README.md             # This file
```

### Adding New Features
1. **Sentiment Categories**: Extend `therapy_responses` dictionary
2. **Coping Strategies**: Add to `getCopingStrategies()` function
3. **UI Components**: Modify templates and CSS
4. **API Endpoints**: Add new routes in `app.py`

### Testing
```bash
# Run the application in debug mode
python app.py

# Test individual components
python -c "from app import TherapyBot; bot = TherapyBot(); print(bot.analyze_sentiment('I feel great today!'))"
```

## 🤝 Contributing

We welcome contributions! Areas for improvement:
- Additional sentiment categories
- Enhanced therapeutic response templates
- Multi-language support
- Advanced analytics features
- Mobile app development

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support and Resources

### Crisis Resources
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

### Professional Help
This AI assistant is designed to provide support and coping strategies, but it's not a replacement for professional mental health care. If you're experiencing persistent mental health concerns, please consider:
- Consulting with a licensed therapist
- Contacting your healthcare provider
- Reaching out to mental health organizations in your area

## 🙏 Acknowledgments

- **Cardiff NLP** for the RoBERTa sentiment analysis model
- **Hugging Face** for the Transformers library
- **Flask** community for the web framework
- **Mental health professionals** who inspire ethical AI development

---

**Disclaimer**: This AI therapy assistant is an experimental tool designed for supportive conversations and is not intended to diagnose, treat, cure, or prevent any mental health condition. Always seek professional help for serious mental health concerns.





