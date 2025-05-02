import os
from PIL import Image

# === CONFIGURATION ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FOLDER = os.path.join(SCRIPT_DIR, "screenshots")
DESTINATION_FOLDER = os.path.join(SCRIPT_DIR, "processed_screenshots")

REPLACE_WITH_BLACK = [(40, 95, 211), (42, 101, 162), (44, 102, 187), (45, 43, 89)] # dark blue shades x3, dark purple bar       
REPLACE_WITH_WHITE = [(247, 244, 234), (205, 204, 238), (227, 222, 239)] # yellowish white, light purple bar shades x2    
REPLACE_WITH_GRAY  = [(108, 107, 146)] # gray purple bar

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (157, 154, 147)

FUZZY_THRESHOLD = 20  # max per-channel difference
# ======================

def is_similar(c1, c2, threshold=FUZZY_THRESHOLD):
    return all(abs(a - b) <= threshold for a, b in zip(c1, c2))

def replace_colors(image):
    img = image.convert("RGB")
    pixels = img.load()
    
    for y in range(img.height):
        for x in range(img.width):
            current = pixels[x, y]
            if any(is_similar(current, target) for target in REPLACE_WITH_BLACK):
                pixels[x, y] = BLACK
            elif any(is_similar(current, target) for target in REPLACE_WITH_WHITE):
                pixels[x, y] = WHITE
            elif any(is_similar(current, target) for target in REPLACE_WITH_GRAY):
                pixels[x, y] = GRAY

    img = img.convert("L") # Convert to grayscale    
    return img

def process_images():
    for filename in os.listdir(SOURCE_FOLDER):
        if filename.lower().endswith(".png"):
            path = os.path.join(SOURCE_FOLDER, filename)
            destinationPath = os.path.join(DESTINATION_FOLDER, filename)
            image = Image.open(path)
            new_img = replace_colors(image)
            new_img.save(destinationPath)
            print(f"Processed {filename}")

process_images()
