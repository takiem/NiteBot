from pynput import keyboard
import threading
import time
import random
import vgamepad as vg
import platform

macro_running = False
listener = None

def start_listener():
    global listener

    def on_activate():
        global macro_running
        if macro_running:
            print("Stopping macro...")
            macro_running = False
        else:
            print("Starting macro...")
            macro_running = True
            threading.Thread(target=run_macro).start()

    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse('<ctrl>+<alt>+q'),
        on_activate
    )

    def for_canonical(f):
        return lambda k: f(listener.canonical(k))

    listener = keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)
    )
    listener.start()

def run_macro():
    gamepad = vg.VX360Gamepad()

    is_windows = platform.system() == "Windows"

    while macro_running:

        wait_time = random.uniform(30, 51)
        print(f"Waiting for {wait_time:.2f} seconds.")
        start_wait = time.time()
        while time.time() - start_wait < wait_time:
            if not macro_running:
                break
            time.sleep(0.1)

        if not macro_running:
            break

        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        gamepad.update()

        button_to_press = vg.XUSB_BUTTON.XUSB_GAMEPAD_Y if is_windows else vg.XUSB_BUTTON.XUSB_GAMEPAD_X
        y_presses = random.randint(2, 4)

        for i in range(y_presses):
            if not macro_running:
                break

            x = random.uniform(-1.0, 1.0)
            y = random.uniform(-1.0, 1.0)
            gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
            gamepad.update()

            gamepad.press_button(button=button_to_press)
            gamepad.update()
            time.sleep(random.uniform(0.1, 0.2))  
            gamepad.release_button(button=button_to_press)
            gamepad.update()
            time.sleep(random.uniform(0.5, 1.0))  

            x = random.uniform(-1.0, 1.0)
            y = random.uniform(-1.0, 1.0)
            gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
            gamepad.update()

        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
        gamepad.update()

    gamepad.reset()
    gamepad.update()

    print("Macro stopped!")

if __name__ == "__main__":
    print("Press CTRL+ALT+Q to start/stop the macro.")
    start_listener()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        if listener is not None:
            listener.stop()