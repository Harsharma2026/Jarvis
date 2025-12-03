import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Groq Configuration (FREE API - get key from console.groq.com)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"  # FREE and fast!

# Workspace Configuration
WORKSPACE_DIR = Path.home() / "Documents" / "Jarvis_Work"
# JARVIS can only work within this folder for safety

# Voice Settings
WAKE_WORD = "jarvis"
LISTEN_TIMEOUT = 5  # seconds
PHRASE_TIME_LIMIT = 10  # seconds

# Audio Settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
