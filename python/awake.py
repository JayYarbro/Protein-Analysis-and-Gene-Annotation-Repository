import pyautogui
import time

def keep_awake(interval=60):
    """
    Moves the mouse slightly every 'interval' seconds to prevent sleep.
    :param interval: Time in seconds between movements.
    """
    try:
        print("Keeping the system awake. Press Ctrl+C to stop.")
        while True:
            # Get the current position of the mouse
            x, y = pyautogui.position()

            # Move the mouse slightly
            pyautogui.moveTo(x + 1, y)
            time.sleep(1)
            pyautogui.moveTo(x - 1, y)

            # Wait for the specified interval before moving the mouse again
            time.sleep(interval - 1)
    except KeyboardInterrupt:
        print("Program stopped by the user.")

if __name__ == "__main__":
    keep_awake(60)  # Set the interval to 60 seconds or adjust as needed
