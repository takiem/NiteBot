from pynput import keyboard
import threading
import time
import random
import vgamepad as vg

macro_running = False
listener = None

def start_listener(stop_event):
    global listener

    def on_activate():
        global macro_running
        if macro_running:
            print("Stopping macro...")
            macro_running = False
        else:
            print("Starting macro...")
            macro_running = True
            threading.Thread(target=run_macro, args=(stop_event,)).start()

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

    while not stop_event.is_set():
        time.sleep(0.1)

    if listener is not None:
        listener.stop()
        listener.join()


def joystick_move(gamepad):
    left_x = random.choice([-1.0, 0.0, 1.0])
    left_y = random.choice([-1.0, 0.0, 1.0])
    right_x = random.choice([-1.0, 0.0, 1.0])
    right_y = random.choice([-1.0, 0.0, 1.0])

    gamepad.left_joystick_float(x_value_float=left_x, y_value_float=left_y)
    gamepad.right_joystick_float(x_value_float=right_x, y_value_float=right_y)
    gamepad.update()

def pressing_a(gamepad):
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(random.uniform(0.1, 0.2))
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()

def run_macro(stop_event):
    gamepad = vg.VX360Gamepad()
    print("Macro started!")

    try:
        while macro_running and not stop_event.is_set():
            joystick_move(gamepad)
            pressing_a(gamepad)
            time.sleep(random.uniform(1, 5))
    except KeyboardInterrupt:
        pass
    finally:
        gamepad.reset()
        gamepad.update()
        print("Macro stopped!")

if __name__ == "__main__":
    print("Press CTRL+ALT+Q to start/stop the macro.")
    stop_event = threading.Event()
    start_listener(stop_event)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()
        if listener is not None:
            listener.stop()
