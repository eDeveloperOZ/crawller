import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    print(os.getcwd() + '\\templates\\index.html')
    return render_template('index.html', name="dean soffer")


@app.route("/start-crawl", methods=['POST'])
def start_crawl():

    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    symbols = request.form['tags']
    resultsToSend = []
    for tag in symbols.splitlines():
        resultsToSend.append(soup.find_all(tag))

    return render_template('results.html', name="crawling!!", url=url, results=resultsToSend)

if __name__ == '__main__':
    app.run(debug=True)