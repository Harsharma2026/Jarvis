"""
Voice Handler - FREE speech recognition and text-to-speech
Uses Google Speech Recognition (FREE) + pyttsx3 (FREE offline TTS)
"""

import speech_recognition as sr
import pyttsx3
import config

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize FREE offline TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 175)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Adjust for ambient noise
        print("🎙️  Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Microphone ready!")
    
    def listen(self):
        """Listen using FREE Google Speech Recognition (no API key needed)"""
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=config.LISTEN_TIMEOUT,
                    phrase_time_limit=config.PHRASE_TIME_LIMIT
                )
            
            # Use Google's FREE speech recognition
            text = self.recognizer.recognize_google(audio)
            return text
                
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except Exception as e:
            print(f"❌ Error in speech recognition: {e}")
            return None
    
    def speak(self, text):
        """FREE offline text-to-speech"""
        try:
            print(f"🔊 {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"❌ Error in text-to-speech: {e}")
