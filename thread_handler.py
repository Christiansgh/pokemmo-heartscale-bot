import keyboard
import threading
import shared_state as state
import controllers.main_controller as main


def init_threads():
    # init_screen_reader_service(1)
    print("TODO: Start threads.")
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
            print("RESET detected")
            # kill all threads besides main and keybind listener.
            # reset the threads.
            # send heal command.
        if keyboard.is_pressed("F12"):
            print("F12 detected")
            state.state["current_task"] = "waiting..." 
            main.handle_heal() 

def init_screen_reader_service(num_threads):
    # for i in range(num_threads):
    #     t = #threading.Thread(target=screen_reader_service, args=(i,))
    #     t.start()
    print("screen_reader_service started")
