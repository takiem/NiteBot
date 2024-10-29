from pynput import keyboard
import threading
import time
import random
import vgamepad as vg

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

    time.sleep(1)

    while macro_running:

        gamepad.right_trigger_float(value_float=1.0)
        gamepad.update()

        start_time = time.time()

        while macro_running and time.time() - start_time < 10:  
            for _ in range(2):
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.update()
                time.sleep(0.1)
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.update()
                time.sleep(3)  

        if macro_running:  
            gamepad.left_joystick_float(
                x_value_float=random.uniform(-1.0, 1.0),
                y_value_float=random.uniform(-1.0, 1.0)
            )
            gamepad.right_joystick_float(
                x_value_float=random.uniform(-1.0, 1.0),
                y_value_float=random.uniform(-1.0, 1.0)
            )
            gamepad.update()

            time.sleep(3)

        gamepad.right_trigger_float(value_float=0.0)
        gamepad.update()

    gamepad.reset()
    gamepad.update()

    print("Macro stopped.")

if __name__ == "__main__":
    print("Press CTRL+ALT+Q to start/stop the macro.")
    start_listener()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        if listener is not None:
            listener.stop()
