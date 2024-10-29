from pynput import keyboard
import threading
import time
import vgamepad as vg
import platform

macro_running = False
listener = None

is_windows = platform.system() == "Windows"
y_axis_value = 1.0 if is_windows else -1.0  

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

def holding_lstick(gamepad):

    gamepad.left_joystick_float(x_value_float=0.0, y_value_float=y_axis_value)
    gamepad.update()

def press_a(gamepad):

    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()
    time.sleep(0.1)  
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()

def run_macro():
    gamepad = vg.VX360Gamepad()
    print("Macro started!")

    try:

        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
        time.sleep(0.5)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        gamepad.update()
        time.sleep(0.5)

        while macro_running:
            holding_lstick(gamepad)         
            press_a(gamepad) 
            time.sleep(0.1)                      
    except KeyboardInterrupt:
        pass
    finally:
        gamepad.reset()
        gamepad.update()
        print("Macro stopped!")

if __name__ == "__main__":
    print("Press CTRL+ALT+Q to start/stop the reload macro.")
    start_listener()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        if listener is not None:
            listener.stop()