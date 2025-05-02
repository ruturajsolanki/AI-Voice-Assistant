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
   - If torch installation takes too long, you can install a CPU-only version:
     ```
     pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
     ```

5. **Set Up Configuration**:
   - A default config.json file will be created on first run
   - You can add your own API keys for enhanced functionality

6. **Run the Voice Assistant**:
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
   - For Apple Silicon Macs (M1/M2/M3), use native torch:
     ```
     pip install torch torchvision torchaudio
     ```

6. **Set Up Configuration**:
   - A default config.json file will be created on first run
   - You can add your own API keys for enhanced functionality

7. **Run the Voice Assistant**:
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

5. **Set Up Configuration**:
   - A default config.json file will be created on first run
   - You can add your own API keys for enhanced functionality

6. **Run the Voice Assistant**:
   - Run the Python script:
     ```
     python voice_assistant.py
     ```

## Configuration Setup

### API Keys

The assistant uses several APIs that require keys:

#### Hugging Face API
A default key is provided in the config.json file when first run.

#### OpenAI API (Optional)
For enhanced capabilities:
1. Create an account on [OpenAI](https://platform.openai.com/signup)
2. Get your API key from the dashboard
3. Add it to the config.json file or set it as an environment variable:

```bash
# On Windows (Command Prompt)
set OPENAI_API_KEY=your_api_key_here

# On Windows (PowerShell)
$env:OPENAI_API_KEY="your_api_key_here"

# On macOS/Linux
export OPENAI_API_KEY=your_api_key_here
```

#### OpenWeatherMap API (Optional)
1. Go to [OpenWeatherMap](https://openweathermap.org/) and create a free account
2. After signing up, go to your API keys section
3. Copy your API key
4. Add it to the config.json file or set it as an environment variable:

```bash
# On Windows (Command Prompt)
set OPENWEATHER_API_KEY=your_api_key_here

# On Windows (PowerShell)
$env:OPENWEATHER_API_KEY="your_api_key_here"

# On macOS/Linux
export OPENWEATHER_API_KEY=your_api_key_here
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

### Torch/Transformers Installation Issues

- Error: Torch installation is too slow or uses too much disk space
  - Solution: Install CPU-only version which is smaller:
    ```
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    ```

- Error: "No module named 'transformers'"
  - Solution: Install just the transformers package:
    ```
    pip install transformers
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

1. **Check API Status**:
   The voice assistant will display API status at startup:
   ```
   API Status:
   - OpenAI API: Available
   - Hugging Face API: Available ✓
   - Weather API: Available
   ```

2. **Test Speech Recognition**:
   The assistant will listen when started. Say something like "Hello" to test.

3. **Test API Functionality**:
   Ask a factual question like "Who is the President of the United States?"
   This will test the factual knowledge database and LLM API integration.

4. **Test Weather Information**:
   Ask "What's the weather in New York?" to test weather API functionality.

---

If you encounter any issues not covered in this guide, please refer to the official documentation for each package or check the troubleshooting section in the [DOCUMENTATION.md](DOCUMENTATION.md) file.
