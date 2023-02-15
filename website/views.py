from flask import Blueprint, render_template
import requests

views = Blueprint('views', __name__)

@views.route('/')
def home():
    data = getNewest()
    return render_template('home.html', header = data)

def getNewest():
    movies = requests.get('http://localhost:3000/movies?_sort=year,id&_order=desc,desc')
    data = movies.json()[0]
    return data