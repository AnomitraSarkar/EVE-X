from pynput import keyboard
from pynput.mouse import Controller as MouseController
import time

mouse = MouseController()
MOVE_DISTANCE = 20  # pixels per keypress

def on_press(key):
    try:
        if key.char.lower() == 'w':
            mouse.move(0, -MOVE_DISTANCE)  # up
        elif key.char.lower() == 's':
            mouse.move(0, MOVE_DISTANCE)   # down
        elif key.char.lower() == 'a':
            mouse.move(-MOVE_DISTANCE, 0)  # left
        elif key.char.lower() == 'd':
            mouse.move(MOVE_DISTANCE, 0)   # right
        elif key.char.lower() == 'q':
            print("Exiting...")
            return False  # stops the listener
    except AttributeError:
        pass  # for special keys like Shift, etc.

print("Use W/A/S/D to move the mouse. Press Q to quit.")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()