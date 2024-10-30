import keyboard
import threading
import time

from movement_controller import *
from battle_controller import *
from utils import *

keep_running = True
lock = threading.Lock()


def listen_for_exit():
    global keep_running

    while keep_running:
        if keyboard.is_pressed('alt+q'):
            print_info("Detected break request...")
            keep_running = False


def start_screenshot_service(interval):
    global keep_running

    while keep_running:
        with lock:
            screenshot_game()
        time.sleep(interval)


def wait_move_ready():
    waiting = True
    print("Waiting for move to be ready...")
    while waiting:
        found, _, _, _, _ = find_candidate(0.60, "move_ready.png")
        if found:
            waiting = False
            print("Move is ready.")
        else:
            time.sleep(0.3)


def wait_fish_ready():
    waiting = True
    print("Waiting for fish to be ready...")
    while waiting:
        found, _, _, _, _ = find_candidate(0.60, "textbubble.png")
        if found:
            waiting = False
            print("Fish is ready.")
        else:
            time.sleep(0.3)


def wait_for_heal():
    waiting = True
    print("Waiting for heal completion...")
    while waiting:
        found, _, _, _, _ = find_candidate(0.60, "heal.png")
        if found:
            waiting = False
            print("Healing completed.")
        else:
            time.sleep(0.3)
    press_key('space')


def listen_for_manual_command():
    global keep_running
    global pay_day
    global thief

    while keep_running:
        if keyboard.is_pressed('F12'):
            print_command("Manual mode activated...")
            pay_day = 32
            thief = 40

            reset()
            while keep_running:
                if pay_day == 0 or thief == 0:
                    reset()
                    pay_day = 32
                    thief = 40
                with lock:
                    best_candidate, best_result = find_best_candidate("events")

                print_info("Analyzing screen...")
                if best_candidate == "remoraid" and best_result >= 0.6:
                    print_info("Found 'Remoraid'")
                    wait_move_ready()
                    send_battle_command(['d', 'space'])
                    pay_day -= 1
                    time.sleep(7)
                    remove_held_item("held_item.png")
                elif best_candidate == "luvdisc" and best_result >= 0.6:
                    print_info("Found 'Luvdisc'")
                    wait_move_ready()
                    send_battle_command(['space', 'space'])
                    thief -= 1
                    time.sleep(7)
                    remove_held_item("held_item.png")
                elif best_candidate == "shellder" and best_result >= 0.6:
                    print_info("Found 'Shellder'")
                    wait_move_ready()
                    send_battle_command(['d', 'space'])
                    pay_day -= 1
                    time.sleep(9)
                    remove_held_item("held_item.png")
                else:
                    press_key('f')
                    wait_fish_ready()
                    press_key('space')
                    time.sleep(4)


def find_best_candidate(candidates_folder_path):
    best_result = 0
    best_candidate = "none"
    max_retries = 3
    retry_count = 0
    game_screenshot = None

    while retry_count < max_retries:
        with lock:
            game_screenshot = cv2.imread("screenshot.png", cv2.IMREAD_GRAYSCALE)

        if game_screenshot is not None:
            break
        else:
            print("Failed to load screenshot.png. Retrying...")
            screenshot_game()
            retry_count += 1

    if game_screenshot is None:
        print("Error: Unable to load screenshot after retries.")
        return best_candidate, best_result

    for entry in os.listdir(candidates_folder_path):
        entry_name = os.path.join(candidates_folder_path, entry)
        img = cv2.imread(entry_name, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Error loading {entry_name}. Skipping.")
            continue

        result = cv2.matchTemplate(game_screenshot, img, cv2.TM_CCOEFF_NORMED)
        _, entry_result, _, _ = cv2.minMaxLoc(result)

        if entry_result > best_result:
            best_result = entry_result
            best_candidate = os.path.splitext(entry)[0]

    print_yellow(f"Best candidate {best_candidate}.png, value {best_result:.2f}")
    return best_candidate, best_result


def find_candidate(certainty, candidate_path):
    max_retries = 3
    retry_count = 0
    game_screenshot = None

    while retry_count < max_retries:
        with lock:
            game_screenshot = cv2.imread("screenshot.png", cv2.IMREAD_GRAYSCALE)

        if game_screenshot is not None:
            break
        else:
            print("Failed to load screenshot.png. Retrying...")
            screenshot_game()
            retry_count += 1

    if game_screenshot is None:
        print("Error: Unable to load screenshot after retries.")
        return False, None, None, None, 0

    candidate = cv2.imread(candidate_path, cv2.IMREAD_GRAYSCALE)
    if candidate is None:
        print(f"Error loading {candidate_path}.")
        return False, None, None, None, 0

    result = cv2.matchTemplate(game_screenshot, candidate, cv2.TM_CCOEFF_NORMED)
    _, max_result, _, max_loc = cv2.minMaxLoc(result)

    if max_result >= certainty:
        return True, max_loc, candidate.shape[1], candidate.shape[0], max_result
    return False, None, None, None, max_result


def reset():
    press_key('b')
    time.sleep(4)

    print_command("Healing")
    press_key('space')
    wait_for_heal()

    print_command("Leaving Pokecenter")
    press_keys_for(['shift', 's'], 5)
    print_command("Moving to fishing spot")
    press_keys_for(['a'], 2)
    press_keys_for(['s'], 3)


def remove_held_item(path):
    with lock:
        found, loc, width, height, _ = find_candidate(0.5, path)

    if not found or loc is None:
        return

    pyautogui.keyDown('ctrl')
    random_x = random.randint(int(loc[0] + width - 40), int(loc[0] + width - 10))
    random_y = random.randint(int(loc[1] + height - 40), int(loc[1] + height - 10))

    pyautogui.click(random_x, random_y)
    pyautogui.keyUp('ctrl')
    move_x = random_x + 457
    move_y = random_y + 91
    pyautogui.click(move_x, move_y)


def init_threads():
    threading.Thread(target=listen_for_exit).start()
    threading.Thread(target=listen_for_manual_command).start()
    threading.Thread(target=start_screenshot_service, args=[1]).start()
