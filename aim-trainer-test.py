import pyautogui
import time
import mss
import numpy as np
import keyboard
from rich.console import Console
from PIL import Image


console = Console()

def check_target(start_button_x, start_button_y):
    # Get current mouse position
    x, y = pyautogui.position()

    # Use mss for faster screen capture
    with mss.mss() as sct:
        # Capture area around start position
        bbox = {"top": start_button_y - 200, "left": start_button_x - 400,
                    "width": 800, "height": 400}
        screen = sct.grab(bbox)

        # Convert to numpy array and use more efficient boolean indexing
        screen_array = np.array(screen)
        white_mask = (screen_array[:, :, 0] > 250) & (screen_array[:, :, 1] > 250) & (screen_array[:, :, 2] > 250)
        white_pixels = np.nonzero(white_mask)

        if white_pixels[0].size > 0:
            # Get the first white pixel found
            target_y = white_pixels[0][0]
            target_x = white_pixels[1][0]

            # Convert coordinates relative to the bbox
            absolute_x = target_x + bbox["left"]
            absolute_y = target_y + bbox["top"] + 50

            return absolute_x, absolute_y

        return None, None

def main():
    console.print("[bold cyan]Aim Trainer Bot Starting...[/bold cyan]")
    console.print("[yellow]Position your cursor over the target area and press Enter when ready...[/yellow]")
    console.print("[red]Press 'q' to quit at any time[/red]")
    input()  # Wait for Enter key

    start_button_x, start_button_y = pyautogui.position()
    pyautogui.click(start_button_x, start_button_y)

    # Set pyautogui to be faster
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0

    targets_hit = 0

    while True:
        if keyboard.is_pressed('q'):
            console.print("[bold red]Stopping bot...[/bold red]")
            break

        target_x, target_y = check_target(start_button_x, start_button_y)
        if target_x and target_y:
            pyautogui.moveTo(target_x, target_y, duration=0)
            pyautogui.click()
            targets_hit += 1
            console.print(f"[green]Target hit! ({targets_hit}/30)[/green]", end='\r')

            if targets_hit >= 30:
                console.print("[bold green]Reached 30 targets! Stopping...[/bold green]")
                break

        # Reduced sleep time
        time.sleep(0.01)  # Minimal delay to prevent excessive CPU usage

        # Click continue/next button after completing round
        if targets_hit >= 30:
            time.sleep(1)  # Wait for next round
            return

if __name__ == "__main__":
    main()
