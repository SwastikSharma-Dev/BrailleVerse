/**
 * Simplified Voice Navigation for Panel-Based Braille Display Website
 * Always-on listening with panel-based navigation
 */

class VoiceNavigator {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.autoRestart = true;
        
        this.initRecognition();
        
        // Auto-start after page load
        window.addEventListener('load', () => {
            setTimeout(() => {
                this.speakPageContent();
                this.startListening();
            }, 1500);
        });
    }
    
    initRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        
        if (!SpeechRecognition) {
            console.warn('Speech Recognition not supported');
            return;
        }
        
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 3;
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.updateIndicator(true);
        };
        
        this.recognition.onresult = (event) => {
            const result = event.results[event.results.length - 1];
            if (result.isFinal) {
                const transcript = result[0].transcript;
                this.processCommand(transcript);
            }
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech error:', event.error);
        };
        
        this.recognition.onend = () => {
            this.isListening = false;
            this.updateIndicator(false);
            
            // Auto-restart
            if (this.autoRestart) {
                setTimeout(() => {
                    try {
                        this.recognition.start();
                    } catch (e) {
                        console.log('Restart delayed');
                    }
                }, 500);
            }
        };
    }
    
    startListening() {
        if (!this.recognition || this.isListening) return;
        
        try {
            this.recognition.start();
        } catch (e) {
            console.log('Recognition already started');
        }
    }
    
    stopListening() {
        if (this.recognition && this.isListening) {
            this.autoRestart = false;
            this.recognition.stop();
        }
    }
    
    updateIndicator(listening) {
        const indicator = document.getElementById('voiceIndicator');
        if (indicator) {
            indicator.classList.toggle('listening', listening);
        }
    }
    
    speak(text, interrupt = false) {
        if (!this.synthesis) return;
        
        if (interrupt) {
            this.synthesis.cancel();
        }
        
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.95;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        this.synthesis.speak(utterance);
    }
    
    speakPageContent() {
        // Check for data-speak-on-load attribute
        const speakElement = document.querySelector('[data-speak-on-load]');
        if (speakElement) {
            const text = speakElement.getAttribute('data-speak-on-load') || speakElement.textContent;
            this.speak(text);
        }
        
        // Speak sr-only announcements
        const announcement = document.querySelector('.sr-only[role="status"]');
        if (announcement) {
            this.speak(announcement.textContent);
        }
    }
    
    processCommand(command) {
        const cmd = command.toLowerCase().trim();
        console.log('Voice command:', cmd);
        
        // Extract numbers (for panel selection)
        const numberMatch = this.extractNumber(cmd);
        
        // Navigation commands
        if (cmd.includes('helper') || cmd.includes('help someone')) {
            this.navigate('/helper/');
        } else if (cmd.includes('visually impaired') || cmd.includes('blind') || cmd.includes('impaired')) {
            this.navigate('/visually-impaired/');
        } else if (cmd.includes('book')) {
            if (window.location.href.includes('visually-impaired')) {
                this.navigate('/visually-impaired/books/');
            } else {
                this.navigate('/visually-impaired/books/');
            }
        } else if (cmd.includes('news')) {
            this.navigate('/visually-impaired/news/');
        } else if (cmd.includes('headline')) {
            this.navigate('/visually-impaired/news/headlines/');
        } else if (cmd.includes('technology') || cmd.includes('tech')) {
            this.navigate('/visually-impaired/news/technology/');
        } else if (cmd.includes('sports') || cmd.includes('sport')) {
            this.navigate('/visually-impaired/news/sports/');
        } else if (cmd.includes('business')) {
            this.navigate('/visually-impaired/news/business/');
        } else if (cmd.includes('ai') || cmd.includes('assistant') || cmd.includes('chat')) {
            this.navigate('/visually-impaired/ai-helper/');
        } else if (cmd.includes('custom text') || cmd.includes('type text') || cmd.includes('send text')) {
            this.navigate('/helper/custom-text/');
        } else if (cmd.includes('pdf')) {
            this.navigate('/helper/pdf-to-braille/');
        } else if (cmd.includes('image') || cmd.includes('picture') || cmd.includes('photo')) {
            this.navigate('/helper/image-transcription/');
        } else if (cmd.includes('back') || cmd.includes('go back')) {
            window.history.back();
        } else if (cmd.includes('home') || cmd.includes('homepage')) {
            this.navigate('/');
        } else if (numberMatch !== null) {
            // Try to click panel by number
            this.selectPanel(numberMatch);
        } else {
            console.log('Command not recognized:', cmd);
        }
    }
    
    extractNumber(text) {
        // Match various number formats
        const patterns = [
            /\b(?:option\s*)?(\d+)/i,
            /\b(one|two|three|four|five|six|seven|eight|nine|ten)\b/i,
            /\b(first|second|third|fourth|fifth)\b/i,
            /\b(\d+)(?:st|nd|rd|th)\b/i
        ];
        
        for (const pattern of patterns) {
            const match = text.match(pattern);
            if (match) {
                const num = match[1].toLowerCase();
                const wordToNum = {
                    'one': 1, 'first': 1,
                    'two': 2, 'second': 2,
                    'three': 3, 'third': 3,
                    'four': 4, 'fourth': 4,
                    'five': 5, 'fifth': 5,
                    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
                };
                return wordToNum[num] || parseInt(match[1]);
            }
        }
        return null;
    }
    
    selectPanel(number) {
        const panels = document.querySelectorAll('.panel');
        if (panels.length >= number) {
            const panel = panels[number - 1];
            this.speak(`Selecting option ${number}`);
            panel.click();
        }
    }
    
    navigate(url) {
        this.speak(`Navigating to ${url.split('/').filter(Boolean).join(' ')}`);
        setTimeout(() => {
            window.location.href = url;
        }, 1000);
    }
}

// Initialize voice navigator
let voiceNav;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        voiceNav = new VoiceNavigator();
    });
} else {
    voiceNav = new VoiceNavigator();
}

// Expose for debugging
window.voiceNav = voiceNav;
