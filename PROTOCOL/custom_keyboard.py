from pynput import keyboard
import pyautogui
import threading

# Track the current mode
current_mode = "NORMAL"
input_buffer = ""
max_buffer_length = 20  # Avoid growing too large

# Available modes mapped to trigraph codes
modes = {
    'WQ': 'WRITE',
    'PC': 'PROTOCOL',
    'EX': 'EXPLORE',
    'MV': 'MOUSE',
    'SZ': 'SPEECH',
    'VK': 'VIM',
}

def handle_mode_switch(code):
    global current_mode
    if code in modes:
        current_mode = modes[code]
        print(f"Switched to mode: {current_mode}")
        # Call placeholder for mode-specific action
        mode_action(current_mode)

def mode_action(mode):
    if mode == 'WRITE':
        print("📝 Write mode active")
    elif mode == 'PROTOCOL':
        print("📡 Protocol mode active")
    elif mode == 'EXPLORE':
        print("📁 Explore mode active")
    elif mode == 'MOUSE':
        pyautogui.moveTo(100, 100)  # Example
        print("🖱️ Mouse moved to (100, 100)")
    elif mode == 'SPEECH':
        print("🎙️ Speech mode active")
    elif mode == 'VIM':
        print("⌨️ Vim mode active")
    # Add more mode logic here

def on_press(key):
    global input_buffer, current_mode
    try:
        print(key,end="")
        char = key.char
    except AttributeError:
        return  # Ignore special keys

    input_buffer += char
    input_buffer = input_buffer[-max_buffer_length:]  # Trim buffer
    

    # Check for pattern ::XX:: (e.g. ::VK::)
    if "::" in input_buffer:
        parts = input_buffer.split("::")
        if len(parts) >= 3:
            code_candidate = parts[-2].upper()
            handle_mode_switch(code_candidate)
            input_buffer = ""  # Reset after successful match

def start_listener():
    print("Starting key listener. Type ::XX:: to switch modes (e.g. ::VK:: for Vim mode)")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()
