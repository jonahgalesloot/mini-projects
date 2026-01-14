# Stealth Jumpscare

## Purpose  
Sneaky jumpscare prank that was inspired by a questionable drawing by my friend, hides a fullscreen OpenCV window (featuring said drawing) offscreen, then reveals it with randomized timing and a loud scream. Uses WindowsAPI calls to strip windows borders and taskbar visibility for maximum surprise. 

## How It Works  
- Fullscreen OpenCV window created at monitor resolution, made borderless/topmost via `ctypes` Windows API.  
- Window positioned offscreen (`-width*2, -height*2`) during "hidden" state.  
- Random wait (normal dist. μ=60s, σ=30s), then instant reposition to `(0,0)` + scream playback. Exact timings can be adjusted within the script
- Audio resampled via NumPy interpolation for randomized pitch variation (speed_factor ±10%).  
- Loops indefinitely until 'q' pressed or window closed.

## Included Files  
- `main.py`: Core script with window manipulation, timing logic, audio processing.  
- `scare.jpg`: Jumpscare image (fullscreen display).  
- `scream.wav`: Base audio file (pitch-shifted on each scare).

Image and audio can be changed by adding other files to the directory with these names, this program has been tested with `png` and `jpg` images, and `mp3` and `wav` audio formats. 

## Prerequisites  
- Python 3.10+  
- Windows (WinAPI calls)  
- `pip install opencv-python pygame screeninfo numpy`

## Usage  
```bash
python jumpscare.py
```
- Made as a prank tool that hides itself from the user, until it doesn't...

