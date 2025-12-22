/**
 * Voice Navigation System for Braille Display Website
 * 
 * This module provides comprehensive voice input/output functionality:
 * - SpeechRecognition for voice commands
 * - SpeechSynthesis for voice feedback
 * - Automatic page narration
 * - Voice-activated navigation
 * 
 * WCAG 2.1 Level AAA compliant
 */

class VoiceNavigator {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.voices = [];
        this.currentUtterance = null;
        this.autoRestart = true; // Always-on listening
        this.commandHistory = [];
        
        // Initialize speech recognition
        this.initRecognition();
        
        // Load available voices
        this.loadVoices();
        
        // Auto-speak on page load and start listening
        window.addEventListener('load', () => {
            this.speakPageContent();
            // Start listening automatically after 2 seconds
            setTimeout(() => {
                this.startListening();
            }, 2000);
        });
    }
    
    /**
     * Initialize Web Speech API Recognition
     */
    initRecognition() {
        // Check browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Speech Recognition not supported in this browser');
            this.showFallbackMessage();
            return;
        }
        
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true; // Continuous listening
        this.recognition.interimResults = true; // Get interim results
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 3; // Get multiple interpretations
        
        // Event handlers
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateListeningIndicator(true);
            console.log('Voice recognition started');
        };
        
        this.recognition.onresult = (event) => {
            const result = event.results[event.results.length - 1];
            if (result.isFinal) {
                const transcript = result[0].transcript;
                console.log('Heard (final):', transcript);
                this.processVoiceCommand(transcript);
            }
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isListening = false;
            this.updateListeningIndicator(false);
        };
        
        this.recognition.onend = () => {
            console.log('Voice recognition ended');
            // Auto-restart if enabled (always-on mode)
            if (this.autoRestart && this.recognition) {
                console.log('Restarting voice recognition (always-on mode)');
                setTimeout(() => {
                    try {
                        if (!this.isListening) {
                            this.recognition.start();
                            this.isListening = true;
                        }
                    } catch (error) {
                        console.log('Recognition restart error:', error);
                    }
                }, 500);
            } else {
                this.isListening = false;
                this.updateListeningIndicator(false);
            }
        };
    }
    
    /**
     * Load available voices for speech synthesis
     */
    loadVoices() {
        this.voices = this.synthesis.getVoices();
        
        // Voices load asynchronously in some browsers
        if (this.synthesis.onvoiceschanged !== undefined) {
            this.synthesis.onvoiceschanged = () => {
                this.voices = this.synthesis.getVoices();
            };
        }
    }
    
    /**
     * Speak text using speech synthesis
     */
    speak(text, options = {}) {
        // Stop any current speech
        this.stopSpeaking();
        
        if (!text) return;
        
        const utterance = new SpeechSynthesisUtterance(text);
        
        // Configure utterance
        utterance.rate = options.rate || 1.0;
        utterance.pitch = options.pitch || 1.0;
        utterance.volume = options.volume || 1.0;
        
        // Select voice (prefer female English voice for accessibility)
        const preferredVoice = this.voices.find(voice => 
            voice.lang.startsWith('en') && voice.name.includes('Female')
        ) || this.voices.find(voice => voice.lang.startsWith('en'));
        
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }
        
        // Event handlers
        utterance.onend = () => {
            this.currentUtterance = null;
            if (options.onEnd) options.onEnd();
        };
        
        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            this.currentUtterance = null;
        };
        
        this.currentUtterance = utterance;
        this.synthesis.speak(utterance);
        
        // Also show in visual feedback area
        this.showVisualFeedback(text);
    }
    
    /**
     * Stop current speech
     */
    stopSpeaking() {
        if (this.synthesis.speaking) {
            this.synthesis.cancel();
        }
        this.currentUtterance = null;
    }
    
    /**
     * Start listening for voice commands
     */
    startListening() {
        if (!this.recognition) {
            this.speak('Voice recognition is not available in this browser.');
            return;
        }
        
        if (this.isListening) {
            return;
        }
        
        try {
            this.recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
        }
    }
    
    /**
     * Stop listening
     */
    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
    }
    
    /**
     * Calculate similarity between two strings for fuzzy matching
     */
    calculateSimilarity(str1, str2) {
        const longer = str1.length > str2.length ? str1 : str2;
        const shorter = str1.length > str2.length ? str2 : str1;
        
        if (longer.length === 0) return 1.0;
        
        // Check if shorter is contained in longer
        if (longer.includes(shorter)) return 0.8;
        
        // Simple word overlap scoring
        const words1 = str1.split(/\s+/);
        const words2 = str2.split(/\s+/);
        let matches = 0;
        
        for (let w1 of words1) {
            for (let w2 of words2) {
                if (w1 === w2 || w1.includes(w2) || w2.includes(w1)) {
                    matches++;
                    break;
                }
            }
        }
        
        return matches / Math.max(words1.length, words2.length);
    }
    
    /**
     * Handle identified intents
     */
    handleIntent(intent) {
        switch(intent) {
            case 'back':
                this.speak('Going back');
                setTimeout(() => window.history.back(), 500);
                break;
            case 'repeat':
                this.speakPageContent();
                break;
            case 'help':
                this.speakHelp();
                break;
            case 'home':
                this.speak('Going to main menu');
                setTimeout(() => window.location.href = '/main-menu/', 500);
                break;
            case 'stop':
                this.stopSpeaking();
                break;
        }
    }
    
    /**
     * Process recognized voice command with improved NLU
     */
    processVoiceCommand(command) {
        const lowerCommand = command.toLowerCase().trim();
        
        // Store in history
        this.commandHistory.push(command);
        if (this.commandHistory.length > 10) this.commandHistory.shift();
        
        console.log('Processing command:', command);
        
        // Enhanced number recognition - support multiple formats
        const numberPatterns = [
            /(?:option|number|choice)\s*(\d+)/i,
            /(\d+)(?:st|nd|rd|th)?\s*(?:option|choice)?/i,
            /(one|two|three|four|five|six|seven|eight|nine|ten|first|second|third|fourth|fifth)/i
        ];
        
        for (let pattern of numberPatterns) {
            const match = lowerCommand.match(pattern);
            if (match) {
                const numberWords = {
                    'one': 1, 'first': 1,
                    'two': 2, 'second': 2,
                    'three': 3, 'third': 3,
                    'four': 4, 'fourth': 4,
                    'five': 5, 'fifth': 5,
                    'six': 6, 'sixth': 6,
                    'seven': 7, 'seventh': 7,
                    'eight': 8, 'eighth': 8,
                    'nine': 9, 'ninth': 9,
                    'ten': 10, 'tenth': 10
                };
                const numStr = match[1].toLowerCase();
                const num = numberWords[numStr] || parseInt(numStr);
                if (num && !isNaN(num)) {
                    this.selectOption(num);
                    return;
                }
            }
        }
        
        // Enhanced fuzzy matching for button text
        const buttons = document.querySelectorAll('.nav-button, .option-button');
        let bestMatch = null;
        let bestScore = 0;
        
        for (let button of buttons) {
            const buttonText = button.textContent.toLowerCase().trim();
            const score = this.calculateSimilarity(lowerCommand, buttonText);
            
            // Direct match or high similarity
            if (score > bestScore) {
                bestMatch = button;
                bestScore = score;
            }
            
            // Also check for key word matches
            const commandWords = lowerCommand.split(/\s+/);
            const buttonWords = buttonText.split(/\s+/);
            
            for (let cmdWord of commandWords) {
                if (cmdWord.length < 3) continue;
                for (let btnWord of buttonWords) {
                    if (btnWord.includes(cmdWord) || cmdWord.includes(btnWord)) {
                        bestScore = Math.max(bestScore, 0.7);
                    }
                }
            }
        }
        
        if (bestMatch && bestScore > 0.5) {
            this.speak(`Selecting ${bestMatch.textContent}`);
            setTimeout(() => bestMatch.click(), 500);
            return;
        }
        
        // Enhanced special commands with more variations
        const intentMap = {
            'back': ['back', 'go back', 'previous page', 'return', 'previous'],
            'repeat': ['repeat', 'say again', 'say that again', 'what'],
            'help': ['help', 'help me', 'options', 'what can i do'],
            'home': ['home', 'main menu', 'menu', 'start'],
            'stop': ['stop', 'quiet', 'silence', 'shut up']
        };
        
        // Check intents
        for (let [intent, phrases] of Object.entries(intentMap)) {
            for (let phrase of phrases) {
                if (lowerCommand.includes(phrase)) {
                    this.handleIntent(intent);
                    return;
                }
            }
        }
        
        // Send to server for additional processing
        this.sendCommandToServer(command);
    }
    
    /**
     * Select option by number
     */
    selectOption(number) {
        const buttons = document.querySelectorAll('.nav-button, .option-button');
        if (number > 0 && number <= buttons.length) {
            const button = buttons[number - 1];
            this.speak(`Selecting: ${button.textContent}`);
            setTimeout(() => button.click(), 1000);
        } else {
            this.speak(`Option ${number} not available. Please choose between 1 and ${buttons.length}.`);
        }
    }
    
    /**
     * Send command to server for processing
     */
    async sendCommandToServer(command) {
        try {
            const response = await fetch('/api/voice-command/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ command: command })
            });
            
            const data = await response.json();
            
            if (data.action === 'navigate' && data.url) {
                this.speak(data.message);
                setTimeout(() => {
                    window.location.href = data.url;
                }, 1500);
            } else if (data.action === 'back') {
                window.history.back();
            } else {
                this.speak(data.message || 'Command not recognized');
            }
        } catch (error) {
            console.error('Error sending command:', error);
            this.speak('Sorry, there was an error processing your command.');
        }
    }
    
    /**
     * Automatically speak page content on load
     */
    speakPageContent() {
        // Get page announcement
        const announcement = document.querySelector('[data-speak-on-load]');
        if (announcement) {
            const text = announcement.getAttribute('data-speak-on-load') || announcement.textContent;
            this.speak(text);
            return;
        }
        
        // Fallback: speak page title and main instruction
        const title = document.querySelector('h1');
        const instruction = document.querySelector('.instruction');
        
        let textToSpeak = '';
        if (title) textToSpeak += title.textContent + '. ';
        if (instruction) textToSpeak += instruction.textContent;
        
        if (textToSpeak) {
            this.speak(textToSpeak);
        }
    }
    
    /**
     * Speak help information
     */
    speakHelp() {
        const helpText = `You can navigate using voice commands. Say the name of any button to select it, 
                          or say the number of the option. Say "back" to go back, or "repeat" to hear the 
                          page content again. Say "help" at any time to hear this message.`;
        this.speak(helpText);
    }
    
    /**
     * Update listening indicator UI
     */
    updateListeningIndicator(listening) {
        const indicator = document.getElementById('listening-indicator');
        if (indicator) {
            indicator.classList.toggle('active', listening);
            indicator.textContent = listening ? '🎤 Listening...' : '🎤 Voice Input';
        }
        
        const voiceBtn = document.getElementById('voice-button');
        if (voiceBtn) {
            voiceBtn.classList.toggle('listening', listening);
            voiceBtn.setAttribute('aria-label', listening ? 'Stop listening' : 'Start voice input');
        }
    }
    
    /**
     * Show visual feedback for spoken text
     */
    showVisualFeedback(text) {
        const feedback = document.getElementById('voice-feedback');
        if (feedback) {
            feedback.textContent = text;
            feedback.classList.add('active');
            
            setTimeout(() => {
                feedback.classList.remove('active');
            }, 3000);
        }
    }
    
    /**
     * Show fallback message when speech recognition is not supported
     */
    showFallbackMessage() {
        const message = document.getElementById('browser-support-message');
        if (message) {
            message.style.display = 'block';
            message.textContent = 'Voice recognition is not supported in this browser. Please use Chrome, Edge, or Safari.';
        }
    }
}

// Initialize voice navigator
let voiceNavigator;

document.addEventListener('DOMContentLoaded', () => {
    voiceNavigator = new VoiceNavigator();
    
    // Bind voice button
    const voiceButton = document.getElementById('voice-button');
    if (voiceButton) {
        voiceButton.addEventListener('click', () => {
            if (voiceNavigator.isListening) {
                voiceNavigator.stopListening();
            } else {
                voiceNavigator.startListening();
            }
        });
    }
    
    // Bind voice text input (for custom text page)
    const voiceTextButton = document.getElementById('voice-text-button');
    if (voiceTextButton) {
        voiceTextButton.addEventListener('click', () => {
            startVoiceTextInput();
        });
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Space: Toggle voice input
        if ((e.ctrlKey || e.metaKey) && e.code === 'Space') {
            e.preventDefault();
            if (voiceNavigator.isListening) {
                voiceNavigator.stopListening();
            } else {
                voiceNavigator.startListening();
            }
        }
        
        // Escape: Stop speaking
        if (e.code === 'Escape') {
            voiceNavigator.stopSpeaking();
        }
        
        // H key: Help
        if (e.code === 'KeyH' && !e.ctrlKey && !e.metaKey) {
            const activeElement = document.activeElement;
            if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
                voiceNavigator.speakHelp();
            }
        }
        
        // R key: Repeat
        if (e.code === 'KeyR' && !e.ctrlKey && !e.metaKey) {
            const activeElement = document.activeElement;
            if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
                voiceNavigator.speakPageContent();
            }
        }
    });
});

/**
 * Voice-to-text for input fields
 */
function startVoiceTextInput() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        alert('Voice recognition is not supported in this browser.');
        return;
    }
    
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    const textInput = document.getElementById('text-input') || document.getElementById('question-input');
    
    recognition.onstart = () => {
        voiceNavigator.speak('Listening for your text...');
        const indicator = document.getElementById('voice-text-indicator');
        if (indicator) indicator.textContent = 'Listening...';
    };
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (textInput) {
            textInput.value = transcript;
            voiceNavigator.speak('Text captured. You can submit or continue editing.');
        }
    };
    
    recognition.onerror = (event) => {
        console.error('Voice input error:', event.error);
        voiceNavigator.speak('Sorry, there was an error. Please try again.');
    };
    
    recognition.onend = () => {
        const indicator = document.getElementById('voice-text-indicator');
        if (indicator) indicator.textContent = '';
    };
    
    recognition.start();
}

/**
 * Announce form submission results
 */
function announceResult(message) {
    if (voiceNavigator) {
        voiceNavigator.speak(message);
    }
}

// Export for use in HTML
window.voiceNavigator = voiceNavigator;
window.startVoiceTextInput = startVoiceTextInput;
window.announceResult = announceResult;
