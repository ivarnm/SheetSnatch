import os
from PIL import Image, ImageDraw, ImageFont
import re

# === CONFIGURATION ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = os.path.join(SCRIPT_DIR, "processed_screenshots")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "output/piano_sheet.pdf")

A4_WIDTH_PX = 2480   # A4 at 300 DPI (8.27 x 11.69 inches)
A4_HEIGHT_PX = 3508
MARGIN_X = 150          # pixels on each side
MARGIN_Y = 100          # pixels on top and bottom
CONTENT_WIDTH = A4_WIDTH_PX - 2 * MARGIN_X
CONTENT_HEIGHT = A4_HEIGHT_PX - 2 * MARGIN_Y

TITLE = "Your Title Here"
TITLE_HEIGHT = 150
FONT_SIZE = 64
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
# ======================

def load_and_resize_images(folder, max_width):
    def numerical_sort_key(filename):
      return [int(part) if part.isdigit() else part.lower()
              for part in re.split(r'(\d+)', filename)]

    images = []
    for filename in sorted(os.listdir(folder), key=numerical_sort_key):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder, filename)
            img = Image.open(path)
            w_percent = max_width / float(img.width)
            h_size = int(img.height * w_percent)
            resized = img.resize((max_width, h_size), Image.LANCZOS)
            images.append(resized)
    return images

def get_font(font_size=FONT_SIZE):
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except IOError:
        print(f"Font not found at {FONT_PATH}. Using default font.")
        font = ImageFont.load_default()
    return font

def create_title_banner(width, height, text):
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = get_font()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    pos = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(pos, text, font=font, fill=(0, 0, 0))
    return img

def add_page_number(page_img, page_num, total_pages, margin_y):
    draw = ImageDraw.Draw(page_img)
    text = f"{page_num} / {total_pages}"
    font = get_font(font_size=46)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (page_img.width - text_width) // 2
    y = page_img.height - margin_y - bbox[3]
    draw.text((x, y), text, fill=(0, 0, 0), font=font)

def create_pages(images, page_width, page_height, margin_x, margin_y, title_img=None):
    pages = []
    current_y = margin_y + (title_img.height if title_img else 0)
    current_page = Image.new("RGB", (page_width, page_height), color=(255, 255, 255))

    if title_img:
        current_page.paste(title_img, (margin_x, margin_y))

    for img in images:
        if current_y + img.height > page_height - margin_y:
            pages.append(current_page)
            current_page = Image.new("RGB", (page_width, page_height), color=(255, 255, 255))
            current_y = margin_y
        current_page.paste(img, (margin_x, current_y))
        current_y += img.height

    pages.append(current_page)

    for i, page in enumerate(pages):
        add_page_number(page, i + 1, len(pages), margin_y)

    return pages

def main():
    images = load_and_resize_images(IMAGE_FOLDER, CONTENT_WIDTH)
    if not images:
        print("No images found.")
        return

    title_img = create_title_banner(CONTENT_WIDTH, TITLE_HEIGHT, TITLE)
    pages = create_pages(images, A4_WIDTH_PX, A4_HEIGHT_PX, MARGIN_X, MARGIN_Y, title_img)

    print(f"Saving {len(pages)} pages to {OUTPUT_FILE}")
    pages[0].save(OUTPUT_FILE, "PDF", resolution=300.0, save_all=True, append_images=pages[1:])

if __name__ == "__main__":
    main()
