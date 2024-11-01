
RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
BLACK = '\033[30m'

def print_delimiter():
    print(f"{WHITE}================================================================={RESET}")

def print_info(message):
    print(f"{BLUE}INFO: {RESET}{message}")

def print_command(message):
    print(f"{MAGENTA}COMMAND: {RESET}{message}")

def print_red(message):
    print(f"{RED}{message}{RESET}")

def print_green(message):
    print(f"{GREEN}{message}{RESET}")

def print_yellow(message):
    print(f"{YELLOW}{message}{RESET}")

#TODO:
def print_keybinds():
    print("TODO")
