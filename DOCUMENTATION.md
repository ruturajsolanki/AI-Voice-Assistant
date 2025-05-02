# AI Voice Assistant Documentation

This document provides comprehensive instructions for setting up and using the AI Voice Assistant on different operating systems.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Windows Setup](#windows-setup)
   - [macOS Setup](#macos-setup)
   - [Linux Setup](#linux-setup)
4. [Configuration](#configuration)
   - [API Keys](#api-keys)
   - [Voice Settings](#voice-settings)
5. [Usage Guide](#usage-guide)
   - [Available Commands](#available-commands)
   - [Example Queries](#example-queries)
6. [Troubleshooting](#troubleshooting)
7. [Recent Changes and Improvements](#recent-changes-and-improvements)

## Overview

The AI Voice Assistant is a Python-based application that can understand spoken commands, answer questions, provide weather information, and access real-time data through LLM APIs. It uses speech recognition to convert your voice to text, processes your requests, and responds both in text and with synthesized speech.

## Features

- **Voice Recognition**: Listens to your spoken questions and commands
- **Text-to-Speech**: Speaks responses out loud with a natural-sounding voice
- **Weather Information**: Gets current weather for any location worldwide
- **Factual Knowledge**: Built-in database of accurate information about world leaders, populations, capitals, and more
- **LLM API Integration**: Access to powerful language models for answering complex questions
- **Time and Date**: Tells you the current time and date
- **Command History**: Keeps track of your previous commands
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection (for speech recognition and web searches)
- Microphone (for voice input)
- Speakers (for voice output)

### Windows Setup

1. **Install Python**:
   - Download and install Python from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Create a Virtual Environment** (optional but recommended):
   ```
   mkdir AI_Voice_Assistant
   cd AI_Voice_Assistant
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Required Packages**:
   ```
   pip install -r requirements.txt
   ```
   
   Note: If you have trouble installing PyAudio, you can download a pre-compiled wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it with:
   ```
   pip install [downloaded-wheel-file].whl
   ```

4. **Download the Voice Assistant Code**:
   - Copy the `voice_assistant.py` file to your project directory

5. **Run the Assistant**:
   ```
   python voice_assistant.py
   ```

### macOS Setup

1. **Install Python**:
   - Download and install Python from [python.org](https://www.python.org/downloads/)
   - Or use Homebrew: `brew install python`

2. **Install Required System Dependencies**:
   ```
   brew install portaudio
   ```

3. **Create a Virtual Environment**:
   ```
   mkdir AI_Voice_Assistant
   cd AI_Voice_Assistant
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Required Packages**:
   ```
   pip install -r requirements.txt
   ```

5. **Download the Voice Assistant Code**:
   - Copy the `voice_assistant.py` file to your project directory

6. **Run the Assistant**:
   ```
   python voice_assistant.py
   ```

### Linux Setup

1. **Install Python and Required System Dependencies**:
   ```
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-venv
   sudo apt-get install portaudio19-dev python3-pyaudio
   sudo apt-get install espeak
   ```

2. **Create a Virtual Environment**:
   ```
   mkdir AI_Voice_Assistant
   cd AI_Voice_Assistant
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Packages**:
   ```
   pip install -r requirements.txt
   ```

4. **Download the Voice Assistant Code**:
   - Copy the `voice_assistant.py` file to your project directory

5. **Run the Assistant**:
   ```
   python voice_assistant.py
   ```

## Configuration

### API Keys

The assistant uses several APIs for enhanced functionality:

#### config.json

The application looks for a `config.json` file in the same directory as the script. This file stores your API keys.

#### Hugging Face API

A Hugging Face API key is already included in the config.json file when you first run the application.

#### OpenAI API (Optional)

For enhanced capabilities:
1. Create an account on [OpenAI](https://platform.openai.com/signup)
2. Get your API key from the dashboard
3. Add it to the config.json file or set it as an environment variable named `OPENAI_API_KEY`

#### OpenWeatherMap API (Optional)

For weather data:
1. Go to [OpenWeatherMap](https://openweathermap.org/) and create a free account
2. After signing up, go to your API keys section
3. Copy your API key
4. Add it to the config.json file or set it as an environment variable named `OPENWEATHER_API_KEY`

### Voice Settings

The voice assistant automatically selects the best voice for your platform:

- **On macOS**: It looks for the "Samantha" voice
- **On Windows**: It tries to find a female voice
- **On Linux**: It uses the default espeak voice

You can customize the voice by modifying the `init_tts_engine()` function in the code:

```python
# For macOS, look for a different voice
if "Alex" in voice.name:  # Change "Samantha" to "Alex" or another voice
    engine.setProperty('voice', voice.id)
    break
```

## Usage Guide

### Available Commands

- **Weather Information**: "What's the weather in [location]?"
- **Time and Date**: "What time is it?" / "What's today's date?"
- **Factual Questions**: "Who is the President of [country]?" / "What's the capital of [country]?"
- **Help**: "Help" or "What can you do?"
- **Command History**: "History" or "Show history"
- **Repeat**: "Repeat" or "Say that again"
- **Exit**: "Exit", "Quit", or "Stop"

### Example Queries

#### Weather
- "What's the weather in New York?"
- "Tell me the temperature in Tokyo"

#### Time and Date
- "What time is it?"
- "What day is today?"

#### Factual Information
- "Who is the President of the United States?"
- "What is the capital of France?"
- "How many people live in India?"
- "What's the latest iPhone model?"
- "Who is the CEO of Apple?"

#### General Knowledge
- "Who is Albert Einstein?"
- "How do computers work?"

## Troubleshooting

### Speech Recognition Issues

- **Problem**: Assistant doesn't understand your speech
- **Solution**: Speak clearly in a quiet environment, ensure your microphone is working properly

### Text-to-Speech Issues

- **Problem**: No voice output on macOS
- **Solution**: Check if you have voices installed in System Preferences > Accessibility > Speech

- **Problem**: Voice sounds robotic or unnatural
- **Solution**: Try adjusting the rate and volume settings in the `init_tts_engine()` function

### API Issues

- **Problem**: LLM API responses are inaccurate or slow
- **Solution**: Check your API keys and internet connection. The assistant will fall back to its built-in knowledge base for common questions.

- **Problem**: Weather information not working
- **Solution**: Check your OpenWeatherMap API key or internet connection. The assistant will try a free web service as a fallback.

## Recent Changes and Improvements

### LLM API Integration
- Added Hugging Face API integration for powerful language models
- Added OpenAI API support as an optional enhancement
- Implemented fallback mechanisms when APIs aren't available

### Factual Knowledge Database
- Added comprehensive database of factual information
- Improved accuracy for questions about world leaders, populations, and capitals
- Added technology, company, and space exploration information

### Speech Recognition Enhancements
- Added visual indicators while listening
- Improved ambient noise handling
- Added multiple recognition services for better accuracy

### Text-to-Speech Improvements
- Platform-specific voice settings for better quality
- Fixed runtime errors on macOS
- Added threading for non-blocking speech on Windows/Linux

### Weather Integration
- Added OpenWeatherMap API integration
- Added fallback to wttr.in web API
- Improved location extraction from questions

### User Interface Upgrades
- Added command history feature
- Implemented help command
- Added repeat functionality
- Improved error handling and recovery

---

This documentation was updated on May 2, 2025.
