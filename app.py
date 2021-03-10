from flask import Flask, render_template, redirect, session, flash, request
from secrets import API_KEY
from models import db, connect_db
import requests
from bs4 import BeautifulSoup
from flask_login import LoginManager

API_BASE_URL = "https://api.genius.com/search"
headers = {"Authorization": f"Bearer {API_KEY}"}

# login_manager = LoginManager()
# login_manager.init_app(app)

app = Flask(__name__)

@app.route('/')
def show_landing_page():
    """Show landing page of site."""

    return render_template("home-anon.html")

@app.route('/search')
def get_lyrics_info():
    """Gets artist info of the lyrics to display."""

    search = request.args["search"]
    params = {"q": search}
    res = requests.get(API_BASE_URL, headers=headers, params=params)

    data = res.json()
    results = data["response"]["hits"]
    # for result in data["response"]["hits"]:
    #     print(result["result"]["full_title"])
    #     print(result["result"]["header_image_thumbnail_url"])
        
    return render_template("results.html", results=results)

@app.route('/register')
def show_register_page():
    """Shows page for registration."""

    return render_template("register.html")

@app.route('/login')
def show_login_page():
    """Shows page for registration."""

    return render_template("login.html")
    



# @app.route('/redirect')
# def redirect_page():

#     return '<h1>Redirect</h1>'

# URL = 'https://genius.com/Citizen-blue-sunday-lyrics'
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, 'html.parser')
# results = soup.find('div', class_='lyrics')
# print(results.prettify())


