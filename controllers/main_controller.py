import utils
import time
import random
import pyautogui
import cv2
import shared_state as state
import controllers.movement_controller as movement
import controllers.battle_controller as battle


def start_main_loop():
    utils.print_info("Main loop initiated.")
    while not state.state["quit"]:
        handle_current_task()
        handle_next_task()

def activate_helpers(target, certainty, max_timeouts = 0):
    state.state["max_timeouts"] = max_timeouts
    state.state["target"] = target
    state.state["certainty"] = certainty
    state.events["activate"].set()

def handle_current_task():
    if state.state["current_task"] is not "idle":
        utils.print_delimiter()
        utils.print_green(f"Current task: {state.state['current_task']}")

    if state.state["payday"] == 0 or state.state["thief"] == 0:
        time.sleep(1)
        battle.run()
        time.sleep(1)
        handle_heal()

    current_task = state.state["current_task"]
    if current_task == "idle":
        return

    if current_task == "fish":
        handle_fish()
    
    if current_task == "battle":
        handle_battle()

    if current_task == "walk_back":
        handle_walk_back()

def handle_next_task():
    if state.state["next_task"] == "none":
        pass
        #state.state["current_task"] = "idle"
    else:
        state.state["current_task"] = state.state["next_task"]

def handle_heal():
    state.state["next_task"] = "walk_back"
    movement.teleport()
    time.sleep(3.7)
    movement.press_and_hold('space', 0.3)
    activate_helpers("screenshots/heal_ready.png", 0.8, 6)
    utils.print_info("Waiting for heal ready...")
    state.events["continue"].clear()
    state.events["continue"].wait()

    utils.print_command("Healing")
    movement.press_and_hold('space', 4)
    movement.run_for(3, 's')
    state.state["payday"] = 32
    state.state["thief"] = 40
    state.state["current_task"] = "idle"
    time.sleep(1)

def handle_walk_back():
    state.state["next_task"] = "fish"
    movement.run_for(1.5, 'a')
    movement.run_for(2, 's')
    state.state["current_task"] = "idle"

def handle_fish():
    movement.fish()
    activate_helpers("screenshots/textbubble.png", 0.6, 15)
    state.events["continue"].clear()
    utils.print_info("Waiting for fish ready...")
    state.events["continue"].wait()

    movement.interact() # Reel in
    movement.fish()

    # Figure out if fishing or battling.
    fish_or_battle()

def fish_or_battle():
    activate_helpers("screenshots/textbubble.png", 0, 1)
    state.events["continue"].clear()
    state.events["continue"].wait()
    fish_result = state.state["result"]
    
    activate_helpers("screenshots/battle.png", 0, 1)
    state.events["continue"].clear()
    state.events["continue"].wait()
    battle_result = state.state["result"]

    state.state["current_task"] = "idle"
    if fish_result > battle_result and fish_result > 0.6:
        activate_helpers("screenshots/textbubble.png", 0.6, 15)
        state.state["next_task"] = "fish"
    elif battle_result > 0.6:
        state.state["next_task"] = "battle"
    else:
        state.state["next_task"] = "fish"

def handle_battle():
    find_opponent()
    if state.state["opponent"] == "remoraid":
        utils.print_info("Remoraid found!")
        activate_helpers("screenshots/move_ready.png", 0.5, 11)
        utils.print_info("Waiting for move ready...")
        state.events["continue"].clear()
        state.events["continue"].wait()
        battle.send_move_two()

    elif state.state["opponent"] == "shellder":
        utils.print_info("Shellder found!")
        activate_helpers("screenshots/move_ready.png", 0.5, 11)
        utils.print_info("Waiting for move ready...")
        state.events["continue"].clear()
        state.events["continue"].wait()
        battle.send_move_two()

    elif state.state["opponent"] == "luvdisc":
        utils.print_info("Luvdisc found!")
        activate_helpers("screenshots/move_ready.png", 0.5, 11)
        utils.print_info("Waiting for move ready...")
        state.events["continue"].clear()
        state.events["continue"].wait()
        battle.send_move_one()

    # Currently the move is sent, which can result in vitcory or another round.
    # Maybe we should add another param to "activate_helpers" that contains the maximum timeout.

    # TODO: IT IS POSSIBLE THAT CHANGING THE THEME FOR BETTER CONTRAST MIGHT BE A BETTER SOLUTION

    utils.print_info("Waiting for battle to finish...")
    activate_helpers("screenshots/dead.png", 0.97, 25)
    state.events["continue"].clear()
    state.events["continue"].wait()
    found = state.state["found"]

    if found:
        state.state["next_task"] = "fish"
        time.sleep(4.5)
        remove_held_item()
    else:
        state.state["next_task"] = "battle"

def find_opponent():
    activate_helpers("screenshots/enemies/remoraid.png", 0, 1)
    state.events["continue"].clear()
    state.events["continue"].wait()
    remoraid = state.state["result"]
    state.state["opponent"] = "remoraid"
    
    activate_helpers("screenshots/enemies/shellder.png", 0, 1)
    state.events["continue"].clear()
    state.events["continue"].wait()
    shellder = state.state["result"]
    if shellder > remoraid:
        state.state["opponent"] = "shellder"

    activate_helpers("screenshots/enemies/luvdisc.png", 0, 1)
    state.events["continue"].clear()
    state.events["continue"].wait()
    luvdisc = state.state["result"]
    if state.state["opponent"] == "shellder" and luvdisc > shellder:
        state.state["opponent"] = "luvdisc"
    elif luvdisc > remoraid:
        state.state["opponent"] = "luvdisc"

def remove_held_item():
    utils.print_command("Remove held item")
    activate_helpers("screenshots/held_item.png", 0.5, 1)
    state.events["continue"].clear()
    state.events["continue"].wait()

    found = state.state["found"]
    if found: 
        loc = state.state["loc"]
        width = state.state["width"]
        height = state.state["height"]
        pyautogui.keyDown('ctrl')
        random_x = random.randint(int(loc[0] + width - 40), int(loc[0] + width - 10)) + 1920 #TODO: Currently pyautogui assumes both screens as one big screen. This means to target #2, we need to add 1920 for the width.
        random_y = random.randint(int(loc[1] + height - 40), int(loc[1] + height - 10))      #TODO: We might be able to do a calculation on startup to store the screen width and set like a screentarget.

        pyautogui.click(random_x, random_y)
        pyautogui.keyUp('ctrl')
        move_x = random_x - 250
        move_y = random_y + 91
        pyautogui.click(move_x, move_y)
    else:
        print("NOT FOUND")
        activate_helpers("screenshots/meowth.png", 0, 1)
        state.events["continue"].clear()
        state.events["continue"].wait()
    #   locate meowth
        loc = state.state["loc"]
        width = state.state["width"]
        height = state.state["height"]

        random_x = random.randint(int(loc[0]), int(loc[0] + width)) + 1920 #TODO: SEE ABOVE TODO FOR SAME SCREEN PROBLEM.
        random_y = random.randint(int(loc[1]), int(loc[1] + height))
    #   right click. Should open window.
        pyautogui.rightClick(random_x, random_y)

    #   relocate held item square.
        activate_helpers("screenshots/held_item.png", 0.5, 1)
        state.events["continue"].clear()
        state.events["continue"].wait()
    #   Draw the square like before. have pyautogui do keyDown ctrl and click in the square randomly.
        loc = state.state["loc"]
        width = state.state["width"]
        height = state.state["height"]
# Screen dimensions for reference
        screen_width, screen_height = pyautogui.size()  # Total virtual screen dimensions

# Adjust x-coordinate by screen width to target second monitor
        offset_x = 1920 if screen_width > 1920 else 0  # Adjust this if your primary screen width varies
        random_x = random.randint(int(loc[0] + width - 40), int(loc[0] + width - 10)) + offset_x
        random_y = random.randint(int(loc[1] + height - 40), int(loc[1] + height - 10))

# Move the mouse to calculated position
        pyautogui.moveTo(random_x, random_y)

    #   Now we need to click outside the square. Prolly take the random X and minus it by Y.
        pyautogui.move(- 60, 0)

    #   With click and hold, and move to Y 0 and 10000 X.
        pyautogui.FAILSAFE = False
        pyautogui.dragTo(10000, 0, 0.2, button='left')
        remove_held_item() # Rerun to remove the item, now that the interface is opened correctly.

def locate_image():
    #img = cv2.imread("screenshots/69.png")
    #res = cv2.rectangle(img, (loc), (loc[0] + width, loc[1] + height), (0, 255, 0), 2)
    #cv2.imshow("Image", res)
    cv2.waitKey(0)

#TODO:
def handle_stuck():
    print("TODO: main_controller.handle_stuck()")
    # When timing out we should count the state up.
    # When X state is set. 
    # Somethings to consider.
    # - Might be in battle.
    #       do movement.run()
    # - Might be stuck outside - do handle_heal()
    # - Might be stuck inside the pokecenter.
    #       Do some wiggling to get outside, then heal.

#TODO:
def handle_too_many_timeouts():
    print("TODO: main_controller.handle_too_many_timeouts()")

