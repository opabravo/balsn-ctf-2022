import requests
import re
import bs4
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def get_soup(url: str) -> bs4.element:
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def find_flag_from_script(url: str) -> bool:
    print(f"[*] {url}")
    r = requests.get(url)
    if flag := re.findall(r"BALSN{.*?}", r.text):
        print(f"[+] {url}\nFound Flag: {flag[0]}")
        return True


URL = "http://my-first-web.balsnctf.com:3000/"
soup = get_soup(URL)
scripts = [s.attrs.get("src") for s in soup.find_all('script')]
urls = [URL + s for s in scripts if s]

with ThreadPoolExecutor(max_workers=10) as executor:
    for flag in executor.map(find_flag_from_script, urls):
        if flag:
            input()
            break
        