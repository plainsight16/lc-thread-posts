import json
def load_progress():
    """Load the current day number and thread ID from progress.json"""
    try:
        with open("progress.json", "r") as f:
            data = json.load(f)
            print(f"Current progress: Day {data['day']}")
            return data
    except FileNotFoundError:
        print("No previous progress found. Starting fresh!")
        return {"day": 0, "thread_id": None}


def save_progress(day, thread_id):
    """Save the current day number and thread ID to progress.json"""
    with open("progress.json", "w") as f:
        json.dump({"day": day, "thread_id": thread_id}, f, indent=2)
    print(f"Progress saved: Day {day}")