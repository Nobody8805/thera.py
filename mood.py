import json
from datetime import datetime
from time import sleep



LOG_FILE="mood_log.json"

def show_last_mood(n=3):
    try: 
        with open(LOG_FILE, "r") as log:
           data=json.load(log)
           print("\nLast", n, "logged moods: ")
           for entry in data["logs"][-n:]:
                print(f"   {entry['time']} — {entry['mood']}")
    except FileNotFoundError:
        print("\nNo mood history found yet.")
    except json.JSONDecodeError:
        print("\nMood log is corrupted or empty.")

def get_mood():
    return input("How are you currently feeling? >>").lower()

def log_mood_json(mood):
    print("So you said you are currently feeling", mood, ". Hmmm. Ill be logging it in.")
    sleep(2)
    current_time = datetime.now().strftime("%d-%m-%Y %H:%M")
    entry = {"time": current_time, "mood": mood}

    # Try to load existing data
    try:
        with open(LOG_FILE, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):  
        data = {"logs": []}

    # Add new entry
    data["logs"].append(entry)

    # Write updated data back
    with open(LOG_FILE, 'w') as file:
        json.dump(data, file, indent=4)


def respond_to_mood(mood):
    responses = {
        'happy': "Ayyy, thats great! But remember, emotions are a roller coaster. Dont get too attached.",
        'sad': "I get it. But dont worry, emotions pass. Just ride the wave and stay kind to yourself.",
        'angry': "Okay. Breathe. Youre not your anger. Find the bug in the system, not in yourself."
    }
    print(responses.get(mood, "Hmm... Ill add that to the list next time."))

def run_logger():
    while True:
        show_last_mood()
        mood=get_mood()
        log_mood_json(mood)
        respond_to_mood(mood)

        again=input("\nLog another mood? (y/n) >>").lower()
        if again != 'y':
            print("Cya later! ")
            break
