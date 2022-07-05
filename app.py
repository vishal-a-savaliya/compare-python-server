from flask import *
# import requests, json
from bs4 import BeautifulSoup
from googleproduct import getProducts
from sites import getSite

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to compare API"

@app.route('/search/<query>')
def search(query):
    return str(getProducts(query))

@app.route('/sites/<query>')
def sites(query):
    return getSite(query)

if __name__ == '__main__':
    app.run(port=8000)
