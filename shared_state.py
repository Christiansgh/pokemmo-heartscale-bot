import threading

state = {
    "current_task": "idle",
    "next_task": "none",
    "await": True,
    "quit": False,
    "num_timeouts": 0
}

state_lock = threading.Lock()

def push_state(state):
    with state_lock:
        if state["next_task"] == "idle":
            state["current_task"] = f"{state}"
    
def pop_state():
    state["current_task"] = state["next_task"]
    state["next_task"] = "none"

    

