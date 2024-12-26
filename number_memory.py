import pyautogui
import time
import mss
import numpy as np
import keyboard
from rich.console import Console
from PIL import Image
console = Console()
import pytesseract


def check_number(start_button_x, start_button_y):
    # Use mss for faster screen capture
    with mss.mss() as sct:


        # Capture area around start position
        bbox = {"top": start_button_y - 200, "left": start_button_x - 500,
                "width": 1000, "height": 100}
        screen = sct.grab(bbox)

        # Convert to PIL Image for OCR
        screen_pil = Image.frombytes('RGB', screen.size, screen.rgb)

        # Convert to high contrast black and white
        screen_pil = screen_pil.convert('L')  # Convert to grayscale

        # Use threshold to convert to pure black and white
        threshold = 200  # Increased threshold to better handle white text
        screen_pil = screen_pil.point(lambda x: 255 if x < threshold else 0, '1')  # Inverted threshold logic


        # Save image for debugging
        debug_filename = "number_capture.png"
        screen_pil.save(debug_filename)

        # Use pytesseract to detect text with multiple configurations
        configs = [
            '--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789',
            '--psm 9 --oem 3 -c tessedit_char_whitelist=0123456789',
            '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789',
            '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789'
        ]

        results = []
        for config in configs:
            try:
                number = pytesseract.image_to_string(screen_pil, config=config).strip()
                if number and number.isdigit():  # Ensure we only get valid numbers
                    results.append(number)
            except Exception as e:
                console.print(f"[dim]OCR error with config {config}: {str(e)}[/dim]")

        if results:
            # Return most common result
            from collections import Counter
            most_common = Counter(results).most_common(1)[0][0]
            console.print(f"[dim]Raw results: {results}[/dim]")  # Debug output
            return most_common

        return None

def main():
    console.print("[bold cyan]Number Memory Bot Starting...[/bold cyan]")
    console.print("[yellow]Position your cursor over the start button and press Enter when ready...[/yellow]")
    console.print("[red]Press 'q' to quit at any time[/red]")
    input()  # Wait for Enter key

    start_button_x, start_button_y = pyautogui.position()
    pyautogui.click(start_button_x, start_button_y)

    # Set pyautogui to be faster
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0

    level = 0

    while True:
        if keyboard.is_pressed('q'):
            console.print("[bold red]Stopping bot...[/bold red]")
            break

        # Wait for number to appear and capture it
        number = check_number(start_button_x, start_button_y)

        if number:
            level += 1
            console.print(f"[bold green]Level {level}: Detected number {number}[/bold green]")

            # Wait for number to disappear and input field to show
            time.sleep(level + 0.5)  # Wait longer for higher levels

            # Type the number
            pyautogui.write(number)
            time.sleep(0.5)

            # Press Enter
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.press('enter')

        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    main()
