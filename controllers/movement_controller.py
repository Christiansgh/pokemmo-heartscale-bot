import time
import pyautogui

from utils import *

# Does everything overworld related.
keybinds = {
    "teleport": 'b',
    "interact": 'space',
    "run": 'shift'
}

directions = {
    "s": 'down',
    "w": 'up',
    "a": 'left',
    "d": 'right'
}

# TODO:
def remove_held_item():
    print("TODO:")

def teleport():
    print_command("Teleport")
    pyautogui.press(keybinds['teleport'])

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
