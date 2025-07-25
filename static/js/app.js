// Global variables
let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];
let currentAudio = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    console.log('AI Therapy Assistant initialized');
    
    // Check for microphone permissions
    checkMicrophonePermissions();
    
    // Initialize text-to-speech
    initializeTextToSpeech();
    
    // Set up keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Auto-focus on message input
    document.getElementById('messageInput').focus();
}

async function checkMicrophonePermissions() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        stream.getTracks().forEach(track => track.stop());
        console.log('Microphone access granted');
    } catch (error) {
        console.warn('Microphone access denied:', error);
        showNotification('Microphone access is required for voice input', 'warning');
    }
}

function initializeTextToSpeech() {
    // Check if speech synthesis is supported
    if ('speechSynthesis' in window) {
        console.log('Text-to-speech is supported');
    } else {
        console.warn('Text-to-speech is not supported in this browser');
    }
}

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
        // Ctrl/Cmd + Enter to send message
        if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
            sendMessage();
        }
        
        // Escape to stop recording
        if (event.key === 'Escape' && isRecording) {
            stopRecording();
        }
    });
}

// Voice recording functions
async function toggleRecording() {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
}

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true
            }
        });
        
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus'
        });
        
        audioChunks = [];
        
        mediaRecorder.ondataavailable = function(event) {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };
        
        mediaRecorder.onstop = function() {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            processAudioInput(audioBlob);
            
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
        };
        
        mediaRecorder.start();
        isRecording = true;
        
        updateVoiceButton();
        showRecordingIndicator();
        
        console.log('Recording started');
        
    } catch (error) {
        console.error('Error starting recording:', error);
        showNotification('Failed to start recording. Please check microphone permissions.', 'error');
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        
        updateVoiceButton();
        hideRecordingIndicator();
        
        console.log('Recording stopped');
    }
}

function updateVoiceButton() {
    const voiceBtn = document.getElementById('voiceBtn');
    const voiceStatus = voiceBtn.querySelector('.voice-status');
    const icon = voiceBtn.querySelector('i');
    
    if (isRecording) {
        voiceBtn.classList.add('recording');
        voiceStatus.textContent = 'Recording... (click to stop)';
        icon.className = 'fas fa-stop';
    } else {
        voiceBtn.classList.remove('recording');
        voiceStatus.textContent = 'Click to speak';
        icon.className = 'fas fa-microphone';
    }
}

function showRecordingIndicator() {
    const indicator = document.getElementById('recordingIndicator');
    indicator.classList.add('active');
}

function hideRecordingIndicator() {
    const indicator = document.getElementById('recordingIndicator');
    indicator.classList.remove('active');
}

// Audio processing
async function processAudioInput(audioBlob) {
    showLoading();
    
    try {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        
        const response = await fetch('/process_audio', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            handleBotResponse(data);
        } else {
            throw new Error(data.error || 'Failed to process audio');
        }
        
    } catch (error) {
        console.error('Error processing audio:', error);
        showNotification('Failed to process audio. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

// Text message handling
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Clear input and show user message
    messageInput.value = '';
    addMessage(message, 'user');
    
    showLoading();
    
    try {
        const response = await fetch('/process_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: message })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            handleBotResponse(data);
        } else {
            throw new Error(data.error || 'Failed to process message');
        }
        
    } catch (error) {
        console.error('Error sending message:', error);
        showNotification('Failed to send message. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Bot response handling
function handleBotResponse(data) {
    // Add bot message
    addMessage(data.bot_response, 'bot', data.sentiment, data.audio_id);
    
    // Update sentiment dashboard
    updateSentimentDashboard(data.sentiment);
    
    // Auto-play response if audio is available
    if (data.audio_id) {
        setTimeout(() => {
            playBotAudio(data.audio_id);
        }, 500);
    }
}

// Message display
function addMessage(text, sender, sentiment = null, audioId = null) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    let sentimentBadge = '';
    if (sentiment) {
        sentimentBadge = `<span class="sentiment-badge sentiment-${sentiment.sentiment}">${sentiment.sentiment}</span>`;
    }
    
    let audioButton = '';
    if (audioId) {
        audioButton = `<button class="play-audio-btn" onclick="playBotAudio('${audioId}')" title="Play audio response">
            <i class="fas fa-volume-up"></i>
        </button>`;
    } else if (sender === 'bot') {
        audioButton = `<button class="play-audio-btn" onclick="speakText(this)" data-text="${text.replace(/"/g, '&quot;')}" title="Read aloud">
            <i class="fas fa-volume-up"></i>
        </button>`;
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-${sender === 'user' ? 'user' : 'robot'}"></i>
        </div>
        <div class="message-content">
            <p>${text}</p>
            ${sentimentBadge}
            <div class="message-meta">
                <span class="timestamp">${timestamp}</span>
                ${audioButton}
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Audio playback
async function playBotAudio(audioId) {
    try {
        // Stop current audio if playing
        if (currentAudio) {
            currentAudio.pause();
            currentAudio = null;
        }
        
        const audio = new Audio(`/get_audio/${audioId}`);
        currentAudio = audio;
        
        audio.onended = () => {
            currentAudio = null;
        };
        
        audio.onerror = () => {
            console.error('Error playing audio');
            showNotification('Failed to play audio response', 'warning');
            currentAudio = null;
        };
        
        await audio.play();
        
    } catch (error) {
        console.error('Error playing audio:', error);
        showNotification('Failed to play audio response', 'warning');
    }
}

// Text-to-speech fallback
function speakText(button) {
    const text = button.getAttribute('data-text');
    
    if ('speechSynthesis' in window) {
        // Stop any current speech
        speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        
        // Try to use a more natural voice
        const voices = speechSynthesis.getVoices();
        const preferredVoice = voices.find(voice => 
            voice.name.includes('Google') || 
            voice.name.includes('Microsoft') ||
            voice.name.includes('Natural')
        );
        
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }
        
        speechSynthesis.speak(utterance);
        
        // Visual feedback
        const icon = button.querySelector('i');
        const originalClass = icon.className;
        icon.className = 'fas fa-volume-up fa-pulse';
        
        utterance.onend = () => {
            icon.className = originalClass;
        };
        
    } else {
        showNotification('Text-to-speech is not supported in this browser', 'warning');
    }
}

// Sentiment dashboard updates
function updateSentimentDashboard(sentimentData) {
    const currentMood = document.getElementById('currentMood');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidenceValue = document.getElementById('confidenceValue');
    const strategiesList = document.getElementById('strategiesList');
    
    // Update current mood
    currentMood.textContent = sentimentData.sentiment.charAt(0).toUpperCase() + sentimentData.sentiment.slice(1);
    currentMood.className = `sentiment-value sentiment-${sentimentData.sentiment}`;
    
    // Update confidence
    const confidence = Math.round(sentimentData.confidence * 100);
    confidenceFill.style.width = `${confidence}%`;
    confidenceValue.textContent = `${confidence}%`;
    
    // Update coping strategies based on sentiment
    const strategies = getCopingStrategies(sentimentData.sentiment);
    strategiesList.innerHTML = strategies.map(strategy => `<li>${strategy}</li>`).join('');
}

function getCopingStrategies(sentiment) {
    const strategies = {
        'positive': [
            'Savor this positive moment',
            'Practice gratitude journaling',
            'Share your joy with others',
            'Engage in activities you love'
        ],
        'negative': [
            'Practice deep breathing exercises',
            'Try progressive muscle relaxation',
            'Reach out to a trusted friend',
            'Consider professional support'
        ],
        'anxiety': [
            'Use the 5-4-3-2-1 grounding technique',
            'Practice box breathing (4-4-4-4)',
            'Try mindfulness meditation',
            'Challenge anxious thoughts'
        ],
        'sadness': [
            'Allow yourself to feel emotions',
            'Practice self-compassion',
            'Engage in gentle physical activity',
            'Connect with supportive people'
        ],
        'neutral': [
            'Check in with your emotions',
            'Practice mindful awareness',
            'Set small, achievable goals',
            'Take care of basic needs'
        ]
    };
    
    return strategies[sentiment] || strategies['neutral'];
}

// Session summary
async function showSessionSummary() {
    showLoading();
    
    try {
        const response = await fetch('/session_summary');
        const data = await response.json();
        
        if (response.ok) {
            displaySessionSummary(data);
        } else {
            throw new Error(data.error || 'Failed to load session summary');
        }
        
    } catch (error) {
        console.error('Error loading session summary:', error);
        showNotification('Failed to load session summary', 'error');
    } finally {
        hideLoading();
    }
}

function displaySessionSummary(data) {
    const modal = document.getElementById('sessionModal');
    const content = document.getElementById('sessionSummaryContent');
    
    let sentimentChart = '';
    if (Object.keys(data.sentiment_distribution).length > 0) {
        sentimentChart = `
            <div class="sentiment-chart">
                <h4>Emotion Distribution</h4>
                <div class="chart-bars">
                    ${Object.entries(data.sentiment_distribution).map(([sentiment, count]) => `
                        <div class="chart-bar">
                            <div class="bar-label">${sentiment}</div>
                            <div class="bar-fill sentiment-${sentiment}" style="width: ${(count / data.total_interactions) * 100}%"></div>
                            <div class="bar-value">${count}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    content.innerHTML = `
        <div class="summary-stats">
            <div class="stat-item">
                <h4>Session Duration</h4>
                <p>${data.session_duration}</p>
            </div>
            <div class="stat-item">
                <h4>Total Interactions</h4>
                <p>${data.total_interactions}</p>
            </div>
        </div>
        
        ${sentimentChart}
        
        <div class="recent-interactions">
            <h4>Recent Conversations</h4>
            ${data.recent_interactions.map(interaction => `
                <div class="interaction-item">
                    <div class="interaction-meta">
                        <span class="timestamp">${new Date(interaction.timestamp).toLocaleString()}</span>
                        <span class="sentiment-badge sentiment-${interaction.sentiment.sentiment}">
                            ${interaction.sentiment.sentiment}
                        </span>
                    </div>
                    <div class="interaction-content">
                        <strong>You:</strong> ${interaction.user_input}
                    </div>
                    <div class="interaction-response">
                        <strong>Therapist:</strong> ${interaction.bot_response.substring(0, 100)}...
                    </div>
                </div>
            `).join('')}
        </div>
        
        <style>
            .summary-stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .stat-item {
                background: #f8fafc;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }
            
            .stat-item h4 {
                color: #6b7280;
                margin-bottom: 10px;
                font-size: 0.9rem;
            }
            
            .stat-item p {
                font-size: 1.5rem;
                font-weight: 600;
                color: #374151;
            }
            
            .sentiment-chart {
                margin-bottom: 30px;
            }
            
            .chart-bars {
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 15px;
            }
            
            .chart-bar {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .bar-label {
                width: 80px;
                font-size: 0.9rem;
                text-transform: capitalize;
            }
            
            .bar-fill {
                height: 20px;
                min-width: 20px;
                border-radius: 10px;
                transition: width 0.5s ease;
            }
            
            .bar-value {
                font-weight: 600;
                font-size: 0.9rem;
            }
            
            .interaction-item {
                background: #f8fafc;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
            }
            
            .interaction-meta {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                font-size: 0.8rem;
            }
            
            .interaction-content,
            .interaction-response {
                margin-bottom: 8px;
                font-size: 0.9rem;
                line-height: 1.4;
            }
        </style>
    `;
    
    modal.classList.add('active');
}

function closeModal() {
    const modal = document.getElementById('sessionModal');
    modal.classList.remove('active');
}

// Utility functions
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.add('active');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.remove('active');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">&times;</button>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#fee2e2' : type === 'warning' ? '#fef3c7' : '#dbeafe'};
        color: ${type === 'error' ? '#991b1b' : type === 'warning' ? '#92400e' : '#1e40af'};
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 10px;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Add CSS for notification animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-close {
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        color: inherit;
        opacity: 0.7;
        margin-left: 10px;
    }
    
    .notification-close:hover {
        opacity: 1;
    }
`;
document.head.appendChild(style);

// Handle modal clicks
document.addEventListener('click', function(event) {
    const modal = document.getElementById('sessionModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Initialize speech synthesis voices (some browsers need this)
if ('speechSynthesis' in window) {
    speechSynthesis.onvoiceschanged = function() {
        console.log('Speech synthesis voices loaded');
    };
}