import keyboard
import threading
import shared_state as state
import controllers.main_controller as main
import controllers.screenreader_controller as screenreader
import utils
import time


def init_threads():
    utils.print_info("Starting screenreader.")
    init_screen_reader_service(1)
    utils.print_info("Starting keybinds listener.")
    t = threading.Thread(target=init_keybinds_listener)
    t.start()

def init_keybinds_listener():
    utils.print_info("Kebinds listener started")
    while not state.state["quit"]:
        if keyboard.is_pressed('alt+q'):
            print("Keybinds listener stopped.")
            # TODO: EXIT GRACEFULLY. LOG DATA AND SHIT BEFORE QUITTING.
            state.state["quit"] = True
        if keyboard.is_pressed('alt+r'):
            state.events["heal_ready"].set()
            # kill all threads besides main and keybind listener
            # reset the threads.
            # send heal command.
        if keyboard.is_pressed("F12"):
            print("F12 detected")
            #main.activate_helpers("screenshots/dead.png", 0.8)
            #state.events["continue"].clear()
            #state.events["continue"].wait()
            state.state["payday"] = 0
            time.sleep(1)

def init_screen_reader_service(num_threads):
    for _ in range(num_threads):
        t = threading.Thread(target=screenreader.handle_activation)
        t.start()
