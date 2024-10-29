import mss
import mss.tools
import cv2

from utils import *

def screenshot_game(thread_num, monitor_num = 2):
    with mss.mss() as sct:
        print_info("Screnshotting game...")
        img = sct.grab(sct.monitors[monitor_num])
        mss.tools.to_png(img.rgb, img.size, output=f"{thread_num}.png")

def find_candidate(certainty, candidate_path):
    max_retries = 3
    retry_count = 0
    game_screenshot = None

    while retry_count < max_retries:
        with lock:
            game_screenshot = cv2.imread("screenshot.png", cv2.IMREAD_GRAYSCALE)
        
        if game_screenshot is not None:
            break  # Exit loop if image loads successfully
        else:
            print("Error: Could not load screenshot.png. Retrying...")
            screenshot_game()
            retry_count += 1
    
    if game_screenshot is None:
        print("Error: Failed to load screenshot after retries.")
        return False, None, None, None, 0

    candidate = cv2.imread(candidate_path, cv2.IMREAD_GRAYSCALE)
    if candidate is None:
        print(f"Error: Could not load {candidate_path}.")
        return False, None, None, None, 0

    # Apply a binary threshold to highlight the white areas
    _, game_screenshot_thresh = cv2.threshold(game_screenshot, 240, 255, cv2.THRESH_BINARY)
    _, candidate_thresh = cv2.threshold(candidate, 240, 255, cv2.THRESH_BINARY)

    # Perform template matching on thresholded images
    result = cv2.matchTemplate(game_screenshot_thresh, candidate_thresh, cv2.TM_CCOEFF_NORMED)
    _, max_result, _, max_loc = cv2.minMaxLoc(result)

    # Check if the result is above the certainty threshold
    if max_result >= certainty:
        print_green(f"{candidate_path} found - result: {max_result:.2f} required: {certainty}")
        return True, max_loc, candidate.shape[1], candidate.shape[0], max_result

    print_red(f"{candidate_path} not found - result: {max_result:.2f} required: {certainty}")
    return False, None, None, None, max_result

#TODO:
def find_best_candidate(path_to_folder):
    print("TODO")

def notify_await_done(target, certainty):
    # Make each thread search for the target
    # find_candidate(certainty, target)
    print("TODO")

