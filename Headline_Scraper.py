import requests
from bs4 import BeautifulSoup
import ollama
import newspaper
import lxml
import os
import json

CONFIG_FILE = "config.json"

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def ensure_model_installed(model_name):
    """Checks if the model exists; if not, downloads it."""
    try:
        print(f"Verifying model: {model_name}...")
        local_models = ollama.list()['models']
        model_names = [m['model'] for m in local_models]
        
        if model_name in model_names or f"{model_name}:latest" in model_names:
            print("Model ready.")
            return True
            
        print(f"Model {model_name} not found. Downloading now (this may take a bit)...")
        ollama.pull(model_name)
        print("Download complete!")
        return True
    except Exception as e:
        print(f"Ollama Connection Error: {e}. Make sure Ollama is running!")
        return False

def get_model_choice():
    """Handles persistent config and first-time RAM setup."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            model = config.get("model_name")
            if ensure_model_installed(model):
                return model

    print("\n--- First Time Setup ---")
    try:
        ram = int(input("How many GB of RAM does your system have? "))
    except ValueError:
        ram = 8

    if ram >= 32:
        model_name = "mistral-nemo:12b"
    elif ram >= 16:
        model_name = "mistral:latest"
    else:
        model_name = "llama3.2:3b"

    if ensure_model_installed(model_name):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"model_name": model_name, "ram": ram}, f)
        print(f"Configuration saved! Using {model_name}.\n")
        return model_name
    return None

def get_headline(url):
    try:
        response = requests.get(url, headers=header, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for tag in soup.find_all(['h2','h3']):
            a_tag = tag.find('a')
            if a_tag and 'href' in a_tag.attrs:
                link = a_tag['href']
                if link.startswith('http') and link not in links:
                    links.append(link)
        
        headlines = []
        for link in links[:9]:
            try:
                article = newspaper.Article(link)
                article.download()
                article.parse()
                if article.title:
                    headlines.append(article.title)
            except:
                continue
        return headlines
    except:
        return []

def local_news():
    headlines = []
    links = ["https://www.banatulmeu.ro/", "https://www.tion.ro/"]
    for link in links: headlines.extend(get_headline(link))
    return headlines

def national_news():
    headlines = []
    links = ["https://observatornews.ro/", "https://www.digi24.ro/", "https://stirileprotv.ro/"]
    for link in links: headlines.extend(get_headline(link))
    return headlines

def international_news():
    headlines = []
    links = [
        "https://www.bbc.com/news/world-europe-66844177",
        "https://www.cnn.com/world",
        "https://www.npr.org/sections/world/",
        "https://www.reuters.com/world/"
    ]
    for link in links: headlines.extend(get_headline(link))
    return headlines

def __main__():
    chosen_model = get_model_choice()
    if not chosen_model:
        return

    print(f"\nActive Model: {chosen_model}")
    print("1. Local News\n2. National News\n3. International News\n4. Reset Hardware Config")
    
    choice = input("Enter choice: ")

    if choice == '4':
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            print("Config deleted. Restart the script to reconfigure.")
        return
    
    if choice == '1':
        headlines = local_news()
    elif choice == '2':
        headlines = national_news()
    elif choice == '3':
        headlines = international_news()
    else:
        print("Invalid choice.")
        return

    if not headlines:
        print("No headlines found. Check your internet connection.")
        return

    print("\nGenerating your spicy summary...\n")
    
    try:
        response = ollama.chat(
            model=chosen_model,
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a cynical, tragic-comedic news anchor. "
                        "Turn the provided headlines into a single, cohesive, 'spicy' paragraph. "
                        "Keep it short and punchy with a darkly humorous twist. No bullet points. "
                        "Match the language of the headlines (Romanian for Romanian, English for English)."
                    )
                },
                {
                    "role": "user", 
                    "content": f"Connect these headlines: {headlines}"
                }
            ]
        )
        print("--- THE DAILY TRAGEDY ---")
        print(response['message']['content'])
        print("--------------------------")
    except Exception as e:
        print(f"Error talking to AI: {e}")

if __name__ == "__main__":
    __main__()