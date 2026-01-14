**AI Fact-Checker**

- **Purpose:** A proof of concept of a quick and accessible truth verifier, built to combat misinformation online. It cross-references multiple Wikipedia articles (used as a temporary source, I intend to expand the project to general internet searches) and uses a locally-run LLM (currently configured to Bespoke Minichack, which I found to be fast and reliable) to analyse sources individually, before running a "synthesis" pass to handle contradictions. 

**Included Files**

- `main.py`: The core logic containing the `tkinter` GUI, Wikipedia API orchestration, and the dual-stage AI prompting/parsing system.

**Prerequisites**

- Python 3.10+
- [Ollama](ollama.com) (Local LLM runner)
- A machine capable of running local models (8GB+ RAM recommended)

**Quick Setup**

1. Install the Python dependencies:
   ```powershell
   python -m pip install ollama wikipedia-api wikipedia

2. Ollama Setup & Model Installation:
    This project requires Ollama to be running in the background.
    Step 1: Download and install the Ollama Client.
    Step 2: Open your terminal and pull the specific fact-checking model used in this code:
    '''powershell
    ollama pull bespoke-minicheck


**Usage Tutorial**
- Wikipedia Mode: Enter a claim. The app will scrape the top 3 relevant Wikipedia entries and provide a synthesized truth-score.
- Manual Mode: Click "Use Manual Input" to paste a specific document or news article you want the AI to verify against your statement.
- Console Monitoring: The terminal will display the "raw" AI thinking process and individual article processing times for performance tracking.

