# IDL Newspaper Scraper

## Clone

bash
git clone https://github.com/PopetAndrei04/IDL-newspaper-Scraper.git
cd IDL-newspaper-Scraper


## Create a virtual environment

bash
python -m venv venv


Activate it:

bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (cmd)
venv\Scripts\activate.bat

# macOS / Linux
source venv/bin/activate


## Install Python dependencies

bash
pip install requests beautifulsoup4 lxml newspaper3k ollama


## Install Ollama

bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Windows: download the installer from https://ollama.com/download


## Start the Ollama server

bash
ollama serve


## Run

bash
python Headline_Scraper.py