import pyautogui

def send_move_one():
    send_move(['space', 'space'])

def send_move_two():
    send_move(['d', 'space', 'space'])

def send_move_three():
    send_move(['s', 'space', 'space'])

def send_move_four():
    send_move(['s', 'd', 'space', 'space'])

#TODO:
def throw_pokeball():
    print("TODO:")

def send_move(moves):
    pyautogui.press('a')
    pyautogui.press('w')
    for entry in moves:
        print(f"SENDING KEY: {entry}")
        pyautogui.press(entry)

#TODO:
def swap_pokemon(path_to_swap):
    print("TODO:")
