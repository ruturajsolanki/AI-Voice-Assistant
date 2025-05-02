# AI Voice Assistant

A voice-controlled assistant that can answer questions, provide weather information, access real-time data through LLM APIs, and more.

## Setup Instructions

### 0. Install Requirements
```bash
pip install -r requirements.txt
```
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
```bash
python voice_assistant.py
```

### 1. Install Dependencies
All dependencies are listed in the requirements.txt file.

### 2. Configure API Keys
The assistant uses several APIs for enhanced functionality:

#### Hugging Face API (Included)
A Hugging Face API key is included in the config.json file.

#### OpenAI API (Optional)
For enhanced capabilities:
1. Create an account on [OpenAI](https://platform.openai.com/signup)
2. Get your API key from the dashboard
3. Add it to the config.json file or set it as an environment variable

#### OpenWeatherMap API (Optional)
For weather data:
1. Go to [OpenWeatherMap](https://openweathermap.org/) and create a free account
2. After signing up, go to your API keys section
3. Copy your API key
4. Add it to the config.json file or set it as an environment variable

### 3. Run the Assistant
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python voice_assistant.py
```

## Features

- **Voice Recognition**: Listens to your spoken questions
- **Text-to-Speech**: Speaks the answers out loud
- **Weather Information**: Get current weather for any location
- **Factual Knowledge**: Accurate information about world leaders, capitals, populations, and more
- **LLM API Integration**: Access to powerful language models for answering complex questions
- **Command History**: Keep track of your previous commands
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Technologies and AI Models Used

The voice assistant uses a combination of different services and technologies:

### Speech Recognition
- **Google Speech Recognition API**: Primary service for converting speech to text
- **CMU Sphinx**: Offline fallback for speech recognition when internet is unavailable

### Text-to-Speech
- **pyttsx3**: Uses your system's built-in speech synthesis engines:
  - macOS: NSSpeechSynthesizer (Samantha voice)
  - Windows: SAPI5
  - Linux: espeak

### Question Answering
- **Hugging Face Models**: API access to powerful language models
- **OpenAI API**: Optional integration for enhanced capabilities
- **Built-in Knowledge Base**: For common questions and faster responses
- **Hardcoded Factual Database**: For accurate information about world leaders and facts
- **DuckDuckGo API**: Used to search the web for answers

### Weather Information
- **OpenWeatherMap API**: Primary source for weather data (requires API key)
- **wttr.in Web Service**: Fallback weather service that doesn't require an API key

## Usage Examples

- "What's the weather in New York?"
- "What time is it?"
- "Who is the President of the United States?"
- "What's the capital of Japan?"
- "How many people live in India?"
- "What's the latest iPhone model?"

## Available Commands

- **help**: Display available commands
- **history**: Show your command history
- **repeat** or **say that again**: Repeat the last response
- **exit**, **quit**, or **stop**: End the conversation

## Exiting the Assistant

Say "exit", "quit", or "stop" to end the conversation.
