# JARVIS - Voice-Activated AI Assistant (100% FREE!)

A personal AI assistant with voice interaction and code editor integration. JARVIS can write code, create projects, and manage files - all through voice commands!

## Features
- 🎤 **FREE Google speech recognition** (no API key needed)
- 🤖 **FREE Groq AI** (Llama 3.3 70B model - fast and powerful)
- 🔊 **FREE offline voice responses** (pyttsx3)
- 💻 **Code editor integration** (read/write files, generate code)
- 🔄 **Continuous conversation mode**
- 🔒 **Safe workspace** (restricted to Documents/Jarvis_Work folder)

## Workspace

JARVIS works in a dedicated folder: `~/Documents/Jarvis_Work`

This keeps your projects organized and your other files safe. JARVIS can:
- Create new projects and folders
- Write and edit code files
- Read existing files
- List directory contents

All within the Jarvis_Work folder!

## Setup

1. **Install dependencies:**
```bash
cd jarvis-assistant
pip install -r requirements.txt
```

2. **Get a FREE Groq API key:**
   - Visit: https://console.groq.com/keys
   - Sign up (completely free, no credit card required)
   - Create an API key
   - Copy the key (starts with `gsk_...`)

3. **Add your API key:**
   - Open the `.env` file
   - Replace `your-groq-api-key-here` with your actual key:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxx
   ```

4. **Run JARVIS:**
```bash
python jarvis.py
```

## Usage

1. **Start a conversation:**
   - Say "Hey Jarvis" to activate
   - JARVIS will greet you and start listening continuously

2. **Have a natural conversation:**
   - Just speak naturally - no need to say "Hey Jarvis" again!
   - "Create a Python file called calculator.py"
   - "Now add a function to add two numbers"
   - "What files do I have?"
   - "Read the calculator.py file"
   - Ask follow-up questions naturally

3. **Pause the conversation:**
   - Say "Stop listening" or "Pause" to pause
   - Say "Hey Jarvis" again to resume

4. **Exit:**
   - Say "Goodbye Jarvis" or "Bye Jarvis" to quit
   - Or just say "Exit", "Quit", or "Goodbye"

## Example Conversations

**Natural conversation flow:**
```
You: "Hey Jarvis"
JARVIS: "Hello! I'm listening. What can I help you with?"

You: "Create a Python file called calculator.py"
JARVIS: "I've created calculator.py in your workspace."

You: "Now add a function to add two numbers"
JARVIS: "I've added an add function to calculator.py."

You: "What other files do I have?"
JARVIS: "You have calculator.py and config.py in your workspace."

You: "Stop listening"
JARVIS: "Okay, I'll wait. Say 'Hey Jarvis' when you need me again."
```

**Project creation:**
- "Create a new project folder called web_app"
- "Add a main.py file with a Flask hello world"
- "Now create a templates folder"
- "Add an index.html file in templates"

## Why 100% FREE?

- **Speech Recognition:** Google's free service (built into SpeechRecognition library)
- **AI Brain:** Groq's free tier with generous limits (14,400 requests/day)
- **Text-to-Speech:** Offline pyttsx3 library (no internet needed)

No credit card, no subscriptions, no hidden costs!

## Configuration

Edit `config.py` to customize:
- `WORKSPACE_DIR` - Change the workspace location
- `GROQ_MODEL` - Switch AI models
- `WAKE_WORD` - Change activation phrase
- `LISTEN_TIMEOUT` - Adjust microphone timeout

## Troubleshooting

**Microphone not working:**
- Check system permissions for microphone access
- Try adjusting `LISTEN_TIMEOUT` in config.py

**API errors:**
- Verify your Groq API key is correct in `.env`
- Check your internet connection

**Voice output issues:**
- pyttsx3 should work out of the box on macOS
- Try adjusting voice rate/volume in `voice_handler.py`

## Safety

JARVIS is restricted to the `~/Documents/Jarvis_Work` folder and cannot:
- Access files outside this folder
- Delete system files
- Modify your personal documents

Your data stays safe!
