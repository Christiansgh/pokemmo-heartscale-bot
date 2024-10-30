import threading

state = {
    "current_task": "idle",
    "next_task": "not_none",#"none",
    "await": True, # For main thread
    "quit": False,
    "num_timeouts": 0,
    "payday": 32,
    "thief": 40,
    "target": "none",
    "found": False,
    "certainty": 0,
}

lock = threading.Lock()

events = {
    "heal_ready": threading.Event(),
    "activate": threading.Event(), # for helper threads
}

def push_state(state):
    with lock:
        if state["next_task"] == "idle":
            state["current_task"] = f"{state}"
    
def pop_state():
    with lock:
        state["current_task"] = state["next_task"]
        state["next_task"] = "none"

    

