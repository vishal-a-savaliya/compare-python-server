from logging import exception
import requests,json
from bs4 import BeautifulSoup
from tldextract import extract


def getSite(search):

    # URL
    url = [f"https://www.google.com/search?&q={search}",
        f"https://www.google.com/search?&q={search}&start=10",
        f"https://www.google.com/search?&q={search}&start=20"
        ]

    data = set()

    for u in url:
        searchSite(u,data)

    # data = {'sites':data }

    # print({'sites':data })
    return json.dumps(list(data))


def searchSite(url,list):

    # Sending HTTP request
    req = requests.get(url)

    # Pulling HTTP data from internet
    sor = BeautifulSoup(req.text, "html.parser")

   

    data = sor.findAll('h3')

    for item in data:

        try:
            url = item.parent['href'].split('https')[1]

        except:
            url=None

        if url:
            tsd, td, tsu = extract("https"+url)

            list.add(td)



# print(getSite('laptop'))