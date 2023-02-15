from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup
import json

views = Blueprint('views', __name__)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'}

@views.route('/')
def home():
    header = getNewest()
    # data = getFromImdb(header['id'])
    return render_template('home.html', header = header)

def getNewest():
    movies = requests.get('http://localhost:3000/movies?_sort=year,id&_order=desc,desc')
    data = movies.json()[0]
    return data


# getting ready for adding a film to db, downloading trailer and poster
# make it without needing id, send in just imdb url, and the program will care about all
# prepare for connecting to bombuj, europix or something else, also prepare for the torrent solution
# def getFromImdb(id):
#     movies = requests.get('http://localhost:3000/movies/' + str(id))
#     url = movies.json()['imdb-url']
#     imdb = requests.get(url, headers = headers)
#     soup = BeautifulSoup(imdb.text, "html.parser")
#     script = soup.find(id = '__NEXT_DATA__')
#     data = json.loads(script.get_text())
#     title = data['props']['pageProps']['aboveTheFoldData']['originalTitleText']['text']
#     year = data['props']['pageProps']['aboveTheFoldData']['releaseYear']['year']
#     length = data['props']['pageProps']['aboveTheFoldData']['runtime']['displayableProperty']['value']['plainText']
#     rating = data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']
#     poster = data['props']['pageProps']['aboveTheFoldData']['primaryImage']['url']
#     categories = []
#     for category in data['props']['pageProps']['aboveTheFoldData']['genres']['genres']:
#         categories.append(category['text'])
#     trailer = data['props']['pageProps']['aboveTheFoldData']['primaryVideos']['edges'][0]['node']['playbackURLs'][0]['url']
#     description = data['props']['pageProps']['aboveTheFoldData']['plot']['plotText']['plainText']
#     return [ title, year, length, rating, poster, categories, trailer, description ]