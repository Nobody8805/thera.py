import json
from datetime import datetime

LOG_FILE="habits.json"

def add_habit():
    #the current date
    today=datetime.now().strftime("%d-%m-%Y")
    
    #load existing data of the date if there or start new (try-except block)
    try:
        with open(LOG_FILE, "r") as file:
            data=json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data={}

    #checking if 'today' exists in the data
    if today not in data:
        data[today]={"non-negotiables":{}, "normal":{}}

    #asking user for the type of habit
    habit_type_key=input("Is this a 'nn' [non-negotiables] or 'n' [normal] habit?").strip().lower()
    if habit_type_key == 'n':
        habit_type='normal'
    elif habit_type_key == 'nn':
        habit_type = 'non-negotiables'
    else:
        print("Invalid input.")
        return
    
    #ask habit name
    habit_name=input("Whats the habit name?").strip().lower()

    #setting default as false
    data[today][habit_type][habit_name]=False

    #saving data to json file
    with open(LOG_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Habit '{habit_name}' added under '{habit_type}' for '{today}'!")

def mark_habit_done():
    today=datetime.now().strftime("%d-%m-%Y")

    try:
        with open(LOG_FILE, "r") as file:
            data=json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        print("No database exists yet, try adding habits.")
        return
    
    if today not in data:
        print("No habits for today found. Try adding habits for today. ")
        return
    
    while True:
        habit_type_key=input("What type of habit? 'nn' [non-negotiables] or 'n' [normal] habit?").strip().lower()
        if habit_type_key == 'n':
            habit_type='normal'
            break
        elif habit_type_key == 'nn':
            habit_type = 'non-negotiables'
            break
        else:
            print("Invalid input.")
            return
        
    selected_type=data[today][habit_type]

    print("\nToday's Habits:")
    for e, (key, value) in enumerate(selected_type.items(), 1): #note this in journal
        print(f"{e}. {key} ➤ {'✅' if value else '❌'}")
    
    updated_value=input("Which habit is completed?>> ").strip().lower()

    if updated_value in selected_type:
        selected_type[updated_value] = True 
        with open(LOG_FILE, "w") as file:
            json.dump(data, file, indent=4)

        print("The data has been updated:-")
        for e, (key, value) in enumerate(selected_type.items(), 1): 
            print(f"{e}. {key} ➤ {'✅' if value else '❌'}")
    else:
        print("Habit does not exist.")

def view_habit():
    today=datetime.now().strftime("%d-%m-%Y")
    try:
        with open(LOG_FILE, "r") as file:
            data=json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        print("No database exists yet.")
        return
    
    if today not in data:
        print("No habbits found for today. Try logging in few habits.")
        return
    
    print(f"\n Habits for {today}:\n")

    for habit_type in [("non-negotiables"), ("normal")]:
        print(f"{habit_type.replace('-', ' ').title()}:")
        for e, (habit, done) in enumerate(data[today][habit_type].items(), 1):
            status = "✅" if done else "❌"
            print(f"{e}. {habit} ➤ {status}")
        print()

def delete_habit():
    today=datetime.now().strftime("%d-%m-%Y")

    with open(LOG_FILE, "r") as file:
        data=json.load(file)
    del_habit=input("Which habbit would you like to delete? ").strip().lower()
    
    for habit_type in [("non-negotiables"), ("normal")]:
        for key in data[today][habit_type]:
            if key == del_habit:
                del data[today][habit_type][del_habit]
                break

    with open(LOG_FILE, "w") as file:
        json.dump(data, file, indent=4)
            
    print("The updated habit list:- ")
    for habit_type in [("non-negotiables"), ("normal")]:
        print(f"{habit_type.replace('-', ' ').title()}:")
        for e, (habit, done) in enumerate(data[today][habit_type].items(), 1):
            status = "✅" if done else "❌"
            print(f"{e}. {habit} ➤ {status}")
        print()
    
