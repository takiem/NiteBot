import os
import colorama
from colorama import Fore
import threading
import rl  
import jamstage  
import ego  
import reload

colorama.init(autoreset=True)

def print_color():
    print(Fore.RED + 'N', end='')
    print(Fore.YELLOW + 'i', end='')
    print(Fore.GREEN + 'T', end='')
    print(Fore.CYAN + 'e', end='')
    print(Fore.BLUE + 'B', end='')
    print(Fore.MAGENTA + 'o', end='')
    print(Fore.RED + 'T', end='')
    print(Fore.CYAN + ' v1.0.0', end='')
    print('\n')

def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_color()
        print("Pick your flavour:")
        print("1) RL 🚀")
        print("2) Fortmeme Jam Stage 🎶")
        print("3) Fortmeme Ego 🧱")
        print("4) Fortmeme Reload 🔁")
        print("5) Exit")

        choice = input("\nEnter your number: ")

        if choice == '1':
            print("Press CTRL+ALT+Q to start or stop the macro.\nPress Enter to go back to main menu.")
            listener_thread = threading.Thread(target=rl.start_listener)
            listener_thread.start()
            input_key = input()
            if input_key == '':
                rl.macro_running = False  
                continue
        elif choice == '2':
            print("Press CTRL+ALT+Q to start or stop the macro.\nPress Enter to go back to main menu.")
            listener_thread = threading.Thread(target=jamstage.start_listener)
            listener_thread.start()
            input_key = input()
            if input_key == '':
                jamstage.macro_running = False  
                continue
        elif choice == '3':
            print("Press CTRL+ALT+Q to start or stop the macro.\nPress Enter to go back to main menu.")
            listener_thread = threading.Thread(target=ego.start_listener)
            listener_thread.start()
            input_key = input()
            if input_key == '':
                ego.macro_running = False  
                continue
        elif choice == '4':
            print("Press CTRL+ALT+Q to start or stop the macro.\nPress Enter to go back to main menu.")
            listener_thread = threading.Thread(target=reload.start_listener)
            listener_thread.start()
            input_key = input()
            if input_key == '':
                reload.macro_running = False  
                continue
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid number.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
