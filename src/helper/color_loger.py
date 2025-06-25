from colorama import Fore


def log_warning(message):
    print(f"{Fore.YELLOW} [WARNING] {Fore.RESET} {message}")

def log_error(message):
    print(f"{Fore.RED} [ERROR] {Fore.RESET} {message}")