# Local AI Voice Assistant

A real-time voice chat application powered by local AI models. This project allows you to have voice conversations with AI models like Gemma running locally on your machine.

## Features

- Real-time speech-to-text conversion
- Local LLM inference using Ollama
- Text-to-speech response generation
- Web interface for interaction
- Phone number interface option


## Installation



### 1. Clone the repository

```bash
git clone https://github.com/Yahya-osama-mohmamed/Local-hosted-AI-Voice-Assistant.git
cd Local-hosted-AI-Voice-Assistant
```

### 2. Set up Python environment and install dependencies

```bash
python -m venv venv
source .venv/bin/activate
## Prerequisites

- pip install -r requirements.txt

### 3. Download required models in Ollama


ollama pull gemma3:1b
# For advanced version
ollama pull gemma3:4b
```

### 4 download piper voice
```bash
python -m piper.download_voices en_US-lessac-medium

```

## Usage

### Basic Voice Chat for kokoro

```bash
python local_voice_chat.py 
```

### Advanced Voice Chat (with system prompt) for  kokoro

#### Web UI (default)
```bash
python local_voice_chat_advanced.py
```

### Advanced Voice Chat (with system prompt) for piper

```bash
python piper_voice.py 
```


#### Phone Number Interface
Get a temporary phone number that anyone can call to interact with your AI:
```bash
python local_voice_chat_advanced.py --phone
```

This will provide you with a temporary phone number that you can call to interact with the AI using your voice.

## How it works

The application uses:
- `FastRTC` for WebRTC communication
- `Moonshine` for local speech-to-text conversion
- `piper or kokoro` for text-to-speech synthesis
- `Ollama` for running local LLM inference with `Gemma` models

When you speak, your audio is:
1. Transcribed to text using Moonshine
2. Sent to a local LLM via Ollama for processing
3. The LLM response is converted back to speech with Kokoro
4. The audio response is streamed back to you via FastRTC






