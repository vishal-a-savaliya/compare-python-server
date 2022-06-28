from flask import *
import requests, json
from bs4 import BeautifulSoup
from tldextract import extract


app = Flask(__name__)


def getProducts(query):

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

    params = {"q": "dji", "hl": "en", 'gl': 'in', 'tbm': 'shop'}

    response = requests.get(f"https://www.google.com/search?q={query}",
                            params=params,
                            headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    #
    #
    #  list with two dict() combined
    return soup
    
    shopping_data = []
    inline_results_dict = {}
    shopping_results_dict = {}

    for inline_result in soup.select('.sh-np__click-target'):

        inline_shopping_title = inline_result.select_one(
            '.sh-np__product-title').text
        inline_shopping_link = f"https://google.com{inline_result['href']}"
        inline_shopping_price = inline_result.select_one('b').text
        inline_shopping_source = inline_result.select_one(
            '.E5ocAb').text.strip()

        inline_results_dict.update({
            'inline_shopping_results': [{
                'title': inline_shopping_title,
                'link': inline_shopping_link,
                'price': inline_shopping_price,
                'source': inline_shopping_source,
            }]
        })

        shopping_data.append(dict(inline_results_dict))

    for shopping_result in soup.select('.sh-dgr__content'):

        title = shopping_result.select_one('.Lq5OHe.eaGTj h4').text
        product_link = f"https://www.google.com{shopping_result.select_one('.Lq5OHe.eaGTj')['href']}"
        source = shopping_result.select_one('.IuHnof').text
        price = shopping_result.select_one('span.kHxwFf span').text

        try:
            rating = shopping_result.select_one('.Rsc7Yb').text
        except:
            rating = None

        try:
            reviews = shopping_result.select_one(
                '.Rsc7Yb').next_sibling.next_sibling
        except:
            reviews = None

        try:
            delivery = shopping_result.select_one('.vEjMR').text
        except:
            delivery = None

        shopping_results_dict.update({
            'shopping_results': [{
                'title': title,
                'link': product_link,
                'source': source,
                'price': price,
                'rating': rating,
                'reviews': reviews,
                'delivery': delivery,
            }]
        })

        shopping_data.append(dict(shopping_results_dict))

#     return json.dumps(shopping_data, indent=2, ensure_ascii=False)
      


def getSite(search):

    # URL
    url = [f"https://www.google.com/search?&q={search}",
           f"https://www.google.com/search?&q={search}&start=10",
           f"https://www.google.com/search?&q={search}&start=20"
           ]

    data = set()

    for u in url:
        searchSite(u, data)

    # data = {'sites':data }

    # print({'sites':data })
    return json.dumps(list(data))


def searchSite(url, list):

    # Sending HTTP request
    req = requests.get(url)

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





@app.route("/")
def home():
    return "Welcome to compare API"

@app.route('/search/<query>')
def search(query):
    return str(getProducts(query))

@app.route('/sites/<query>')
def sites(query):
    return getSite(query)
    # return f"hiii this is {query}"

if __name__ == '__main__':
    app.run()
