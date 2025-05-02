# Piano Sheet Screenshot Processor

Have you ever tried to find a good score for a music piece, only to end up with a YouTube video showing images of each row of the score, but with no link to buy the sheet music? This project lets you take screenshots of a specified part of your screen, process the images to remove unwanted artifacts, and combine them into a print-friendly PDF.

This is _not_ a fully automated process. You'll need to modify configuration values in the Python files to specify the screenshot area, color replacements, font path, etc. Familiarity with Python is recommended.

Contributions are welcome! Feel free to make a PR if you'd like to improve the project.

## Features
1. **Capture a fixed part of your screen** using a hotkey.
2. **Process the screenshots** by replacing specific colors with black, white, or gray.
3. **Convert the processed images into a printable PDF** (A4 pages, margins, page numbers, and title).


## Requirements
- Python 3
- Pip


## Setup
1. Clone or download this repository.
2. Open a terminal in the folder and run:

```bash
pip install -r requirements.txt
```

## Usage
### 1. Take screenshots
Open `screenshot_area.py` and change the configuration variables at the top of the file. Most importantly, change `CAPTURE_BOX` to your desired screenshot area, and optionally adjust `TRIGGER_HOTKEY`.

Then run the script:

```bash
python screenshot_area.py
```

Each time you press the configured hotkey (default: Ctrl+K), a screenshot will be saved in the `screenshots` folder.

### 2. Process screenshots
YouTube videos often contain visual artifacts like a vertical playback bar or slightly off-white backgrounds. The `process_screenshots.py` script allows you to replace specific colors with black, white, or gray.

Edit `process_screenshots.py` and set RGB values for the `REPLACE_WITH_BLACK`, `REPLACE_WITH_WHITE`, and `REPLACE_WITH_GRAY` lists. Leave a list empty if you don’t want to replace that color. `FUZZY_THRESHOLD` determines how similar a color must be to be replaced.

Then run:

```bash
python process_screenshots.py
```

Check the `processed_screenshots` folder to verify the results. Tweak the replacement values if needed.


### 3. Generate PDF
To combine the processed screenshots into a PDF:
1. Open `combine_to_pdf.py` and configure the `TITLE` and `FONT_PATH` values.
1. Then run:
```bash
python combine_to_pdf.py
```
The script will generate a PDF in the `output` folder.


## Contributing
I do not plan to maintain or improve this project further, but feel free to create a pull request if you'd like to contribute. There are many areas for potential improvement!