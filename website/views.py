from flask import Blueprint, render_template, request, url_for, redirect
import requests, re, json, os, time
from bs4 import BeautifulSoup

views = Blueprint('views', __name__)

@views.route('/')
def home():
    data = get_newest()
    movies = get_movies_by_category()
    return render_template('home.html', data = data)

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
                imdb_ids = fetch_imdb_id()
                if data[0] in imdb_ids:
                    print('LOG: Movie "' + data[1] + '" is already added')
                else:
                    poster_path = save_movie_poster(data[0], data[5], data[1])
                    trailer_path = save_movie_trailer(data[0], data[7], data[1])
                    json_object = data_to_json_object(data, poster_path, trailer_path, url)
                    put_movie_data_into_db(json_object)
                    put_categories_data_into_db(data[6])
            else:
                print('LOG: Invalid IMDB movie url')
            return redirect(url_for('views.add_movie'))
    return render_template('settings.html')

def get_newest():
    movies = requests.get('http://localhost:3000/movies_collection?_sort=year,id&_order=desc,desc')
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
    db_filename = '../static/posters/' + imdb_id + '.jpg'
    if poster.ok:
        print('LOG: save_movie_poster() response: ' + "% s" % poster.status_code)
        with open(filename, 'wb') as f:
            for chunk in poster.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        while not os.path.exists(filename):
            time.sleep(1)
        print('LOG: save_movie_poster() successfully saved poster for movie: ' + title)
        return db_filename
    else:
        print('LOG: save_movie_poster() response: ' + "% s" % poster.status_code)

def save_movie_trailer(imdb_id, url, title):
    trailer = requests.get(url, stream=True)
    filename = 'website/static/trailers/' + imdb_id + '.mp4'
    db_filename = '../static/trailers/' + imdb_id + '.mp4'
    if trailer.ok:
        print('LOG: save_movie_trailer() response: ' + "% s" % trailer.status_code)
        with open(filename, 'wb') as f:
            for chunk in trailer.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        while not os.path.exists(filename):
            time.sleep(1)
        print('LOG: save_movie_poster() successfully saved trailer for movie: ' + title)
        return db_filename
    else:
        print('LOG: save_movie_trailer() response: ' + "% s" % trailer.status_code)

def data_to_json_object(data, poster, trailer, url):
    json_object = {
        "imdb_id": data[0],
        "title": data[1],
        "year": data[2],
        "length": data[3],
        "rating": data[4],
        "poster_path": poster,
        "categories": data[6],
        "imdb_url": url,
        "trailer_path": trailer,
        "description": data[8]
    }
    return json_object

def put_movie_data_into_db(json_object):
    movie = requests.post('http://localhost:3000/movies_collection', json = json_object)
    if movie.ok:
        print('LOG: put_movie_data_into_db() response: ' + "% s" % movie.status_code)
    else:
        print('LOG: put_movie_data_into_db() response: ' + "% s" % movie.status_code)

def fetch_imdb_id():
    imdb_id_length = len(json.loads(requests.get('http://localhost:3000/movies_collection').content))
    imdb_ids = []
    for i in range(1, imdb_id_length + 1):
        imdb_id_response = requests.get('http://localhost:3000/movies_collection/' + str(i))
        if imdb_id_response.ok:
            print('LOG: fetch_imdb_id() response: ' + "% s" % imdb_id_response.status_code)
            imdb_id_json = json.loads(imdb_id_response.content)
            imdb_ids.append(imdb_id_json['imdb_id'])
        else:
            print('LOG: fetch_imdb_id() response: ' + "% s" % imdb_id_response.status_code)
    return imdb_ids

def get_movie_from_imdb(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'}
    imdb = requests.get(url, headers = headers)
    if imdb.ok:
        print('LOG: get_movie_from_imdb() response: ' + "% s" % imdb.status_code)
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

def fetch_categories():
    categories_length = len(json.loads(requests.get('http://localhost:3000/categories_collection').content))
    categories = []
    for i in range(1, categories_length + 1):
        categories_response = requests.get('http://localhost:3000/categories_collection/' + str(i))
        if categories_response.ok:
            print('LOG: fetch_categories() response: ' + "% s" % categories_response.status_code)
            categories_json = json.loads(categories_response.content)
            categories.append(categories_json['category_name'])
        else:
            print('LOG: fetch_categories() response: ' + "% s" % categories_response.status_code)
    return categories

def put_categories_data_into_db(categories_array):
    fetched_categories = fetch_categories()
    for category in categories_array:
        if category in fetched_categories:
            print('LOG: Could not add category: ' + category +  ' already exists')
        else:
            json_object = {
                "category_name": category
            }
            categories = requests.post('http://localhost:3000/categories_collection', json = json_object)
            if categories.ok:
                print('LOG: Added category: ' + category +  ' to DB')
                print('LOG: put_categories_data_into_db() response: ' + "% s" % categories.status_code)
            else:
                print('LOG: put_categories_data_into_db() response: ' + "% s" % categories.status_code)

def fetch_movies():
    movies = json.loads(requests.get('http://localhost:3000/movies_collection').content)
    return movies

def get_movies_by_category():
    json_object = []
    categories = fetch_categories()
    movies = fetch_movies()
    for category in categories:
        json = {
            category : [
            
            ]
        }
        for movie in movies:
            if category in movie['categories']:
                json[category].append(movie)
        json_object.append(json)
    return json_object


# categories_length = len(json.loads(requests.get('http://localhost:3000/categories_collection').content))
#     categories = []
#     for i in range(1, categories_length + 1):
#         categories_response = requests.get('http://localhost:3000/categories_collection/' + str(i))
#         if categories_response.ok:
#             print('LOG: fetch_categories() response: ' + "% s" % categories_response.status_code)
#             categories_json = json.loads(categories_response.content)
#             categories.append(categories_json['category_name'])
#         else:
#             print('LOG: fetch_categories() response: ' + "% s" % categories_response.status_code)