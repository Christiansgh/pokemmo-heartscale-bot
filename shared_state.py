import threading

state = {
    "current_task": "idle",
    "next_task": "none",
    "await": False, # For main thread
    "quit": False,
    "max_timeouts": 0,
    "max_errors": 5,
    "errors": 0,
    "payday": 32,
    "thief": 40,
    "target": "none",
    "opponent": "none",
    "found": False,
    "loc": (0, 0),
    "width": 0,
    "height": 0,
    "certainty": 0,
    "result": 0,
}

lock = threading.Lock()

events = {
    "activate": threading.Event(), # for helper threads
    "continue": threading.Event(), # for main thread
}

def push_state(state):
    with lock:
        if state["next_task"] == "idle":
            state["current_task"] = f"{state}"
    
def pop_state():
    with lock:
        state["current_task"] = state["next_task"]
        state["next_task"] = "none"

    

