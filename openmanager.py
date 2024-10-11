import subprocess
import os

def open_application(app_name):
    try:
        if 'notepad' in app_name:
            subprocess.Popen(['notepad.exe'])
        elif 'chrome' in app_name:
            subprocess.Popen(
                ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'])
        elif 'calculator' in app_name:
            subprocess.Popen(['calc.exe'])
        elif 'word' in app_name:
            subprocess.Popen(
                ['C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE'])
        elif 'settings' in app_name:  # New condition for opening Settings
            subprocess.Popen(['start', 'ms-settings:'], shell=True)
        elif 'crop' in app_name:  # Opening Snipping Tool for "open crop"
            subprocess.Popen(['snippingtool.exe'])
        elif 'files' in app_name:  # Opening File Explorer for "open files"
            subprocess.Popen(['explorer.exe'])
        elif 'c drive' in app_name:  # Open C Drive
            subprocess.Popen(['explorer.exe', 'C:\\'])
        elif 'd drive' in app_name:  # Open D Drive
            subprocess.Popen(['explorer.exe', 'D:\\'])
        elif 'e drive' in app_name:  # Open E Drive
            subprocess.Popen(['explorer.exe', 'E:\\'])
        elif 'f drive' in app_name:  # Open F Drive
            subprocess.Popen(['explorer.exe', 'F:\\'])
        elif 'g drive' in app_name:  # Open G Drive
            subprocess.Popen(['explorer.exe', 'G:\\'])
        elif 'ms store' in app_name:
            subprocess.Popen(['start', 'ms-windows-store:'], shell=True)
        elif 'edge' in app_name:
            subprocess.Popen(['C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'])
        elif 'outlook' in app_name:
            subprocess.Popen(['C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE'])
        elif 'ms teams' in app_name or 'teams' in app_name:
            subprocess.Popen(['C:\\Users\\YourUsername\\AppData\\Local\\Microsoft\\Teams\\Update.exe', '--processStart', 'Teams.exe'])  # Adjust the path as needed
        elif 'mail' in app_name:
            subprocess.Popen(['start', 'outlookmail:'], shell=True)  # Opens Windows Mail
        elif 'fire fox' in app_name:
            subprocess.Popen(['C:\\Program Files\\Mozilla Firefox\\firefox.exe'])
        elif 'brave' in app_name:
            subprocess.Popen(['C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'])
        elif 'task manager' in app_name:
            subprocess.Popen(['taskmgr'])
        else:
            speak("Sorry, I cannot open that application.")
    except FileNotFoundError:
        speak("The application was not found. Please check the installation.")
    except Exception as e:
        speak(f"Sorry, I encountered an error: {str(e)}")
