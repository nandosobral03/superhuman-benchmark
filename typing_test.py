import pyautogui
import mss
import numpy as np
import time
import keyboard
from rich.console import Console
import pytesseract
from PIL import Image

console = Console()

def capture_text_area(start_button_x, start_button_y):
    with mss.mss() as sct:
        # Capture area above the start button where text typically appears
        bbox = {"top": start_button_y-50 , "left": start_button_x - 50, "width": 1000, "height": 200}
        screen = sct.grab(bbox)

        # Convert to PIL Image for OCR
        img = Image.frombytes("RGB", screen.size, screen.rgb)

        # Open saved image
        img = Image.open("typing_test_capture.png")

        # Extract text using OCR
        text = pytesseract.image_to_string(img)
        # Remove special characters
        text = ''.join(c for c in text if c not in '|[]').replace('\n', ' ').replace('  ', ' ')
        return text.strip()

def type_text(text):
    # Type the entire text at once for maximum speed
    pyautogui.write(text, interval=0.0001)
    if keyboard.is_pressed('q'):
        return False
    return True

def main():
    console.print("[bold cyan]Typing Test Bot Starting...[/bold cyan]")
    console.print("[yellow]Position your cursor over the first word and press Enter when ready...[/yellow]")
    console.print("[red]Press 'q' to quit at any time[/red]")
    input()

    # Get start button position
    start_button_x, start_button_y = pyautogui.position()
    pyautogui.click(start_button_x, start_button_y)
    time.sleep(1)  # Wait for test to start

    while True:
        if keyboard.is_pressed('q'):
            console.print("[bold red]Stopping bot...[/bold red]")
            break

        # Capture and read the text
        text = capture_text_area(start_button_x, start_button_y)

        if text:
            console.print(f"[green]Detected text: {text}[/green]")

            # Type the text
            if not type_text(text):
                break

            # Wait for next test
            time.sleep(2)
            pyautogui.click(start_button_x, start_button_y)
            time.sleep(1)

        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    main()
