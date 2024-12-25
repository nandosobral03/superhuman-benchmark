import pyautogui
import mss
from rich.console import Console
import numpy as np
import time
import keyboard

console = Console()

square_size = 100


def draw_bbox(start_button_x, start_button_y):
    """Draw a rectangle to visualize the bounding box being checked"""
    x1 = start_button_x - 180
    y1 = start_button_y
    x2 = start_button_x + 180
    y2 = start_button_y - 300

    # Draw the corners
    console.print(f"[yellow]Bounding Box:[/yellow]")
    console.print(f"Top left: ({x1}, {y1})")
    console.print(f"Bottom right: ({x2}, {y2})")

    # Draw rectangle using pyautogui
    pyautogui.moveTo(x1, y1)
    pyautogui.dragTo(x2, y1, duration=0.2)
    pyautogui.dragTo(x2, y2, duration=0.2)
    pyautogui.dragTo(x1, y2, duration=0.2)
    pyautogui.dragTo(x1, y1, duration=0.2)

def get_position_category(x, y, start_x, start_y):
    # Define boundaries for 3x3 grid
    left_bound = start_x - 180
    right_bound = start_x + 180
    top_bound = start_y - 300
    bottom_bound = start_y

    third_width = (right_bound - left_bound) / 3
    third_height = (bottom_bound - top_bound) / 3

    # Determine horizontal position
    if x < left_bound + third_width:
        h_pos = "left"
    elif x < left_bound + 2 * third_width:
        h_pos = "middle"
    else:
        h_pos = "right"

    # Determine vertical position
    if y < top_bound + third_height:
        v_pos = "top"
    elif y < top_bound + 2 * third_height:
        v_pos = "middle"
    else:
        v_pos = "bottom"

    return f"{v_pos} {h_pos}"

def check_white(start_button_x, start_button_y):
    # Use mss for faster screen capture
    with mss.mss() as sct:
        # Capture area around cursor position
        bbox = {"top": start_button_y - 300, "left": start_button_x - 180, "width": 360, "height": 300}
        screen = sct.grab(bbox)

        # Convert to numpy array for faster processing
        screen_array = np.array(screen)

        # Check if any pixels are white (all values high)
        white_pixels = np.all(screen_array[:, :, :3] > 250, axis=2)

        # If white pixels found, get their coordinates
        if np.any(white_pixels):
            # Get indices of white pixels
            white_y, white_x = np.where(white_pixels)
            # Convert to actual screen coordinates
            screen_x = start_button_x + white_x[0] - 180 + square_size/2 # Add offset from bbox left
            screen_y = start_button_y + white_y[0] - 300 + square_size/2  # Add offset from bbox top
            return True, (screen_x, screen_y)

        return False, None

def main():
    console.print("[bold cyan]Sequence Memory Bot Starting...[/bold cyan]")
    console.print("[yellow]Position your cursor over the start button and press Enter when ready...[/yellow]")
    console.print("[red]Press 'q' to quit at any time[/red]")
    input()  # Wait for Enter key

    # Click to start
    start_button_x, start_button_y = pyautogui.position()

    # Draw the bounding box to visualize the area being checked
    # draw_bbox(start_button_x, start_button_y)

    pyautogui.click(start_button_x, start_button_y)
    time.sleep(1)  # Wait for game to start

    sequence = []
    watching = True
    last_found_time = 0
    expected_length = 1  # Track expected sequence length

    while True:
        if keyboard.is_pressed('q') or expected_length >= 30:  # Check if q is pressed or round 25 completed
            console.print("[bold red]Stopping bot...[/bold red]")
            break

        if watching:
            # Watch for white squares
            found, pos = check_white(start_button_x, start_button_y)
            if found:
                current_time = time.time()
                # Only add if enough time has passed since last white square
                if current_time - last_found_time > 0.45:
                    position_category = get_position_category(pos[0], pos[1], start_button_x, start_button_y)
                    sequence.append(pos)
                    console.print(f"[cyan]Added {position_category} position ({pos[0]}, {pos[1]}) to sequence[/cyan]")
                    # Move mouse to the white square when found
                    last_found_time = current_time
                time.sleep(0.1)  # Wait for square to return to blue

            # When sequence ends (no white squares for a while)
            if len(sequence) > 0 and time.time() - last_found_time > 0.9:
                if len(sequence) == expected_length:
                    watching = False
                    console.print(f"[green]Replaying sequence (Round {expected_length})...[/green]")

        else:
            # Replay the sequence as they appear
            for i, pos in enumerate(sequence, 1):
                position_category = get_position_category(pos[0], pos[1], start_button_x, start_button_y)
                console.print(f"[cyan]Clicking {position_category} position ({pos[0]}, {pos[1]}) - Step {i} of {len(sequence)}[/cyan]")
                # Move cursor first so user can see where it's going
                pyautogui.moveTo(pos[0], pos[1])
                time.sleep(0.05)  # Brief pause to see cursor position
                pyautogui.click()
                time.sleep(0.05)  # Wait between clicks

            # Reset for next round with increased sequence length
            sequence = []
            watching = True
            last_found_time = 0
            expected_length += 1  # Increment expected length for next round
            time.sleep(0.9)  # Wait for next sequence to start

        time.sleep(0.001)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    main()
