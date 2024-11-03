import os
import colorama
from colorama import Fore
import threading
import rl
import jamstage
import ego
import reload

colorama.init(autoreset=True)

listener_thread = None
stop_event = threading.Event()

def print_color():
    print(Fore.RED + 'N', end='')
    print(Fore.YELLOW + 'i', end='')
    print(Fore.GREEN + 'T', end='')
    print(Fore.CYAN + 'e', end='')
    print(Fore.BLUE + 'B', end='')
    print(Fore.MAGENTA + 'o', end='')
    print(Fore.RED + 'T', end='')
    print(Fore.CYAN + ' v1.0.2', end='')
    print('\n')

def stop_listener():
    global listener_thread, stop_event
    stop_event.set()  
    if listener_thread and listener_thread.is_alive():
        listener_thread.join()  
    stop_event.clear()  

def start_listener(target_function):
    global listener_thread, stop_event
    stop_listener()  
    listener_thread = threading.Thread(target=target_function, args=(stop_event,))
    listener_thread.start()

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_color()
        print("Pick your flavour:")
        print("1) RL 🚀")
        print("2) Fortmeme Jam Stage 🎶")
        print("3) Fortmeme Ego 🧱")
        print("4) Fortmeme Reload / Battle Royale 🔫")
        print("5) Exit")

        choice = input("\nEnter your number: ")

        if choice == '1':
            print("Press CTRL+ALT+Q to start or stop the macro.\nPress Enter to go back to main menu.")
            start_listener(rl.start_listener)
            input_key = input()
            if input_key == '':
                stop_listener()
                continue
        elif choice == '2':
            print("Press CTRL+ALT+Q to start or stop the macro.\nPress Enter to go back to main menu.")
            start_listener(jamstage.start_listener)
            input_key = input()
            if input_key == '':
                stop_listener()
                continue
        elif choice == '3':
            print("Press CTRL+ALT+Q to start or stop the macro.\nPress Enter to go back to main menu.")
            start_listener(ego.start_listener)
            input_key = input()
            if input_key == '':
                stop_listener()
                continue
        elif choice == '4':
            print("Press CTRL+ALT+Q to start or stop the macro.\nPress Enter to go back to main menu.")
            start_listener(reload.start_listener)
            input_key = input()
            if input_key == '':
                stop_listener()
                continue
        elif choice == '5':
            print("Goodbye!")
            stop_listener()
            break
        else:
            print("Invalid number.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()