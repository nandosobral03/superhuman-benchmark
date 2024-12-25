import pyautogui
import mss
from rich.console import Console
import numpy as np
import time
import keyboard
import pytesseract
from PIL import Image

console = Console()

def get_numbers_and_positions(start_button_x, start_button_y):
    # Use mss for faster screen capture
    while True:  # Keep trying until we get sequential numbers
        with mss.mss() as sct:
            # Capture area around start position
            bbox = {"top": start_button_y - 450, "left": start_button_x - 400,
                    "width": 800, "height": 550}
            screen = sct.grab(bbox)

            # Convert to numpy array for processing
            screen_array = np.array(screen)
            # Convert to PIL Image for OCR
            pil_image = Image.fromarray(screen_array)

            # Convert to grayscale for better OCR
            gray = np.array(pil_image.convert('L'))

            # Threshold to isolate white borders
            threshold = 150
            white_mask = gray > threshold

            # Find contours of white borders
            from scipy import ndimage
            labeled_array, num_features = ndimage.label(white_mask)

            # Store regions by their numbers to handle duplicates
            number_regions = {}
            failed_regions = []

            # Process each contour
            for label in range(1, num_features + 1):
                # Get bounding box for this contour
                y_indices, x_indices = np.where(labeled_array == label)
                if len(x_indices) == 0 or len(y_indices) == 0:
                    continue

                # Calculate bounding box
                x_min, x_max = np.min(x_indices), np.max(x_indices)
                y_min, y_max = np.min(y_indices), np.max(y_indices)

                # Check if bounding box is reasonable size for a number
                width = x_max - x_min
                height = y_max - y_min
                if width < 20 or height < 20 or width > 100 or height > 100:
                    continue

                # Calculate area early to filter small regions
                area = width * height
                if area < 5000:  # Skip regions smaller than 6000 pixels
                    continue

                # Extract region with padding for OCR
                padding = 5  # Increased padding for better context
                region = gray[max(0, y_min-padding):min(gray.shape[0], y_max+padding),
                             max(0, x_min-padding):min(gray.shape[1], x_max+padding)]

                # Enhance contrast for better number recognition
                region = np.clip((region - region.min()) * (255.0 / (region.max() - region.min())), 0, 255).astype(np.uint8)

                # Try multiple OCR configurations for better 9 recognition
                configs = [
                    '--psm 11 --oem 3 -c tessedit_char_whitelist=0123456789',
                    '--psm 9 --oem 3 -c tessedit_char_whitelist=0123456789',
                    '--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789',
                    '--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789',
                    '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789'
                ]

                number = None
                for config in configs:
                    try:
                        result = pytesseract.image_to_string(region, config=config).strip()
                        if result and result.isdigit():
                            number = int(result)
                            break
                    except (ValueError, AttributeError):
                        continue

                if number is not None:
                    # Debug: Print successful OCR results
                    console.print(f"[green]Successfully read number {number} from region {label}[/green]")
                else:
                    console.print(f"[red]Failed to read number from region {label}[/red]")
                    # Calculate center position for failed region
                    center_x = start_button_x + (x_min + x_max)//2 - 400
                    center_y = start_button_y + (y_min + y_max)//2 - 450
                    # Store failed region info
                    failed_regions.append(((center_x, center_y), (width, height), area))
                    continue

                # Calculate center position relative to screen
                center_x = start_button_x + (x_min + x_max)//2 - 400  # Adjust for bbox offset
                center_y = start_button_y + (y_min + y_max)//2 - 450  # Adjust for bbox offset

                # If we've seen this number before, keep only the larger region
                if number in number_regions:
                    old_area = number_regions[number][2]
                    if area > old_area:
                        number_regions[number] = ((center_x, center_y), (width, height), area)
                else:
                    number_regions[number] = ((center_x, center_y), (width, height), area)

            # Convert dictionary to sorted list of (number, position) tuples
            number_positions = [(num, pos[0]) for num, pos in sorted(number_regions.items())]

            # Check if numbers are sequential
            numbers = [num for num, _ in number_positions]
            if not numbers:
                continue

            # Try to infer missing number if exactly one region failed
            if len(failed_regions) == 1 and len(numbers) >= 2:
                # Get the expected sequence from 1 to the max number found
                expected_sequence = list(range(1, max(numbers) + 1))
                # Find which numbers are missing
                missing_numbers = [n for n in expected_sequence if n not in numbers]

                if len(missing_numbers) == 1:
                    missing_number = missing_numbers[0]
                    failed_pos, failed_dims, failed_area = failed_regions[0]
                    number_regions[missing_number] = (failed_pos, failed_dims, failed_area)
                    # Update numbers list with the newly added missing number
                    number_positions = [(num, pos[0]) for num, pos in sorted(number_regions.items())]
                    numbers = [num for num, _ in number_positions]

            expected_sequence = list(range(min(numbers), max(numbers) + 1))
            if numbers == expected_sequence:
                # Debug: Print final results
                console.print(f"[cyan]Found {len(number_positions)} valid sequential numbers[/cyan]")
                return number_positions
            else:
                console.print("[yellow]Numbers not sequential, retrying...[/yellow]")
                time.sleep(0.1)  # Brief pause before retrying

def main():
    console.print("[bold cyan]Chimp Test Bot Starting...[/bold cyan]")
    console.print("[yellow]Position your cursor over the start button and press Enter when ready...[/yellow]")
    console.print("[red]Press 'q' to quit at any time[/red]")
    input()  # Wait for Enter key

    # Get start position
    start_button_x, start_button_y = pyautogui.position()

    # Click to start
    pyautogui.click(start_button_x, start_button_y)
    time.sleep(1)  # Wait for game to start

    sequence_length = 0

    while True:
        if keyboard.is_pressed('q'):
            console.print("[bold red]Stopping bot...[/bold red]")
            break

        # Get numbers and their positions
        number_positions = get_numbers_and_positions(start_button_x, start_button_y)

        if not number_positions:
            break



        # Click numbers in sequence
        for number, pos in number_positions:
            console.print(f"[cyan]Clicking number {number} at position ({pos[0]}, {pos[1]})[/cyan]")
            pyautogui.moveTo(pos[0], pos[1])
            time.sleep(0.05)  # Brief pause to see cursor position
            pyautogui.click()
            time.sleep(0.05)  # Wait between clicks

        sequence_length = len(number_positions)
        if sequence_length >= 40:
            console.print("[bold green]Reached 40 digit sequence! Stopping...[/bold green]")
            break

        time.sleep(1)  # Wait for next round

        # Click continue/next button (approximately same position as start)
        pyautogui.click(start_button_x, start_button_y)
        time.sleep(1)

        time.sleep(0.001)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    main()
