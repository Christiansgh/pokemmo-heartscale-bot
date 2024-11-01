import time
import pyautogui

from utils import *

# Does everything overworld related.
keybinds = {
    "teleport": 'b',
    "interact": 'space',
    "fish": 'f',
    "run": 'shift'
}

directions = {
    "s": 'down',
    "w": 'up',
    "a": 'left',
    "d": 'right'
}

def teleport():
    face('w')
    print_command("Teleport")
    face('w')
    pyautogui.press(keybinds['teleport'])

def fish():
    face('s')
    print_command("Fish")
    pyautogui.press(keybinds['fish'])

def interact():
    print_command("Interact")
    pyautogui.press(keybinds['interact'])

def press_and_hold(key, interval):
    pyautogui.keyDown(key)
    time.sleep(interval)
    pyautogui.keyUp(key)

def face(direction):
    print_command(f'Face {directions[direction]}')
    pyautogui.press(direction)

def run_for(interval, direction):
    print_command(f"Start running {directions[direction]}")
    pyautogui.keyDown(keybinds['run'])
    pyautogui.keyDown(direction)
    time.sleep(interval)
    pyautogui.keyUp(direction)
    pyautogui.keyUp(keybinds['run'])
    print_command(f"Stop running {directions[direction]}")

# TODO:
def hard_reset():
    print("TODO:")
    
# TODO:
def open_held_item_menu():
    print("TODO:")
