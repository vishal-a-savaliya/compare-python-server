from logging import exception
import requests,json
from bs4 import BeautifulSoup
from tldextract import extract


def getSite(search):

    # URL
    url = [f"https://www.google.co.in/search?hl=en-IN&gl=IN&ceid=IN:en&q={search}",
           f"https://www.google.co.in/search?hl=en-IN&gl=IN&ceid=IN:en&q={search}&start=10",
           f"https://www.google.co.in/search?hl=en-IN&gl=IN&ceid=IN:en&q={search}&start=20"
           ]

    data = set()

    for u in url:
        searchSite(u, data)

    # data = {'sites':data }

    # print({'sites':data })
    return json.dumps(list(data))


def searchSite(url, list):

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }

    params = {"hl": "en", 'gl': 'in' }
    cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
    
    # Sending HTTP request
    req = requests.get(url, headers=headers, params=params, cookies=cookies)

    # Pulling HTTP data from internet
    sor = BeautifulSoup(req.text, "html.parser")

    data = sor.findAll('h3')

    for item in data:

        try:
            url = item.parent['href'].split('https')[1]

        except:
            url = None

        if url:
            tsd, td, tsu = extract("https"+url)

            list.add(td)