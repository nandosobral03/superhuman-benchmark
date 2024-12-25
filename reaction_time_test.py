import pyautogui
import time
import mss
import numpy as np
import keyboard
from rich.console import Console

console = Console()

def check_color():
    # Get current mouse position
    x, y = pyautogui.position()

    # Use mss for faster screen capture
    with mss.mss() as sct:
        # Capture single pixel at cursor position
        bbox = {"top": y, "left": x, "width": 1, "height": 1}
        screen = sct.grab(bbox)

        # Get RGB values of the pixel
        pixel = screen.pixel(0,0)
        r = pixel[0]
        g = pixel[1]
        b = pixel[2]

        # Check if pixel is green (high green, low red and blue)
        if g > 200 and r < 150 and b < 150:
            return "green"
        # Check if pixel is blue (high blue, low red and green)
        elif b > 200 and r < 150 and g < 150:
            return "blue"
        return None

def main():
    console.print("[bold cyan]Reaction Time Test Bot Starting...[/bold cyan]")
    console.print("[yellow]Position your cursor over the test area and press Enter when ready...[/yellow]")
    console.print("[red]Press 'q' to quit at any time[/red]")
    input()  # Wait for Enter key

    blue_count = 0
    last_color = None

    while True:
        if keyboard.is_pressed('q'):  # Check if q is pressed
            console.print("[bold red]Stopping bot...[/bold red]")
            break

        current_color = check_color()

        if current_color:
            pyautogui.click()

            if current_color == "green":
                console.print("[green]Click![/green]")
                blue_count = 0
            elif current_color == "blue":
                console.print("[blue]Next[/blue]")
                if last_color == "blue":
                    blue_count += 1
                    if blue_count >= 2:
                        console.print("[bold red]Two blues in a row - stopping bot...[/bold red]")
                        break
                else:
                    blue_count = 1

            last_color = current_color
            time.sleep(0.001)  # Wait before checking again

        time.sleep(0.001)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    main()
