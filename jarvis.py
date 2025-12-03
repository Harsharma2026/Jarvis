#!/usr/bin/env python3
"""
JARVIS - Voice-Activated AI Assistant
Main entry point for the assistant
"""

import sys
from assistant.voice_handler import VoiceHandler
from assistant.ai_brain import AIBrain
from assistant.code_handler import CodeHandler
from config import WAKE_WORD
import config

def main():
    print("🤖 Initializing JARVIS...")
    
    # Check API key
    if not config.GROQ_API_KEY:
        print("❌ Error: GROQ_API_KEY not found")
        print("Get a FREE API key from: https://console.groq.com/keys")
        print("Then add it to the .env file")
        sys.exit(1)
    
    # Initialize components
    from assistant.memory import Memory
    
    voice = VoiceHandler()
    memory = Memory(config.WORKSPACE_DIR)
    brain = AIBrain(memory=memory)
    code_handler = CodeHandler(memory=memory)
    
    # Update session
    memory.update_session()
    
    print(f"✅ JARVIS is ready!")
    print(f"💡 Say '{WAKE_WORD}' to start a conversation")
    print(f"💡 Or press Ctrl+C to exit\n")
    
    conversation_active = False
    
    try:
        while True:
            if not conversation_active:
                # Listen for wake word to start conversation
                print(f"👂 Listening for '{WAKE_WORD}'...")
                text = voice.listen()
                
                if not text:
                    continue
                    
                if WAKE_WORD.lower() in text.lower():
                    conversation_active = True
                    voice.speak("Hello! I'm listening. What can I help you with?")
                    print("🎤 Conversation started! (Say 'stop listening' to pause)\n")
            else:
                # Continuous conversation mode
                print("👂 Listening...")
                command = voice.listen()
                
                if not command:
                    continue
                
                print(f"📝 You: {command}")
                
                # Check for exit commands
                command_lower = command.lower()
                if any(phrase in command_lower for phrase in ["goodbye jarvis", "bye jarvis", "exit jarvis"]):
                    voice.speak("Goodbye! Have a great day!")
                    break
                elif any(word in command_lower for word in ["exit", "quit", "goodbye", "bye"]):
                    voice.speak("Goodbye! Have a great day!")
                    break
                
                # Check for pause command
                if any(phrase in command.lower() for phrase in ["stop listening", "pause", "sleep"]):
                    voice.speak("Okay, I'll wait. Say 'Hey Jarvis' when you need me again.")
                    conversation_active = False
                    print("💤 Conversation paused\n")
                    continue
                
                # Process command with AI
                response = brain.process_command(command, code_handler)
                print(f"💭 JARVIS: {response}\n")
                
                # Speak the response
                voice.speak(response)
    
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down JARVIS...")
        voice.speak("Shutting down. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        voice.speak("I encountered an error. Please check the console.")

if __name__ == "__main__":
    main()
