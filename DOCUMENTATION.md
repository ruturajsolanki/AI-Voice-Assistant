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
   - [OpenWeatherMap API](#openweathermap-api)
   - [Voice Settings](#voice-settings)
5. [Usage Guide](#usage-guide)
   - [Available Commands](#available-commands)
   - [Example Queries](#example-queries)
6. [Troubleshooting](#troubleshooting)
7. [Recent Changes and Improvements](#recent-changes-and-improvements)

## Overview

The AI Voice Assistant is a Python-based application that can understand spoken commands, answer questions, provide weather information, and more. It uses speech recognition to convert your voice to text, processes your requests, and responds both in text and with synthesized speech.

## Features

- **Voice Recognition**: Listens to your spoken questions and commands
- **Text-to-Speech**: Speaks responses out loud with a natural-sounding voice
- **Weather Information**: Gets current weather for any location worldwide
- **General Knowledge**: Answers a variety of questions using web searches
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
   pip install SpeechRecognition pyttsx3 pyaudio requests pyowm
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
   pip install SpeechRecognition pyttsx3 pyaudio requests pyowm setuptools
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
   pip install SpeechRecognition pyttsx3 pyaudio requests pyowm
   ```

4. **Download the Voice Assistant Code**:
   - Copy the `voice_assistant.py` file to your project directory

5. **Run the Assistant**:
   ```
   python voice_assistant.py
   ```

## Configuration

### OpenWeatherMap API

To use the weather functionality with OpenWeatherMap:

1. Sign up for a free account at [OpenWeatherMap](https://home.openweathermap.org/users/sign_up)
2. After signing up, go to your API keys section
3. Copy your API key
4. Open the `voice_assistant.py` file and replace `YOUR_OPENWEATHERMAP_API_KEY` with your actual key

```python
# Find this line in the code
api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your API key
```

Note: Even without the API key, the assistant will still work using the wttr.in web service as a fallback.

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
- **Time**: "What time is it?"
- **Date**: "What's today's date?"
- **Help**: "Help" or "What can you do?"
- **Command History**: "History" or "Show history"
- **Repeat**: "Repeat" or "Say that again"
- **Exit**: "Exit", "Quit", or "Stop"

### Example Queries

- "What's the weather in New York?"
- "Tell me the temperature in Tokyo"
- "What time is it?"
- "Who is Albert Einstein?"
- "How do computers work?"
- "What is the capital of France?"

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

- **Problem**: Weather information not working
- **Solution**: Check your OpenWeatherMap API key or internet connection

## Recent Changes and Improvements

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

### Code Structure
- Better error handling throughout
- Platform detection for OS-specific optimizations
- More robust API integration

---

This documentation was created on May 2, 2025.
