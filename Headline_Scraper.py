import requests
from bs4 import BeautifulSoup
import ollama
import newspaper
import lxml

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}



def get_headline(url):
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []

    for tag in soup.find_all(['h2','h3']):
        a_tag = tag.find('a')
        if a_tag and 'href' in a_tag.attrs:
            link = a_tag['href']
            if link.startswith('http') and link not in links:
                links.append(link)

    print(len(links))

    headlines = []
    for link in links[:9]:
        try:
            article = newspaper.Article(link)
            article.download()
            article.parse()
            headline = article.title
            if headline:
                headlines.append(headline)
        except Exception as e:
            print(f"Error processing {link}: {e}")

    return headlines


def local_news():
    local_headliness = []
    links = [
        "https://www.banatulmeu.ro/",
        "https://www.tion.ro/"
    ]
    for link in links:
        local_headliness.extend(get_headline(link))
    return local_headliness

def national_news():
    national_headliness = []
    links = [
        "https://observatornews.ro/",
        "https://www.digi24.ro/",
        "https://stirileprotv.ro/"
        
    ]
    for link in links:
        national_headliness.extend(get_headline(link))
    return national_headliness

def international_news():
    international_headliness = []
    links = [
        "https://www.bbc.com/news/world-europe-66844177",
        "https://www.cnn.com/world",
        "https://www.npr.org/sections/world/",
        "https://www.reuters.com/world/"
    ]
    for link in links:
        international_headliness.extend(get_headline(link))
    return international_headliness

def __main__():
    print("Choose your poison for today\n" \
    "1. Local News\n" \
    "2. National News\n"\
    "3. International News\n")
    choice = input("Enter your choice (1, 2, or 3): ")
    if choice == '1':
        headlines = local_news()
    elif choice == '2':
        headlines = national_news()
    elif choice == '3':
        headlines = international_news()
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return
    
    response = ollama.chat(
        model="mistral-nemo:12b",
        # Use a more specific System Prompt to control the structure
        messages=[
            {
                "role": "system", 
                "content": (
                    "You are a cynical, tragic-comedic news anchor. "
                    "Your task is to take a list of headlines a nd turn them into a single, "
                    "cohesive, 'spicy' paragraph of text. "
                    "keep it short and punchy, like a news summary, but with a darkly humorous twist. "
                    "DO NOT use bullet points. DO NOT simply repeat or rephrase the headlines. "
                    "Instead, weave them together into a narrative about the state of the world. "
                    "Feel free to use strong language and a dark, comedic tone to present the 'big picture'."
                    "Use the language that most headlines are written in, for example when all the headlines are in romanian, use romanian language to write the paragraph. When all the headlines are in english, use english language to write the paragraph."
                )
            },
            {
                "role": "user", 
                "content": f"Connect these headlines into one cohesive, tragic-comedic paragraph: {headlines}"
            }
        ]
    )
    print(response['message']['content'])


if __name__ == "__main__":    __main__()
