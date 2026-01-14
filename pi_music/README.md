**Pi Sonification & Visualizer**

- **Purpose:** For Pi Day 2025, I wanted to push myself to remember 30 digits of Pi. This tool was created to help me with this, by turning a sequence of numbers to a melody. By mapping digits to a specific pentatonic scale, it ensures that all parts of Pi are musically harmonious. The program also includes a histogram that highlights notes being played


**Included Files**

- `main.py`: The standalone application — calculates Pi to user-defined precision, generates sine wave audio buffers, and renders the terminal visualization.

**Prerequisites**

- Windows machine (tested on Windows 11)
- Python 3.10+
- A working audio output device

**Quick Setup**

This project requires two external libraries for high-precision math and audio output. Install them via pip:

```powershell
python -m pip install mpmath pyaudio
