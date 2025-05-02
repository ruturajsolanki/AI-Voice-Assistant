# AI Voice Assistant Installation Guide

This guide provides detailed, step-by-step instructions for installing the AI Voice Assistant on Windows, macOS, and Linux systems.

## Quick Start

For experienced users, here's the quick installation process:

```bash
# Clone or download the repository
# Navigate to the project directory
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python voice_assistant.py
```

## Detailed Installation Instructions

### Windows Installation

1. **Install Python**:
   - Download Python 3.7 or newer from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation by opening Command Prompt and typing:
     ```
     python --version
     ```

2. **Create Project Directory**:
   - Create a folder for the project:
     ```
     mkdir AI_Voice_Assistant
     cd AI_Voice_Assistant
     ```

3. **Set Up Virtual Environment**:
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate the virtual environment:
     ```
     venv\Scripts\activate
     ```
   - You should see `(venv)` at the beginning of your command prompt line

4. **Install Dependencies**:
   - Install all required packages using the requirements file:
     ```
     pip install -r requirements.txt
     ```
   - If PyAudio installation fails, download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it:
     ```
     pip install [path-to-downloaded-wheel-file]
     ```

5. **Run the Voice Assistant**:
   - Run the Python script:
     ```
     python voice_assistant.py
     ```

### macOS Installation

1. **Install Python**:
   - Download Python 3.7 or newer from [python.org](https://www.python.org/downloads/mac-osx/)
   - Or use Homebrew:
     ```
     brew install python
     ```
   - Verify installation:
     ```
     python3 --version
     ```

2. **Install System Dependencies**:
   - Install PortAudio (required for PyAudio):
     ```
     brew install portaudio
     ```

3. **Create Project Directory**:
   - Create a folder for the project:
     ```
     mkdir AI_Voice_Assistant
     cd AI_Voice_Assistant
     ```

4. **Set Up Virtual Environment**:
   - Create a virtual environment:
     ```
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     ```
     source venv/bin/activate
     ```
   - You should see `(venv)` at the beginning of your command prompt line

5. **Install Dependencies**:
   - Install all required packages:
     ```
     pip install -r requirements.txt
     ```
   - If you encounter issues with PyAudio, try:
     ```
     pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
     ```

6. **Run the Voice Assistant**:
   - Run the Python script:
     ```
     python voice_assistant.py
     ```

### Linux Installation (Ubuntu/Debian)

1. **Install Python and System Dependencies**:
   - Update package lists:
     ```
     sudo apt-get update
     ```
   - Install Python and development tools:
     ```
     sudo apt-get install python3 python3-pip python3-venv
     ```
   - Install audio dependencies:
     ```
     sudo apt-get install portaudio19-dev python3-pyaudio
     ```
   - Install text-to-speech engine:
     ```
     sudo apt-get install espeak
     ```

2. **Create Project Directory**:
   - Create a folder for the project:
     ```
     mkdir AI_Voice_Assistant
     cd AI_Voice_Assistant
     ```

3. **Set Up Virtual Environment**:
   - Create a virtual environment:
     ```
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     ```
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   - Install all required packages:
     ```
     pip install -r requirements.txt
     ```

5. **Run the Voice Assistant**:
   - Run the Python script:
     ```
     python voice_assistant.py
     ```

## Troubleshooting Common Installation Issues

### PyAudio Installation Problems

#### Windows:
- Error: `Microsoft Visual C++ 14.0 is required`
  - Solution: Install Visual C++ Build Tools from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - Alternative: Install pre-compiled wheel from [Christoph Gohlke's site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

#### macOS:
- Error: `fatal error: 'portaudio.h' file not found`
  - Solution: Install portaudio with Homebrew and try again:
    ```
    brew install portaudio
    pip install pyaudio
    ```

#### Linux:
- Error: `No module named 'pyaudio'`
  - Solution: Install system packages:
    ```
    sudo apt-get install python3-pyaudio
    ```
  - Or install development packages and then pyaudio:
    ```
    sudo apt-get install portaudio19-dev
    pip install pyaudio
    ```

### Text-to-Speech Issues

#### macOS:
- If no voice output, check System Preferences > Accessibility > Speech to ensure voices are installed

#### Linux:
- If espeak is not working, try installing festival:
  ```
  sudo apt-get install festival
  ```

## Verifying Installation

To verify that all components are working correctly:

1. **Test Speech Recognition**:
   ```python
   import speech_recognition as sr
   r = sr.Recognizer()
   with sr.Microphone() as source:
       print("Say something!")
       audio = r.listen(source)
   try:
       print("You said: " + r.recognize_google(audio))
   except sr.UnknownValueError:
       print("Google Speech Recognition could not understand audio")
   ```

2. **Test Text-to-Speech**:
   ```python
   import pyttsx3
   engine = pyttsx3.init()
   engine.say("Hello World")
   engine.runAndWait()
   ```

3. **Test Weather API** (if configured):
   ```python
   import pyowm
   owm = pyowm.OWM('your_api_key')
   mgr = owm.weather_manager()
   observation = mgr.weather_at_place('London,GB')
   w = observation.weather
   print(w.detailed_status)
   ```

## Next Steps

After successful installation:

1. Get an OpenWeatherMap API key (optional but recommended)
2. Configure the voice assistant by editing the API key in the code
3. Explore the available commands in the [DOCUMENTATION.md](DOCUMENTATION.md) file

---

If you encounter any issues not covered in this guide, please refer to the official documentation for each package or create an issue in the project repository.
