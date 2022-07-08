import requests
import re
import json
from bs4 import BeautifulSoup


def getProducts(query):

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36"
    }

    params = {"hl": "en", 'gl': 'in', 'tbm': 'shop'}
    cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}

    response = requests.get(f"https://www.google.com/search?hl=en-IN&gl=IN&ceid=IN:en&q={query}",
                            params=params,
                            headers=headers,
                            cookies=cookies)

    soup = BeautifulSoup(response.text, 'html.parser')
#     return soup

    shopping_data = []
    inline_results_dict = {}
    shopping_results_dict = {}
    # images = {}

    for inline_result in soup.select('.sh-np__click-target'):

        inline_shopping_title = inline_result.select_one(
            '.sh-np__product-title').text
        inline_shopping_link = f"https://google.com{inline_result['href']}"
        inline_shopping_image = inline_result.div.img['src']
        inline_shopping_price = inline_result.select_one('b').text
        inline_shopping_price = inline_shopping_price.split(' ')[0]
        inline_shopping_price = inline_shopping_price.split('\xa0')[0]
        inline_shopping_source = inline_result.select_one(
            '.E5ocAb').text.strip()

        inline_results_dict.update({

            'title': inline_shopping_title,
            'image': inline_shopping_image,
            'link': inline_shopping_link,
            'price': inline_shopping_price,
            'source': inline_shopping_source,
            'rating': None,
            'reviews': None,
            'delivery': None,

        })

        shopping_data.append(dict(inline_results_dict))

    for shopping_result in soup.select('.sh-dgr__content'):

        title = shopping_result.select_one('.Lq5OHe.eaGTj h4').text
        image = shopping_result.select_one('.ArOc1c img')['src']
        product_link = f"https://www.google.com{shopping_result.select_one('.Lq5OHe.eaGTj')['href']}"
        source = shopping_result.select_one('.IuHnof').text
        price = shopping_result.select_one('span.kHxwFf span').text

        price =price.split(' ')[0]
        price =price.split('\xa0')[0]

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

            'title': title,
            'image': image,
            'link': product_link,
            'price': price,
            'source': source,
            'rating': rating,
            'reviews': reviews,
            'delivery': delivery,

        })

        shopping_data.append(dict(shopping_results_dict))

    shopping_data.sort(key=lambda x: x["price"])

    return json.dumps(shopping_data, indent=2, ensure_ascii=False)


# print(getProducts('colgate'))
