import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from lxml import etree

app = Flask(__name__)

@app.route("/")
def hello_world():
    print(os.getcwd() + '\\templates\\index.html')
    return render_template('index.html', name="dean soffer")


# perform extraction of the data by user choice of type
def extract_data(select_type, selector, soup):
    data = []

    if select_type == 'Tags':
        data.append(soup.find_all(selector))

    elif select_type == 'CSS':
        data.append(soup.select(selector))

    elif select_type == 'xPath':
        tree = etree.HTML(str(soup))
        element = tree.xpath(selector)
        if len(element) > 0:
            data.append(element)

    elif select_type == 'Tag id':
        data.append(soup.find(id=selector))

    return data

@app.route("/start-crawl", methods=['POST'])
def start_crawl():
    results = {}
    url = request.form['url']
    symbols = request.form['info']
    select_type = request.form['dataType']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # for tag_selector in symbols.splitlines():
    #     results[tag_selector] = []

    for tag_selector in symbols.splitlines():
        results[tag_selector] = extract_data(select_type, tag_selector, soup)[0]



    return render_template('results.html', name="crawling!!", url=url, results=results)

if __name__ == '__main__':
    app.run(debug=True)