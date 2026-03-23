import re
import requests
import bs4
# from selenium import webdriver
# from selenium.webdriver.edge.service import Service
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

class Song_Scrapper:
    def __init__(self):
        self._spotify_song_regex=r"(open).(spotify).(com)[/](track)"
        self._soundcloud_song_regex=r""

    # TODO: write regex for soundcloud links
    def get_song_title(self, url) -> str | None:
        if re.search(self._spotify_song_regex, url) is not None:
            response=requests.get(url)
            soup = bs4.BeautifulSoup(response.content, 'html.parser')
            og_title=soup.find('meta', property='og:title')

            if og_title and og_title.get('content'):
                title_content=og_title['content']
                return title_content 
        
        return None

    # def check(self, url):
    #     reg = re.match()
    #     enumerate()

if __name__=='__main__':
    scrp = Song_Scrapper()
    title=scrp.get_song_title('https://open.spotify.com/track/4Y53Vi8Uwo47odD10w5Lv3?si=e0ebfda753d1440c')
    print(title)