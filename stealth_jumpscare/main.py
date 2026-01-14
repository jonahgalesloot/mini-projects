import cv2, time, random, pygame
import numpy as np
import ctypes
from screeninfo import get_monitors

# Get the primary monitor's resolution
primary_monitor = next((m for m in get_monitors() if m.is_primary), None)
if primary_monitor:
    width, height = primary_monitor.width, primary_monitor.height
else:
    width, height = 1920, 1080  # Default fallback

# Initialize pygame mixer
pygame.mixer.init()

# Load and verify the scream sound
try:
    scream = pygame.mixer.Sound("scream.wav")
except pygame.error as e:
    raise FileNotFoundError("Error loading scream.wav: " + str(e))

# Convert sound to a NumPy array
arr = pygame.sndarray.array(scream)

# Windows API constants
WS_CAPTION = 0x00C00000
WS_THICKFRAME = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080  # Hides from taskbar
GWL_STYLE = -16
GWL_EXSTYLE = -20

def set_borderless(window_name):
    """Removes the border and hides the window from the taskbar."""
    hwnd = ctypes.windll.user32.FindWindowW(None, window_name)
    if hwnd == 0:
        print(f"Window '{window_name}' not found.")
        return

    # Remove title bar and border
    style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
    style &= ~(WS_CAPTION | WS_THICKFRAME)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)

    # Hide from taskbar
    ex_style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, ex_style | WS_EX_TOOLWINDOW)

    # Apply changes
    ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0002 | 0x0001 | 0x0020)

# Create a window for the jumpscare
cv2.namedWindow("jumpscare", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("jumpscare", cv2.WND_PROP_TOPMOST, 1)
time.sleep(0.1)  # Allow OpenCV to create the window before modifying it
set_borderless("jumpscare")
cv2.resizeWindow("jumpscare", width, height)

# Load and verify the image
img = cv2.imread("scare.jpg")
if img is None:
    raise FileNotFoundError("scare.jpg not found! Make sure it's in the script folder.")

cv2.imshow("jumpscare", img)

# Functions to hide/show the window
def windowHide():
    cv2.moveWindow("jumpscare", -width * 2, -height * 2)

def windowShow():
    cv2.moveWindow("jumpscare", 0, 0)

# Jumpscare loop
state = "dissapear"
while True:
    if cv2.waitKey(1) == ord('q') or cv2.getWindowProperty("jumpscare", cv2.WND_PROP_VISIBLE) < 1:
        break

    if state == "dissapear":
        actTime = time.time() + random.normalvariate(60, 10)
        state = "waiting appear"
        windowHide()

    elif state == "waiting appear":
        if time.time() > actTime:
            state = "appear"

    elif state == "appear":
        default = 0.25
        speed_factor = random.uniform(0.9, 1.1)
        actTime = time.time() + default * speed_factor**2  # More randomness
        state = "waiting dissapear"
        windowShow()

        if len(arr.shape) == 2:  # Stereo audio
            new_length = int(arr.shape[0] / speed_factor)
            resampled_arr = np.zeros((new_length, arr.shape[1]), dtype=np.int16)

            for i in range(arr.shape[1]):  # Process each channel separately
                resampled_arr[:, i] = np.interp(
                    np.linspace(0, arr.shape[0], new_length),
                    np.arange(arr.shape[0]),
                    arr[:, i]
                ).astype(np.int16)

        else:  # Mono audio
            new_length = int(len(arr) / speed_factor)
            resampled_arr = np.interp(
                np.linspace(0, len(arr), new_length),
                np.arange(len(arr)),
                arr
            ).astype(np.int16)

        # Convert back to a sound object and play
        new_sound = pygame.sndarray.make_sound(resampled_arr)
        new_sound.play()

    elif state == "waiting dissapear":
        if time.time() > actTime:
            state = "dissapear"

cv2.destroyAllWindows()
