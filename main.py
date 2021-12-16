import os
import sys

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from lxml import etree
from urlextract import URLExtract

app = Flask(__name__)
serverId = 0
@app.route("/")
def hello_world():
    print(os.getcwd() + '\\templates\\index.html')
    return render_template('index.html', serverId=serverPort)


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

def extract_urls(domain_name, soup):
    extractor = URLExtract()
    data = []
    #gets all lines thats cmtains the domain to look for
    for link in str(soup).splitlines():
        if domain_name in link:
            #check if the origin url exsits in list ebfore appending any further links to avoid recursive infinite scraping
            if extractor.find_urls(link)[0] == domain_name:
                print("same name as origin url")
            else:
                data.append(extractor.find_urls(link))
            # print('-------------------------')
    #data holds a list off all links that require additional serach-work
    #data is to be sent to mngr for further distribution of work load
    for itm in data:
        print(itm)

@app.route("/start-crawl", methods=['POST'])
def start_crawl():
    results = {}
    url = request.form['url']
    symbols = request.form['info']
    select_type = request.form['dataType']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    extract_urls(url, soup)

    for tag_selector in symbols.splitlines():
        results[tag_selector] = extract_data(select_type, tag_selector, soup)[0]
    serverId =  args = sys.argv[1:]
    return render_template('results.html', name="crawling!!", url=url, results=results, serverId=serverPort)

if __name__ == '__main__':
    args = sys.argv[1:]
    serverPort = args[0]
    print(serverPort)
    app.run(debug=True, port=serverPort)