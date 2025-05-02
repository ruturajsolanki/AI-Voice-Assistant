import speech_recognition as sr
import requests
import time
import json
import os
import re
import threading
import datetime
import platform

# Try to import TTS libraries with fallbacks
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    print("Text-to-speech module not available. Using text-only mode.")
    TTS_AVAILABLE = False

# Try to import weather libraries with fallbacks
try:
    import pyowm
    from pyowm.utils import config
    from pyowm.utils import timestamps
    WEATHER_API_AVAILABLE = True
except ImportError:
    print("Weather API module not available. Weather functionality will be limited.")
    WEATHER_API_AVAILABLE = False

# Global TTS engine
tts_engine = None
tts_lock = threading.Lock()

# Command history
command_history = []
MAX_HISTORY = 10

def init_tts_engine():
    """Initialize the text-to-speech engine with simpler settings that work on macOS"""
    global tts_engine
    
    if not TTS_AVAILABLE:
        return None
        
    try:
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        
        # Detect OS for platform-specific settings
        system = platform.system()
        
        if system == 'Darwin':  # macOS
            # On macOS, just set a voice that's known to work well
            # We'll avoid pitch adjustments which cause the "not supported" message
            for voice in voices:
                if "Samantha" in voice.name:
                    engine.setProperty('voice', voice.id)
                    break
            
            # Only adjust rate on macOS (safer option)
            engine.setProperty('rate', 175)  # Default is 200
            
        else:  # Windows, Linux, etc.
            # More extensive voice customization on other platforms
            selected_voice = None
            for voice in voices:
                voice_name = voice.name.lower()
                if "female" in voice_name:
                    selected_voice = voice.id
                    break
                    
            if selected_voice:
                engine.setProperty('voice', selected_voice)
                
            # Set properties for more natural speech
            engine.setProperty('rate', 165)
            engine.setProperty('volume', 0.9)
            
            # Try pitch adjustment on non-macOS platforms
            try:
                engine.setProperty('pitch', 1.05)
            except:
                pass
                
        return engine
    except Exception as e:
        print(f"Error initializing text-to-speech: {e}")
        return None

def speak(text):
    """
    Convert text to speech and speak it safely.
    Uses a simpler approach that works reliably on macOS.
    """
    print(f"AI: {text}")
    
    if not TTS_AVAILABLE or not tts_engine:
        return
    
    # Define a function to run in a thread
    def speak_text():
        try:
            # For macOS, we need to be extra careful with the speech engine
            if platform.system() == 'Darwin':
                # Simple approach for macOS - avoid using runAndWait() multiple times
                tts_engine.say(text)
                tts_engine.runAndWait()
            else:
                # For other platforms, use the thread-safe approach with locks
                with tts_lock:
                    tts_engine.say(text)
                    tts_engine.runAndWait()
        except RuntimeError as e:
            if "run loop already started" in str(e):
                # This happens on macOS - just ignore it
                pass
            else:
                print(f"TTS Runtime Error: {e}")
        except Exception as e:
            print(f"TTS Error: {e}")
    
    # For macOS, don't use threading as it causes issues with the speech engine
    if platform.system() == 'Darwin':
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            # Just print the error but continue
            print(f"MacOS TTS Error: {e}")
    else:
        # For other platforms, use threading
        threading.Thread(target=speak_text).start()

def listen():
    """
    Listen for voice input with improved recognition settings.
    Shows a visual indicator while listening.
    """
    recognizer = sr.Recognizer()
    
    # Adjust recognition parameters for better results
    recognizer.energy_threshold = 300  # Default is 300, lower for more sensitivity
    recognizer.dynamic_energy_threshold = True  # Adjusts for ambient noise
    recognizer.pause_threshold = 0.8  # Default is 0.8, shorter for faster response
    
    with sr.Microphone() as source:
        # Visual indicator that we're listening
        print("🎤 Speak your request: ", end="", flush=True)
        
        # Show listening animation
        listen_thread = threading.Thread(target=show_listening_animation)
        listen_thread.daemon = True
        listen_thread.start()
        
        # Adjust for ambient noise to improve recognition
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            # Listen with timeout
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            
            # Stop the animation
            global listening_active
            listening_active = False
            time.sleep(0.2)  # Give time for animation to stop
            print("\r" + " " * 50 + "\r", end="", flush=True)  # Clear the animation
            
            # Try multiple recognition services for better results
            text = try_multiple_recognition_services(recognizer, audio)
            
            if text:
                print(f"📝 You said: {text}")
                add_to_history(text)
                return text
            else:
                print("Sorry, I could not understand your speech. Please try again.")
                speak("Sorry, I could not understand your speech. Please try again.")
                return None
                
        except sr.UnknownValueError:
            # Stop the animation if it's still running
            listening_active = False
            time.sleep(0.2)
            print("\r" + " " * 50 + "\r", end="", flush=True)  # Clear the animation
            
            print("Sorry, I could not understand your speech. Please try again.")
            speak("Sorry, I could not understand your speech. Please try again.")
            return None
        except sr.RequestError:
            # Stop the animation if it's still running
            listening_active = False
            time.sleep(0.2)
            print("\r" + " " * 50 + "\r", end="", flush=True)  # Clear the animation
            
            print("Sorry, there was an error with the speech recognition service.")
            speak("Sorry, there was an error with the speech recognition service.")
            return None
        except Exception as e:
            # Stop the animation if it's still running
            listening_active = False
            time.sleep(0.2)
            print("\r" + " " * 50 + "\r", end="", flush=True)  # Clear the animation
            
            print(f"An unexpected error occurred: {str(e)}")
            speak("An unexpected error occurred. Please try again.")
            return None

# Global variable for the listening animation
listening_active = False

def show_listening_animation():
    """Show an animation while listening for voice input"""
    global listening_active
    listening_active = True
    animation = "|/-\\"
    idx = 0
    
    while listening_active:
        print(f"\r🎤 Listening {animation[idx % len(animation)]}", end="", flush=True)
        idx += 1
        time.sleep(0.1)

def try_multiple_recognition_services(recognizer, audio):
    """Try multiple speech recognition services for better results"""
    # First try Google (most reliable)
    try:
        return recognizer.recognize_google(audio)
    except:
        pass
    
    # If Google fails, try Sphinx (offline, less accurate but works without internet)
    try:
        return recognizer.recognize_sphinx(audio)
    except:
        # Sphinx might not be installed, so we'll just pass if it fails
        pass
    
    # If all services fail, return None
    return None

def add_to_history(command):
    """Add a command to the history"""
    global command_history
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    command_history.append((timestamp, command))
    
    # Keep only the most recent commands
    if len(command_history) > MAX_HISTORY:
        command_history.pop(0)

def get_weather_via_api(location):
    """
    Get weather information for a location using OpenWeatherMap API.
    """
    if not WEATHER_API_AVAILABLE:
        return None
        
    try:
        # You need to get your own API key from https://openweathermap.org/api
        # Replace this with your actual API key
        api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your API key
        
        # Initialize OpenWeatherMap client
        owm = pyowm.OWM(api_key)
        mgr = owm.weather_manager()
        
        # Search for current weather in the location
        observation = mgr.weather_at_place(location)
        w = observation.weather
        
        # Get temperature in Celsius
        temp = w.temperature('celsius')
        temp_current = temp['temp']
        temp_feel = temp['feels_like']
        
        # Get weather details
        status = w.detailed_status
        humidity = w.humidity
        wind_speed = w.wind()['speed']
        
        # Format the response in a more conversational way
        weather_info = f"In {location}, it's currently {status}. "
        weather_info += f"The temperature is {temp_current:.1f} degrees Celsius, but it feels like {temp_feel:.1f}. "
        
        # Add more details in a natural way
        if humidity > 80:
            weather_info += f"It's quite humid at {humidity} percent. "
        elif humidity < 30:
            weather_info += f"It's very dry with only {humidity} percent humidity. "
        else:
            weather_info += f"Humidity is at {humidity} percent. "
            
        if wind_speed > 10:
            weather_info += f"And it's pretty windy with winds at {wind_speed} meters per second."
        elif wind_speed < 2:
            weather_info += f"There's barely any wind, just {wind_speed} meters per second."
        else:
            weather_info += f"With a gentle breeze of {wind_speed} meters per second."
        
        return weather_info
    except Exception as e:
        print(f"Error with OpenWeatherMap API: {e}")
        return None

def get_weather_via_web(location):
    """
    Fallback method to get weather information using a web API that doesn't require a key.
    """
    try:
        # Using wttr.in which doesn't require an API key
        encoded_location = location.replace(" ", "+")
        url = f"https://wttr.in/{encoded_location}?format=j1"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Extract current weather
            current = data.get("current_condition", [{}])[0]
            temp_c = current.get("temp_C", "unknown")
            feels_like = current.get("FeelsLikeC", "unknown")
            weather_desc = current.get("weatherDesc", [{}])[0].get("value", "unknown")
            humidity = current.get("humidity", "unknown")
            wind_speed = current.get("windspeedKmph", "unknown")
            
            # Format the response in a more conversational way
            weather_info = f"In {location}, it's currently {weather_desc}. "
            weather_info += f"The temperature is {temp_c} degrees Celsius, but it feels like {feels_like}. "
            
            # Add more details in a natural way
            try:
                humidity_val = int(humidity)
                if humidity_val > 80:
                    weather_info += f"It's quite humid at {humidity} percent. "
                elif humidity_val < 30:
                    weather_info += f"It's very dry with only {humidity} percent humidity. "
                else:
                    weather_info += f"Humidity is at {humidity} percent. "
            except:
                weather_info += f"Humidity is at {humidity} percent. "
                
            try:
                wind_val = float(wind_speed)
                if wind_val > 20:
                    weather_info += f"And it's very windy with winds at {wind_speed} kilometers per hour."
                elif wind_val < 5:
                    weather_info += f"There's barely any wind, just {wind_speed} kilometers per hour."
                else:
                    weather_info += f"With a gentle breeze of {wind_speed} kilometers per hour."
            except:
                weather_info += f"Wind speed is {wind_speed} kilometers per hour."
            
            return weather_info
        else:
            return None
    except Exception as e:
        print(f"Error with web weather API: {e}")
        return None

def get_weather(location):
    """
    Get weather information using available methods.
    """
    # Try the OpenWeatherMap API first
    weather_info = get_weather_via_api(location)
    
    # If that fails, try the web API
    if not weather_info:
        weather_info = get_weather_via_web(location)
    
    # If all methods fail, return a helpful message
    if not weather_info:
        return f"I'm sorry, I couldn't retrieve weather information for {location}. Please check the location name or try again later."
    
    return weather_info

def extract_location(question):
    """
    Extract location from a weather-related question.
    """
    # Try to find "in [location]" pattern
    in_match = re.search(r'in\s+([a-zA-Z\s,]+)(?:\?|$)', question)
    if in_match:
        return in_match.group(1).strip()
    
    # Try to find "for [location]" pattern
    for_match = re.search(r'for\s+([a-zA-Z\s,]+)(?:\?|$)', question)
    if for_match:
        return for_match.group(1).strip()
    
    # Try to find location after weather keywords
    weather_keywords = ["weather", "temperature", "forecast", "rain", "sunny", "cloudy"]
    for keyword in weather_keywords:
        if keyword in question.lower():
            parts = question.lower().split(keyword)
            if len(parts) > 1 and parts[1].strip():
                # Clean up the location text
                location = parts[1].strip()
                location = re.sub(r'^(in|at|for|of)\s+', '', location)
                location = re.sub(r'\?.*$', '', location)
                return location.strip()
    
    return None

def process_command(user_input):
    """
    Process special commands and return True if it was a special command.
    """
    if user_input.lower() in ["exit", "quit", "stop"]:
        goodbye_message = "Goodbye! Have a wonderful day!"
        print(f"AI: {goodbye_message}")
        
        # Speak goodbye without waiting for completion
        if TTS_AVAILABLE and tts_engine:
            try:
                tts_engine.say(goodbye_message)
                tts_engine.runAndWait()
            except:
                pass
        
        return True
    
    # Check for history command
    if user_input.lower() in ["history", "show history", "command history"]:
        if not command_history:
            speak("You haven't made any requests yet.")
        else:
            print("\n=== Command History ===")
            for i, (timestamp, cmd) in enumerate(command_history, 1):
                print(f"{i}. [{timestamp}] {cmd}")
            print("=====================\n")
            speak("I've displayed your command history on the screen.")
        return True
    
    # Check for repeat command
    if user_input.lower().startswith("repeat") or user_input.lower() == "say that again":
        if not command_history:
            speak("There's nothing to repeat yet.")
        else:
            # Get the last command
            _, last_command = command_history[-1]
            print(f"Repeating: {last_command}")
            
            # Process the last command again
            print("🤖 Thinking...")
            ai_response = ask_ai(last_command)
            speak(ai_response)
        return True
    
    # Check for help command
    if user_input.lower() in ["help", "commands", "what can you do"]:
        help_message = """
I can help you with several things:
- Weather information: Ask about the weather in any location
- Time and date: Ask for the current time or date
- General questions: I'll try to answer any question you have
- Command history: Say "history" to see your previous commands
- Repeat: Say "repeat" or "say that again" to repeat the last response

You can also say "exit", "quit", or "stop" to end our conversation.
        """
        print(help_message)
        speak("I've displayed a list of commands I can help you with on the screen.")
        return True
        
    # Not a special command
    return False

def ask_ai(question):
    """
    Send a question to an AI model and get a response using a reliable API.
    """
    # Check if it's a weather-related question
    weather_keywords = ["weather", "temperature", "forecast", "rain", "sunny", "cloudy", "humidity", "hot", "cold", "warm"]
    is_weather_question = any(keyword in question.lower() for keyword in weather_keywords)
    
    if is_weather_question:
        # Extract location from the question
        location = extract_location(question)
        if location:
            return get_weather(location)
        else:
            return "To get weather information, please specify a location. For example, you can ask me 'What's the weather like in Mumbai?'"
    
    # First try using a simple knowledge base for common questions
    answer = get_knowledge_base_answer(question)
    if answer:
        return answer
        
    # If not in knowledge base, use a more direct approach
    return get_direct_answer(question)

def get_knowledge_base_answer(question):
    """
    Check if the question can be answered from our local knowledge base.
    """
    question_lower = question.lower()
    
    # Simple knowledge base for common questions with more conversational responses
    knowledge_base = {
        "temperature": "If you'd like to know the temperature somewhere, just ask me about the weather in a specific place. For example, 'What's the temperature in New York?'",
        "weather": "I'd be happy to tell you about the weather. Just let me know which location you're interested in, like 'What's the weather in Mumbai?'",
        "time": f"It's currently {time.strftime('%I:%M %p')}.",
        "date": f"Today is {time.strftime('%A, %B %d, %Y')}.",
        "name": "I'm your AI voice assistant, designed to help answer your questions and make your day a little easier.",
        "created": "I was created as a Python-based voice assistant project. I'm constantly learning and improving!",
        "hello": "Hello there! How can I help you today?",
        "hi": "Hi! What can I do for you?",
        "how are you": "I'm doing well, thanks for asking! How about you?",
        "thank you": "You're very welcome! Is there anything else I can help with?",
        "thanks": "You're welcome! Let me know if you need anything else."
    }
    
    # Check for exact matches first
    for key, value in knowledge_base.items():
        if key in question_lower:
            return value
    
    # No match found
    return None

def get_direct_answer(question):
    """
    Get a direct answer to a question using various methods.
    """
    try:
        # Method 1: Try using a simple web search API (SerpAPI alternative)
        search_answer = get_search_answer(question)
        if search_answer:
            return search_answer
            
        # Method 2: Try using a pre-defined response based on question type
        return get_question_type_response(question)
            
    except Exception as e:
        print(f"Error getting answer: {str(e)}")
        return "I'm sorry, I couldn't find an answer to that question right now."

def get_search_answer(question):
    """
    Try to get an answer using a search API.
    This is a simplified version that doesn't require an API key.
    """
    try:
        # Using DuckDuckGo API (doesn't require authentication)
        encoded_question = question.replace(" ", "+")
        url = f"https://api.duckduckgo.com/?q={encoded_question}&format=json"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Check for an abstract (summary)
            if data.get("Abstract"):
                return data["Abstract"]
                
            # Check for an answer
            if data.get("Answer"):
                return data["Answer"]
                
            # Check for related topics
            if data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
                return data["RelatedTopics"][0]["Text"]
        
        return None
    except:
        return None

def get_question_type_response(question):
    """
    Generate a response based on the type of question.
    More conversational and human-like responses.
    """
    question_lower = question.lower()
    
    # Dictionary of informative responses by question type
    if question_lower.startswith("who"):
        return "I don't have specific information about who you're asking about. I wish I could tell you more, but my knowledge is limited. You might find better information on Wikipedia or a similar site."
        
    elif question_lower.startswith("what"):
        return "That's an interesting question! I don't have specific information about what you're asking, but I'd recommend checking a search engine for the most up-to-date information."
        
    elif question_lower.startswith("when"):
        return "I don't have access to historical or scheduling information to answer when questions accurately. A quick web search might give you the exact date or time you're looking for."
        
    elif question_lower.startswith("where"):
        return "I don't have access to location data to answer where questions accurately. Google Maps or a similar service would be perfect for finding this location."
        
    elif question_lower.startswith("why"):
        return "That's a thoughtful question about why something happened or exists. Unfortunately, I don't have the contextual understanding to explain it properly. This would require specialized knowledge about the subject."
        
    elif question_lower.startswith("how"):
        return "That's a great question about how to do something. I don't have detailed procedural knowledge on this specific topic, but you might find step-by-step guides online that can walk you through it."
    
    # Default response
    return "That's an interesting question! I don't have enough information to give you a complete answer, but I'd be happy to help with something else."

def print_welcome_banner():
    """Print a nicer welcome banner"""
    banner = """
╔════════════════════════════════════════════════════╗
║                                                    ║
║               AI VOICE ASSISTANT                   ║
║                                                    ║
╚════════════════════════════════════════════════════╝
    """
    print(banner)
    print("Ask me anything! Say 'help' for a list of commands.")
    print("Say 'exit', 'quit', or 'stop' to end the conversation.\n")

def test_tts():
    """Test if text-to-speech is working properly"""
    if TTS_AVAILABLE and tts_engine:
        print("Testing text-to-speech...")
        try:
            tts_engine.say("Text to speech is working properly.")
            tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"TTS test failed: {e}")
            return False
    else:
        print("Text-to-speech is not available.")
        return False

def main():
    # Initialize the TTS engine at startup
    global tts_engine
    tts_engine = init_tts_engine()
    
    # Print welcome banner
    print_welcome_banner()
    
    # Test TTS functionality
    tts_working = test_tts()
    
    # Welcome message
    welcome_message = "Hello! I'm your AI voice assistant. How can I help you today?"
    print(f"AI: {welcome_message}")
    
    if tts_working:
        # If TTS is working, speak the welcome message
        try:
            tts_engine.say(welcome_message)
            tts_engine.runAndWait()
        except Exception as e:
            print(f"Error with welcome message TTS: {e}")
    
    # Small delay to ensure welcome message is spoken
    time.sleep(1)
    
    while True:
        try:
            user_input = listen()
            if user_input:
                # Check if it's a special command
                if process_command(user_input):
                    # If it was a special command and process_command returned True,
                    # we've already handled it, so continue to the next iteration
                    if user_input.lower() in ["exit", "quit", "stop"]:
                        break
                    continue
                
                print("🤖 Thinking...")
                ai_response = ask_ai(user_input)
                speak(ai_response)
                
                # Small delay to ensure the response is fully spoken
                time.sleep(0.5)
                
            # Small pause to prevent CPU overuse
            time.sleep(0.2)
            
        except KeyboardInterrupt:
            print("\nExiting voice assistant. Goodbye!")
            
            # Try to speak goodbye, but don't wait if it fails
            try:
                if TTS_AVAILABLE and tts_engine:
                    tts_engine.say("Goodbye!")
                    tts_engine.runAndWait()
            except:
                pass
                
            break
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            speak("I encountered a problem. Let's try again.")
            print("Continuing...")

if __name__ == "__main__":
    main()