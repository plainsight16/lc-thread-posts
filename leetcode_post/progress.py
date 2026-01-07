import json
from pathlib import Path

PROGRESS_FILE = Path("progress.json")

def init_thread(thread_id:str):
    data = {"day": 0, "thread_id": thread_id}
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))

def load_progress():
    if not PROGRESS_FILE.exists():
        return {"day": 0, "thread_id": None}
    return json.loads(PROGRESS_FILE.read_text())



def save_progress(day, thread_id):
    PROGRESS_FILE.write_text(
        json.dumps({"day":day, "thread_id": thread_id})
    )