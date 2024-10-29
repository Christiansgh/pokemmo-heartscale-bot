import utils
import time
import shared_state as state
import controllers.movement_controller as movement


def start_main_loop():
    utils.print_info("Main loop initiated.")
    while not state.state["quit"]:
        handle_current_task()
        handle_next_task()

def await_event(event):
    if event == "fish_caught":
        # Wait for text bubble.
        print("TODO:")
    if event == "heal_ready":
        # Wait till outside pokemon center.
        print("TODO:")
        print("Making threads look for heal popup.")
    if event == "done_walking":
        # Wait till at fishing spot.
        print("TODO:")

    # awaits untill the next state is ready.
    # Fishing, healing, move etc.

def handle_current_task():
    if state.state["current_task"] == "idle":
        utils.print_info("Current task: Idle...")
        return
    if state.state["payday"] == 0 or state.state["thief"] == 0:
        handle_heal()
        handle_walk_back()
        await_event("done_walking")

    if state.state["current_task"] == "fishing":
        await_event("fish_caught")

    elif state.state["current_task"] == "battling":
        print("TODO:")   

def handle_next_task():
    if state.state["next_task"] == "none":
        print("TODO:")
        #state.state["current_task"] = "idle"
    else:
        state.state["current_task"] = state.state["next_task"]

def handle_heal():
    utils.print_command("Teleporting")
    movement.teleport()
    time.sleep(3)
# loop back if assertion fails
    movement.press_and_hold('space', 0.2)
    await_event("heal_ready")
# assert has heal ready. // Find candidate
    utils.print_command("Healing")
    movement.press_and_hold('space', 4)
    movement.run_for(2, 's')

#TODO:
def handle_battle():
    print("TODO:")

#TODO:
def handle_fish():
    print("TODO:")

#TODO:
def handle_walk_back():
    print("TODO:")

#TODO:
def handle_stuck():
    print("TODO:")

#TODO:
def handle_too_many_timeouts():
    print("TODO:")

