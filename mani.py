import requests
from datetime import datetime  # Corrected import for the datetime class
import os
import re
import shutil  # For regular expressions
import psutil
import pyautogui
import pytz
import speech_recognition as sr  # Speech recognition library
import pyttsx3  # Text-to-speech conversion
import subprocess
import webbrowser
from playsound import playsound
import google.generativeai as genai
from openmanager import open_application
from tqdm import tqdm
from downloadlinks import download_links
genai.configure(api_key=os.environ.get("API_KEY", "AIzaSyAHR-VibLkLg15S99FvIWjr26UjeRz9dPQ"))# Import the API key from config


# Initialize the text-to-speech engine
tts_engine = pyttsx3.init()

# Function to make Jarvis speak
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Initialize the recognizer
recognizer = sr.Recognizer()


# Function to take voice input and convert it to text with noise handling
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Reduce ambient noise adjustment time
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)  # Add timeout to avoid hanging

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()  # Convert to lowercase for easier command processing
    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said. Please try again.")
        return ""
    except sr.RequestError:
        speak("Sorry, I'm having trouble connecting to the speech recognition service.")
        return ""
    except sr.WaitTimeoutError:
        speak("Listening timed out. Please try again.")
        return ""


# Function to respond to specific commands
def respond(command):

    user_input = None
    # Remove any trigger word like "Jarvis"
    command = re.sub(r"\bjarvis\b", "", command).strip()
    if "push to github" in command:
        speak("Pushing code to GitHub.")
        result = git_push()
        speak(result)
        return False
    elif command.startswith("ask gemini"):
        question = command.replace("ask gemini", "").strip()  # Remove "ask gemini" from the command
        speak(f"Let me ask Gemini: {question}.")
        result = ask_gemini(question)  # Ask the Gemini AI the question
        print(result)  # Print the response from Gemini to the console
         # Make Jarvis speak the response
        return False
    
    # Command for committing with a voice message
    elif "commit" in command and "message" in command:
        match = re.search(r"commit with message\s+['\"]?(.*?)['\"]?$", command)
        if match:
            commit_message = match.group(1)
            speak(f"Committing changes with message: {commit_message}")
            result = git_commit(commit_message)
            speak(result)
        return False

    # Command for adding changes
    elif "add changes" in command:
        speak("Adding all changes.")
        result = git_add()
        speak(result)
        return False
    
    # Handle greetings and inquiries
    elif re.search(r"(hello|hi|hey)", command):
        speak("Hello! How can I assist you today?")
        return False
    elif re.search(r"(your name|who are you)", command):
        speak("I am Jarvis, your personal assistant.")
        return False
    elif command.startswith("download "):
        software_name = command.replace("download ", "").strip().lower()
        if software_name in download_links:
            speak(f"Opening the download page for {software_name}.")
            webbrowser.open(download_links[software_name])
        else:
            speak(f"Sorry, I don't have a download link for {software_name}.")
        return False
    # Time commands
    elif re.search(r"time in (india|usa|uk|canada)", command):
        country = re.search(r"(india|usa|uk|canada)", command).group(0)
        current_time = get_current_time(country.upper())
        speak(f"The current time in {country.capitalize()} is {current_time}.")
        return False

    # Open applications
    elif re.search(r"(open|start|launch)\s+(notepad|chrome|calculator|word|settings|crop|files|d drive|e drive|c drive|g drive|f drive|ms store|edge|ms teams|mail|fire fox|brave|task manager)", command):
        app_name = re.search(
            r"(notepad|chrome|calculator|word|settings|crop|files|d drive|e drive|c drive|g drive|f drive|ms store|edge|ms teams|mail|fire fox|brave|task manager)", command).group(0)
        speak(f"Opening {app_name}.")
        open_application(app_name)
        return False
    

    # Open websites
    elif re.search(r"go to\s+(.*\..*)", command):
        website_name = re.search(r"go to\s+(.*\..*)", command).group(1)
        speak(f"Opening {website_name}.")
        open_website(website_name)
        return False

    # Write text in Notepad
    elif re.search(r"copy\s+(.*)", command):
        text_to_write = re.search(r"copy\s+(.*)", command).group(1)
        speak(f"Writing '{text_to_write}' in Notepad.")
        write_in_notepad(text_to_write)
        return False

    # Close applications
    elif re.search(r"close\s+(.*)", command):
        app_name = re.search(r"close\s+(.*)", command).group(1)
        speak(f"Closing {app_name}.")
        close_application(app_name)
        return False

    # Create a folder command
    elif re.search(r"create a folder\s+(.*)", command):
        folder_name = re.search(r"create a folder\s+(.*)", command).group(1)
        create_folder(folder_name)
        return False

    # Delete a folder command
    match_delete = re.search(r"delete a folder\s+['\"]?(.+?)['\"]?$", command)
    if match_delete:
        folder_name = match_delete.group(1)
        delete_folder(folder_name)
        return False

    # Sleep computer
    elif 'exit' in command or 'sleep' in command:
        speak("Putting the computer to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return True  # Exit the loop

    # Play music command
    elif re.search(r"(play video song|play audio song)\s+(.*)", command):
        media_type = re.search(
            r"(play video song|play audio song)", command).group(1)
        song_name = re.search(
            r"(play video song|play audio song)\s+(.*)", command).group(2).strip()

        if "video song" in media_type:
            play_video_song(song_name)
        else:
            play_audio_song(song_name)
        return False
    
    elif "cpu usage" in command:
        speak(get_cpu_usage())
        return False
    elif "memory usage" in command:
        speak(get_memory_usage())
        return False
    elif "disc space" in command:
        speak(get_disk_space())
        return False
    
    
    # Inside the respond function
    


    # Exit Jarvis
    elif 'escape' in command or 'quit' in command:
        speak("Goodbye!")
        return True  # Indicate to exit the loop
    
    # Return None for unrecognized commands
    return None
import subprocess

# Function to run git commands
def run_git_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"Error running git command: {e.stderr.decode('utf-8')}"

# Function to add changes
def git_add():
    return run_git_command("git add .")

# Function to commit changes with a voice-provided message
def git_commit(commit_message):
    return run_git_command(f'git commit -m "{commit_message}"')

# Function to push to GitHub
def git_push():
    return run_git_command("git push origin main")  # or another branch


# Function to get the current time for a specific country
def get_current_time(country):
    timezone_mapping = {
        'INDIA': 'Asia/Kolkata',
        'USA': 'America/New_York',  # Eastern Time Zone
        'UK': 'Europe/London',
        'CANADA': 'America/Toronto'  # Eastern Time Zone
    }

    tz = pytz.timezone(timezone_mapping[country])
    current_time = datetime.now(tz).strftime("%H:%M %p")  # Format time

    return current_time



def get_user_input(prompt):
    """Helper function to get user input with retry and close option."""
    while True:
        speak(prompt)
        user_input = listen()
        if user_input:
            if user_input.lower() == "close":
                speak("Operation has been canceled.")
                return None
            return user_input
        else:
            speak("I didn't catch that. Please repeat.")





# Function to open a website
def open_website(website_name):
    webbrowser.open(f"http://{website_name}")  # Open the website

# Function to write text in Notepad
def write_in_notepad(text):
    pyautogui.sleep(1)  # Adjust sleep time if necessary
    pyautogui.typewrite(text)  # Type the text into Notepad

# Function to close applications
def close_application(app_name):
    try:
        running_processes = {p.info['name'].lower(): p.info['pid']
                            for p in psutil.process_iter(['name', 'pid'])}
        matched_processes = [
            proc for proc in running_processes if app_name.lower() in proc]

        if matched_processes:
            for process in matched_processes:
                pid = running_processes[process]
                os.system(f"taskkill /f /pid {pid}")
                speak(f"{process.split('.')[0].capitalize()} has been closed.")
        else:
            speak(f"Sorry, no running application matches '{app_name}'.")
    except Exception as e:
        speak(
            f"Sorry, I encountered an error while closing {app_name}: {str(e)}")

# Function to create a folder on the desktop
def create_folder(folder_name):
    desktop_path = os.path.join(os.path.expanduser(
        "~"), "Desktop")  # Get the desktop path
    # Create the folder path
    folder_path = os.path.join(desktop_path, folder_name)

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # Create the folder
            speak(f"Folder '{folder_name}' has been created on your desktop.")
        else:
            speak(f"Folder '{folder_name}' already exists on your desktop.")
    except Exception as e:
        speak(
            f"Sorry, I encountered an error while creating the folder: {str(e)}")
        
# Function to delete a folder from the desktop
def delete_folder(folder_name):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, folder_name)

    try:
        if os.path.exists(folder_path):
            # Use shutil.rmtree to delete the folder and its contents
            shutil.rmtree(folder_path)
            speak(
                f"Folder '{folder_name}' and its contents have been deleted from your desktop.")
        else:
            speak(f"Folder '{folder_name}' does not exist on your desktop.")
    except Exception as e:
        speak(
            f"Sorry, I encountered an error while deleting the folder: {str(e)}")

# Function to play video songs
# Function to play video songs
def play_video_song(song_name):
    search_url = f"https://www.youtube.com/results?search_query={'+'.join(song_name.split())}"
    speak(f"Searching for the video song '{song_name}' on YouTube.")
    webbrowser.open(search_url)  # Open the search results in a web browser

# Function to play audio songs
def play_audio_song(song_name):
    # Assuming you're using Spotify or another service; adjust the URL as needed
    search_url = f"https://open.spotify.com/search/{'+'.join(song_name.split())}"
    speak(f"Searching for the audio song '{song_name}' on Spotify.")
    webbrowser.open(search_url)  # Open the search results in a web browser

# Function to get the current CPU usage and stat
def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)

    if cpu_usage < 50:
        state = "good"
    elif 50 <= cpu_usage <= 80:
        state = "average"
    else:
        state = "poor"

    return f"Current CPU usage is {cpu_usage}%. The CPU is in a {state} state."

# Function to get the current memory usage and state
def get_memory_usage():
    memory = psutil.virtual_memory()
    memory_usage = memory.percent

    if memory_usage < 50:
        state = "good"
    elif 50 <= memory_usage <= 80:
        state = "average"
    else:
        state = "poor"

    return f"Current memory usage is {memory_usage}%. The memory is in a {state} state."

# Function to get the available disk space
def get_disk_space():
    disk = psutil.disk_usage('/')
    total_space = disk.total // (2**30)  # Convert to GB
    used_space = disk.used // (2**30)    # Convert to GB
    free_space = disk.free // (2**30)    # Convert to GB

    return f"Total disk space: {total_space}GB, Used: {used_space}GB, Free: {free_space}GB."
# Updated ask_gemini function with your API key
def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Using the "gemini-1.5-flash" model
        response = model.generate_content(prompt)
        return response.text if response and response.text else "I couldn't get a response."
    except Exception as e:
        return f"An error occurred with Gemini AI: {str(e)}"



if __name__ == "__main__":
    speak("Hello, I am Jarvis. How can I assist you today?")

    while True:
        # Listen for commands
        command = listen()

        # Check if the command includes a stop keyword to exit
        if command:
            exit_program = respond(command)  # Check if the user wants to exit

            if exit_program:  # Exit if the user said goodbye or sleep
                break

            # Handle unrecognized commands here
            if exit_program is None:  # Only respond if not exiting
                speak("I'm not sure how to help with that.")



