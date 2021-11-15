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
def extractData(soup, r = ''):
    data = []
    symbols = request.form['info']
    dataType = request.form['dataType']
    if(dataType == 'Tags'):
        for dat in symbols.splitlines():
            data.append(soup.find_all(dat))
    elif(dataType == 'CSS'):
        for dat in symbols.splitlines():
            data.append(soup.select(dat))
    elif(dataType=='xPath'):
        dom = etree.HTML(r)
        #print(dom.xpath(symbols))
        for dat in symbols.splitlines():
            print(dom.xpath(dat))
            data.append(dom.xpath(dat).text)
    elif(dataType=='Tag id'):
        for dat in symbols.splitlines(): data.append(soup.find(id=dat))

    return data

@app.route("/start-crawl", methods=['POST'])
def start_crawl():

    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    symbols = request.form['info']
    resultsToSend = extractData(soup,response.content)

    return render_template('results.html', name="crawling!!", url=url, results=resultsToSend)

if __name__ == '__main__':
    app.run(debug=True)