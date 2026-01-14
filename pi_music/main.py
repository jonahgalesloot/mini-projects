import array
import math
import time
import os
import pyaudio
from mpmath import mp

# Get user input with validation
while True:
    try:
        chars = int(input("How many decimal places of pi? "))
        mp.dps = chars + 2
        break  # Valid input, exit loop
    except ValueError:
        print("Please enter a valid integer.")

# Get pi with the specified precision
piString = str(mp.pi)

# Pi digits as a sequence (removes the decimal point)
pi = [int(char) for char in piString if char.isdigit()]

# Audio setup
p = pyaudio.PyAudio()
volume = 0.5  # Volume level (0.0 to 1.0)
fs = 44100  # Sampling rate (Hz)
duration = 0.5  # Duration of each note (seconds)
num_samples = int(fs * duration)  # Number of samples per note

# Define the pentatonic scale mapping (3 is A4)
notes = [
    {"key": "D5", "frequency": 587.33},   # 0
    {"key": "E5", "frequency": 659.26},   # 1
    {"key": "G5", "frequency": 783.99},   # 2
    {"key": "A4", "frequency": 440.0},    # 3 (Root)
    {"key": "C5", "frequency": 523.25},   # 4
    {"key": "D5", "frequency": 587.33},   # 5
    {"key": "E5", "frequency": 659.26},   # 6
    {"key": "G5", "frequency": 783.99},   # 7
    {"key": "A5", "frequency": 880.0},    # 8
    {"key": "C6", "frequency": 1046.5}    # 9
]

# Function to generate a sine wave for a given frequency
def generate_sine_wave(frequency):
    return [volume * math.sin(2 * math.pi * k * frequency / fs) for k in range(num_samples)]

waveforms = {num: array.array('f', generate_sine_wave(notes[num]["frequency"])) for num in range(10)}

# Open the PyAudio stream once
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)

# Play notes sequentially
for index, num in enumerate(pi):
    # Write the corresponding waveform to the stream
    stream.write(waveforms[num].tobytes())

    # Visualization: Display Pi digits graphically
    outp = f"Playing the first {chars} digits of Pi!\n"

    for i in range(10):
        row = 9 - i
        
        outp += f"{row}|"
        for j, height in enumerate(pi):  # Use 'j' instead of 'i'
            if j == index:
                outp += "\033[47m"  # Highlight the current note
            outp += "#" if height == row else " "
            outp += "\033[00m"  # Reset formatting
        outp += "\n"  # Newline at the end of each row

    outp += "_" * (len(pi) + 4) + "\n"
    outp += f"{num}: {notes[num]['key']} ({notes[num]['frequency']} Hz)\n"

    # Clear screen before updating (cross-platform compatibility)
    os.system("cls" if os.name == "nt" else "clear")

    # Print the final assembled output
    print(outp)

    # Small delay to allow display updates
    time.sleep(duration * 0.1)

# Close the stream properly after playing all notes
stream.stop_stream()
stream.close()
p.terminate()
