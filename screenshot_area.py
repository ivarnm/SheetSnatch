import os
from PIL import ImageGrab
from pynput import keyboard

# === CONFIGURATION ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(SCRIPT_DIR, "screenshots")
CAPTURE_BOX = (75, 200, 1300, 650)  # (left, top, right, bottom)
TRIGGER_HOTKEY = {keyboard.Key.ctrl, keyboard.KeyCode(char='k')}
# ======================

os.makedirs(SAVE_FOLDER, exist_ok=True)
current_keys = set()
def take_screenshot():
    # Determine next available filename
    existing = [
        int(f.split('.')[0]) for f in os.listdir(SAVE_FOLDER)
        if f.endswith('.png') and f.split('.')[0].isdigit()
    ]
    next_index = max(existing, default=0) + 1
    filename = os.path.join(SAVE_FOLDER, f"{next_index}.png")
    
    # Take screenshot of region
    image = ImageGrab.grab(bbox=CAPTURE_BOX)
    image.save(filename)
    print(f"Screenshot saved as {filename}")

def on_press(key):
    current_keys.add(key)
    if all(k in current_keys for k in TRIGGER_HOTKEY):
        take_screenshot()

def on_release(key):
    current_keys.discard(key)

print("Press Ctrl+K to capture the screenshot region.")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
