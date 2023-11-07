from flask import Flask, render_template, request, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# YouTube Scraper
def scrape_youtube(query):
    youtube_results = []

    url = f'https://www.youtube.com/results?search_query={query}'
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')

    for item in soup.select('.yt-lockup-video'):
        title = item.select('.yt-lockup-title')[0].get_text()
        link = 'https://www.youtube.com' + item.select('a')[0]['href']
        youtube_results.append({'title': title, 'link': link})

    return youtube_results

# Amazon Scraper
def scrape_amazon(query):
    amazon_results = []

    url = f'https://www.amazon.com/s/?field-keywords={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for item in soup.select('.s-result-item'):
        title = item.select('h2 a span')[0].get_text()
        link = item.select('h2 a')[0]['href']
        amazon_results.append({'title': title, 'link': link})

    return amazon_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    if request.method == 'POST':
        query = request.form['query']
        youtube_data = scrape_youtube(query)
        return render_template('youtube.html', query=query, youtube_data=youtube_data)
    return render_template('youtube.html')

@app.route('/amazon', methods=['GET', 'POST'])
def amazon():
    if request.method == 'POST':
        query = request.form['query']
        amazon_data = scrape_amazon(query)  # Call the scraping function
        return render_template('amazon.html', query=query, amazon_data=amazon_data)
    return render_template('amazon.html')


if __name__ == '__main__':
    app.run(debug=True)
