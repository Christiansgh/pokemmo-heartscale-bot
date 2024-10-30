import utils
import time
import shared_state as state
import controllers.movement_controller as movement


def start_main_loop():
    utils.print_info("Main loop initiated.")
    while not state.state["quit"]:
        handle_current_task()
        handle_next_task()

def activate_helpers(target, certainty):
    state.state["target"] = target
    state.state["certainty"] = certainty
    utils.print_info("Activating helpers...")
    state.events["activate"].set()

def handle_current_task():
    if state.state["payday"] == 0 or state.state["thief"] == 0:
        handle_heal()
        handle_walk_back()

    # if state.state["current_task"] == "fishing":
    #     print("TODO: handle_current_task(battling)")
    #
    # elif state.state["current_task"] == "battling":
    #     print("TODO: handle_current_task(battling)")

def handle_next_task():
    if state.state["next_task"] == "none":
        print("TODO: handle_next_task()")
        #state.state["current_task"] = "idle"
    else:
        state.state["current_task"] = state.state["next_task"]

def handle_heal():
    movement.teleport()
    time.sleep(3)
    activate_helpers("screenshots/heal_ready.png", 0.8)
    state.state["await"] = True
    while state.state["await"]:
        movement.press_and_hold('space', 0.2)
        utils.print_red("Waiting for heal ready...")
        time.sleep(0.3)

    utils.print_command("Healing")
    movement.press_and_hold('space', 2)
    movement.run_for(2.5, 's')

def handle_walk_back():
    movement.run_for(2, 'a')
    movement.run_for(2, 's')
    state.state["payday"] = 32

#TODO:
def handle_battle():
    print("TODO: main_controller.handle_battle()")

#TODO:
def handle_fish():
    print("TODO: main_controller.handle_fish()")

#TODO:
def handle_stuck():
    print("TODO: main_controller.handle_stuck()")

#TODO:
def handle_too_many_timeouts():
    print("TODO: main_controller.handle_too_many_timeouts()")

