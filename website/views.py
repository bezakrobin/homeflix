from flask import Blueprint, render_template, request, url_for, redirect
import requests, re, json, os, time
from bs4 import BeautifulSoup

views = Blueprint('views', __name__)

@views.route('/')
def home():
    header = get_newest()
    return render_template('home.html', header = header)

@views.route('/settings', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        url = request.form['imdb-url']
        if not url:
            print('LOG: No url given at: Add movie form')
        else:
            if is_imdb_url(url):
                print('LOG: Valid IMDB movie url')
                data = get_movie_from_imdb(url)
                save_movie_poster(data[0], data[5], data[1])
                save_movie_trailer(data[0], data[7], data[1])
            else:
                print('LOG: Invalid IMDB movie url')
            return redirect(url_for('views.add_movie'))
    return render_template('settings.html')

def get_newest():
    movies = requests.get('http://localhost:3000/movies?_sort=year,id&_order=desc,desc')
    if movies.ok:
        print('LOG: get_newest() response: ' + "% s" % movies.status_code)
        data = movies.json()[0]
        return data
    else:
        print('LOG: get_newest() response: ' + "% s" % movies.status_code)

def is_imdb_url(url):
    pattern = r'^https?://(www\.)?imdb\.com/title/tt\d+/$'
    return bool(re.match(pattern, url))

def save_movie_poster(imdb_id, url, title):
    poster = requests.get(url, stream=True)
    filename = 'website/static/posters/' + imdb_id + '.jpg'
    if poster.ok:
        print('LOG: save_movie_poster() response: ' + "% s" % poster.status_code)
        with open(filename, 'wb') as f:
            for chunk in poster.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        while not os.path.exists(filename):
            time.sleep(1)
        print('LOG: save_movie_poster() successfully saved poster for movie: ' + title)
    else:
        print('LOG: save_movie_poster() response: ' + "% s" % poster.status_code)

def save_movie_trailer(imdb_id, url, title):
    trailer = requests.get(url, stream=True)
    filename = 'website/static/trailers/' + imdb_id + '.mp4'
    if trailer.ok:
        print('LOG: save_movie_trailer() response: ' + "% s" % trailer.status_code)
        with open(filename, 'wb') as f:
            for chunk in trailer.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        while not os.path.exists(filename):
            time.sleep(1)
        print('LOG: save_movie_poster() successfully saved trailer for movie: ' + title)
    else:
        print('LOG: save_movie_trailer() response: ' + "% s" % trailer.status_code)

def put_movie_data_into_db():
    pass


# getting ready for adding a film to db
# prepare for connecting to bombuj, europix or something else, also prepare for the torrent solution
def get_movie_from_imdb(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'}
    imdb = requests.get(url, headers = headers)
    if imdb.ok:
        print('LOG: get_movie_from_imdb() response: ' + "% s" % trailer.status_code)
        soup = BeautifulSoup(imdb.text, "html.parser")
        script = soup.find(id = '__NEXT_DATA__')
        data = json.loads(script.get_text())
        imdb_id = data['props']['pageProps']['aboveTheFoldData']['id']
        title = data['props']['pageProps']['aboveTheFoldData']['originalTitleText']['text']
        year = data['props']['pageProps']['aboveTheFoldData']['releaseYear']['year']
        length = data['props']['pageProps']['aboveTheFoldData']['runtime']['displayableProperty']['value']['plainText']
        rating = data['props']['pageProps']['aboveTheFoldData']['ratingsSummary']['aggregateRating']
        poster = data['props']['pageProps']['aboveTheFoldData']['primaryImage']['url']
        categories = []
        for category in data['props']['pageProps']['aboveTheFoldData']['genres']['genres']:
            categories.append(category['text'])
        trailer = data['props']['pageProps']['aboveTheFoldData']['primaryVideos']['edges'][0]['node']['playbackURLs'][0]['url']
        description = data['props']['pageProps']['aboveTheFoldData']['plot']['plotText']['plainText']
    else:
        print('LOG: get_movie_from_imdb() response: ' + "% s" % trailer.status_code)
    return [ imdb_id, title, year, length, rating, poster, categories, trailer, description ]