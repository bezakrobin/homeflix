from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    trailer = 'avatar.mp4'
    poster = 'avatar.jpg'
    return render_template('home.html', trailer = trailer, poster = poster)