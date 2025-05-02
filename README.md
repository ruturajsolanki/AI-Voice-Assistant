# AI Voice Assistant

A voice-controlled assistant that can answer questions, provide weather information, and more.

## Setup Instructions

### 1. Install Dependencies
All dependencies are already installed in the virtual environment.

### 2. Get an OpenWeatherMap API Key
To use the weather functionality, you need to get a free API key from OpenWeatherMap:

1. Go to [OpenWeatherMap](https://openweathermap.org/) and create a free account
2. After signing up, go to your API keys section
3. Copy your API key
4. Open `voice_assistant.py` and replace `YOUR_OPENWEATHERMAP_API_KEY` with your actual API key

### 3. Run the Assistant
```bash
source venv/bin/activate
python voice_assistant.py
```

## Features

- **Voice Recognition**: Listens to your spoken questions
- **Text-to-Speech**: Speaks the answers out loud
- **Weather Information**: Get current weather for any location
- **General Knowledge**: Answers a variety of questions
- **Time and Date**: Tells you the current time and date

## Usage Examples

- "What's the weather in New York?"
- "What time is it?"
- "Who is Albert Einstein?"
- "How do computers work?"

## Exiting the Assistant

Say "exit", "quit", or "stop" to end the conversation.
