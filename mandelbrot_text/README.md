**ANSI Mandelbrot Explorer**

- **Purpose:** An exploration of the Mandelbrot Set inspired by a math class. I took on the personal challenge of rendering the fractal within the standard windows terminal. To achieve "high resolution" renders", I used `pyautogui` to zoom the terminal out to its minimum font size, turning character cells into pixels before rendering the set. 


**Included Files**

- `main.py`: The core application containing the complex number iteration logic, coordinate-to-complex mapping, and the terminal manipulation system.

**Prerequisites**

- Windows machine (required for `msvcrt` and specific terminal behavior)
- Python 3.10+
- A terminal that supports ANSI TrueColor (24-bit)

**Quick Setup**

Install the necessary automation library via pip:

```powershell
python -m pip install pyautogui
