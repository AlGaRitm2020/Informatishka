from bs4 import BeautifulSoup
import requests

def get_theory_video(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    youtube_link = soup.find('iframe')['src']
    youtube_link = youtube_link.replace('embed', 'watch')
    return youtube_link

if __name__ == '__main__':
    print(get_theory_video('https://code-enjoy.ru/ege_po_informatike_2021_zadanie_1_osobie_tochki/'))