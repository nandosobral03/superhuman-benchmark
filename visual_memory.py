import pyautogui
import mss
from rich.console import Console
import numpy as np
import time
import keyboard
from scipy.ndimage import label
from PIL import Image

console = Console()

def find_white_squares(start_button_x, start_button_y):
    # Use mss for faster screen capture
    with mss.mss() as sct:
        # Capture area around cursor position
        bbox = {"top": start_button_y - 300, "left": start_button_x - 200, "width": 400, "height": 400}
        screen = sct.grab(bbox)

        # Convert to numpy array for faster processing
        screen_array = np.array(screen)

        # Check if any pixels are white (all values high)
        white_pixels = np.all(screen_array[:, :, :3] > 250, axis=2)

        # Use scipy's label to identify connected components (squares)
        labeled_array, num_features = label(white_pixels)

        white_squares = []
        for i in range(1, num_features + 1):
            # Get coordinates of pixels in this square
            y_coords, x_coords = np.where(labeled_array == i)

            if len(x_coords) > 10:  # Filter out noise - require minimum size
                # Calculate center of the square
                center_x = start_button_x + np.mean(x_coords) - 200
                center_y = start_button_y + np.mean(y_coords) - 300
                white_squares.append((center_x, center_y))

        return white_squares

def main():
    console.print("[bold cyan]Visual Memory Bot Starting...[/bold cyan]")
    console.print("[yellow]Position your cursor over the start button and press Enter when ready...[/yellow]")
    console.print("[red]Press 'q' to quit at any time[/red]")
    input()  # Wait for Enter key

    # Get start button position
    start_button_x, start_button_y = pyautogui.position()
    pyautogui.click(start_button_x, start_button_y)
    time.sleep(1)  # Wait for game to start

    level = 1
    while level <= 30:  # Stop after level 30
        if keyboard.is_pressed('q'):
            console.print("[bold red]Stopping bot...[/bold red]")
            break

        # Wait for white squares to appear
        time.sleep(0.5)
        white_squares = find_white_squares(start_button_x, start_button_y)

        if white_squares:
            console.print(f"[green]Level {level}: Found {len(white_squares)} white squares[/green]")
            time.sleep(1)  # Wait for squares to change back

            # Click each remembered position
            for i, pos in enumerate(white_squares, 1):
                console.print(f"[cyan]Clicking position ({pos[0]:.0f}, {pos[1]:.0f}) - Square {i} of {len(white_squares)}[/cyan]")
                pyautogui.moveTo(pos[0], pos[1])
                time.sleep(0.05)
                pyautogui.click()
                time.sleep(0.05)

            level += 1
            time.sleep(1)  # Wait for next round

        time.sleep(0.001)  # Small delay to prevent excessive CPU usage

    if level > 30:
        console.print("[bold green]Completed 30 levels! Stopping bot...[/bold green]")

if __name__ == "__main__":
    main()
