import pyautogui
import time
import mss
import numpy as np
import keyboard
from rich.console import Console
from PIL import Image
console = Console()

def check_word_status(start_button_x, start_button_y):
    # Get current mouse position
    x, y = pyautogui.position()

    # Use mss for faster screen capture
    with mss.mss() as sct:
        # Capture area around start position
        bbox = {"top": start_button_y - 200, "left": start_button_x - 400,
                "width": 800, "height": 100}
        screen = sct.grab(bbox)

        # Convert to PIL Image for OCR
        screen_pil = Image.frombytes('RGB', screen.size, screen.rgb)

        # save image
        screen_pil.save("screen.png")

        # Use pytesseract to detect text
        import pytesseract
        word = pytesseract.image_to_string(screen_pil).strip()

        if word:
            # Return the detected word if found
            return word
        return None

def main():
    console.print("[bold cyan]Verbal Memory Bot Starting...[/bold cyan]")
    console.print("[yellow]Position your cursor over the start button and press Enter when ready...[/yellow]")
    console.print("[red]Press 'q' to quit at any time[/red]")
    input()  # Wait for Enter key

    start_button_x, start_button_y = pyautogui.position()
    pyautogui.click(start_button_x, start_button_y)

    # Set pyautogui to be faster
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0

    # Store seen words
    seen_words = set()
    words_processed = 0

    # Calculate button positions relative to start position
    new_button_x = start_button_x + 100
    seen_button_x = start_button_x - 100
    button_y = start_button_y - 70

    while True:
        if keyboard.is_pressed('q'):
            console.print("[bold red]Stopping bot...[/bold red]")
            break

        if words_processed >= 400:
            console.print("[bold green]Reached 400 words! Stopping...[/bold green]")
            return

        word = check_word_status(start_button_x, start_button_y)

        if word in seen_words:
            seen_words.add(word)
            words_processed += 1
            pyautogui.moveTo(seen_button_x, button_y)
            pyautogui.click()
            console.print(f"[bold green]{word} SEEN ({words_processed}/300)[/bold green]")
        else:
            seen_words.add(word)
            words_processed += 1
            pyautogui.moveTo(new_button_x, button_y)
            pyautogui.click()
            console.print(f"[bold red]{word} NEW ({words_processed}/300)[/bold red]")

        time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    main()
