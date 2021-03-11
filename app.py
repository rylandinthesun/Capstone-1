import os

from flask import Flask, render_template, redirect, session, flash, request, g, abort
from sqlalchemy.exc import IntegrityError
from secrets import API_KEY
from models import db, connect_db, User, Lyric, Like, Save
import requests
from bs4 import BeautifulSoup
from forms import AddUserForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///lyrically'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

API_BASE_URL = "https://api.genius.com/search"
headers = {"Authorization": f"Bearer {API_KEY}"}

CURR_USER = "curr_user"

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])

    else:
        g.user = None
    print(g.user)


def do_login(user):
    """Log in user."""

    session[CURR_USER] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER in session:
        del session[CURR_USER]


@app.route('/')
def show_landing_page():
    """Show landing page of site."""

    return render_template("home.html")


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


@app.route('/register', methods=["GET", "POST"])
def signup():
    """Show page for registeration and validate user to sign up."""

    form = AddUserForm()

    if form.validate_on_submit():
        try:
            user = User.signup(email=form.email.data, password=form.password.data, username=form.username.data)
            db.session.commit()
        
        except IntegrityError:
            flash("Username already taken")
            return render_template('register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('register.html', form=form)
            
            
            
@app.route('/login', methods=["GET", "POST"])
def login():
    """Show page for login and validate user to login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.email.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Welcome back {user.username}")
            return redirect("/")
        
        flash("Invalid email or password.")

    return render_template("login.html", form=form)



@app.route('/logout')
def logout():
    """Logs user out and redirects to homepage."""

    session.pop(CURR_USER)
    flash("Goodbye!")
    return redirect('/login')





@app.route('/profile/<int:user_id>')
def show_user_profile(user_id):
    """Show profile of current logged in user."""

    if "curr_user" not in session:
        flash("Please login first!")
        redirect('/login')

    user = User.query.get_or_404(user_id)

    return render_template('user_profile.html', user=user)
    
@app.route('/lyrics/<path>')
def show_lyrics(path):
    """Scrape and show lyrics on a single page."""

    URL = f"https://genius.com/{path}"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('div', class_='lyrics')
    lyrics = results.get_text()
    
    return render_template("lyrics.html", lyrics=lyrics)
