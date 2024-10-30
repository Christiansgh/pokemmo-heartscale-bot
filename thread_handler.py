import keyboard
import threading
import shared_state as state
import controllers.main_controller as main
import controllers.screenreader_controller as screenreader
import utils


def init_threads():
    utils.print_info("Starting screenreader.")
    init_screen_reader_service(1)
    utils.print_info("Starting keybinds listener.")
    t = threading.Thread(target=init_keybinds_listener)
    t.start()

def init_keybinds_listener():
    print("keybinds_reader_service started")
    while not state.state["quit"]:
        if keyboard.is_pressed('alt+q'):
            print("Keybinds listener stopped.")
            # TODO: EXIT GRACEFULLY. LOG DATA AND SHIT BEFORE QUITTING.
            state.state["quit"] = True
        if keyboard.is_pressed('alt+r'):
            state.events["heal_ready"].set()
            # kill all threads besides main and keybind listener.
            # reset the threads.
            # send heal command.
        if keyboard.is_pressed("F12"):
            print("F12 detected")
            state.state["current_task"] = "waiting..." 
            main.handle_heal() 

def init_screen_reader_service(num_threads):
    for _ in range(num_threads):
        t = threading.Thread(target=screenreader.handle_activation)
        t.start()
    print("screen_reader_service started")
