import pyautogui
import utils
import time
import shared_state as state

def send_move_one():
    if state.state["thief"] == 0:
        utils.print_red("ERROR: IN BATTLE TRYING TO SEND MOVE WITH 0 PP LEFT")
        run()
        return
    send_move(['space'])
    state.state['thief'] -= 1
    utils.print_command(f"Thiefs left: {state.state['thief']}")

def send_move_two():
    if state.state["payday"] == 0:
        utils.print_red("ERROR: IN BATTLE TRYING TO SEND MOVE WITH 0 PP LEFT")
        run()
        return
    send_move(['d', 'space'])
    state.state['payday'] -= 1
    utils.print_command(f"Paydays left: {state.state['payday']}")

def send_move_three():
    send_move(['s', 'space'])

def send_move_four():
    send_move(['s', 'd', 'space'])

#TODO:
def throw_pokeball():
    print("TODO:")

def send_move(moves):
    pyautogui.press('a')
    pyautogui.press('w')
    pyautogui.press('space')
    for entry in moves:
        utils.print_command(f"SENDING KEY: {entry}")
        pyautogui.press(entry)

def run():
    utils.print_command("RUNNING")
    pyautogui.press('shift')
    pyautogui.press('s')
    pyautogui.press('d')
    pyautogui.press('space')
    time.sleep(1)
    pyautogui.press('shift')

#TODO:
def swap_pokemon(path_to_swap):
    print("TODO:")
