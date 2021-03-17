import os

from flask import Flask, render_template, redirect, session, flash, request, g, abort
from sqlalchemy.exc import IntegrityError
from secrets import API_KEY
from models import db, connect_db, User, Lyric, Rating, Save
import requests
from bs4 import BeautifulSoup
from forms import AddUserForm, LoginForm, EditUserForm, RatingForm, UpdateRatingForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///lyrically'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "b4e770dbe0a5904fbb11f744"

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


@app.route('/search', methods=["GET"])
def get_lyrics_info():
    """Gets artist info of the lyrics to display."""

    search = request.args["q"]
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
            user = User.signup(email=form.email.data, password=form.password.data, username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, bio=form.bio.data)
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
    return redirect('/')


@app.route('/profile/<int:user_id>')
def show_user_profile(user_id):
    """Show profile of current logged in user."""

    if not g.user:
        flash("Access unauthorized.")
        return redirect("/login")

    user = User.query.get_or_404(user_id)
    

    return render_template('user_profile.html', user=user)


@app.route('/profile/edit', methods=["GET", "POST"])
def edit_profile():
    """Update profile of current logged in user."""

    if not g.user:
        flash("Access unauthorized.")
        return redirect(f"/profile/{g.user.id}")

    user=User.query.get_or_404(g.user.id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.bio = form.bio.data
        user.image_url = form.image_url.data
        db.session.commit()
        return redirect(f"/profile/{g.user.id}")
    else:
        return render_template("edit_user.html", user=user, form=form)


@app.route('/delete_confim')
def confirm_deletion():
    """Show page to confirm user wants to delete."""

    if not g.user:
        flash("Access unauthorized.")
        return redirect(f"/profile/{g.user.id}")

    return render_template("delete_confirm.html")



@app.route('/profile/delete', methods=["POST"])
def delete_user():
    """Delete user who is currently signed in."""
    
    if not g.user:
        flash("Access unauthorized.")
        return redirect(f"/profile/{g.user.id}")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/")
    

@app.route('/lyrics/<path>', methods=["GET", "POST"])
def show_lyrics(path):
    """Scrape and show lyrics on a single page."""

    lyrics = Lyric.query.filter(Lyric.path == path).all()

    if lyrics:

        return render_template("lyrics.html", lyrics=lyrics)

    else:

        URL = f"https://genius.com/{path}" 
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyric_results = soup.find('div', class_='lyrics')
        lyric = lyric_results.get_text()
        track_results = soup.find('h1', class_="header_with_cover_art-primary_info-title")
        track_name = track_results.get_text()
        artist_results = soup.find('a', class_="header_with_cover_art-primary_info-primary_artist")
        artist_name = artist_results.get_text()
        try:
            album_results = soup.find('span', class_="metadata_unit-info").find_next('span', class_="metadata_unit-info")
            album_name = album_results.get_text()
        except AttributeError:
            album_name = "Album Name Not Found."
        art_results = soup.find('div', {"class": "cover_art"}).findChildren('img')
        for image in art_results:
            img = image.get('src')
        album_image = img
        lyrics = Lyric(lyrics=lyric, track_name=track_name, artist_name=artist_name, album_name=album_name, album_image=album_image, path=path)

        db.session.add(lyrics)
        db.session.commit()

        lyrics = Lyric.query.filter(Lyric.path == path).all()

    return render_template("lyrics.html", lyrics=lyrics)


@app.route('/lyrics/add_save/<int:lyric_id>', methods=["POST"])
def save_lyrics(lyric_id):
    """Saves lyrics to save database."""

    lyric = Lyric.query.get_or_404(lyric_id)

    if not g.user:
        flash("Can only save lyrics if you're logged in.")
        return redirect(f"/lyrics/{lyric.path}")

    g.user.saves.append(lyric)
    db.session.commit()

    return redirect(request.referrer)


@app.route('/lyrics/remove_save/<int:lyric_id>', methods=["POST"])
def unsave_lyrics(lyric_id):
    """Saves lyrics to save database."""

    lyric = Lyric.query.get_or_404(lyric_id)

    if not g.user:
        flash("Access unauthorized.")
        return redirect(f"/lyrics/{lyric.path}")

    g.user.saves.remove(lyric)
    db.session.commit()

    return redirect(request.referrer)


@app.route('/rating/<int:lyric_id>', methods=["GET", "POST"])
def show_rating_page(lyric_id):
    """Show form for rating lyrics and add a rating."""

    lyric = Lyric.query.get_or_404(lyric_id)

    if not g.user:
        flash("Access unauthorized.")
        return redirect(f"/lyrics/{lyric.path}")

    form = RatingForm()

    if form.validate_on_submit():
        try:
            r = request.form["rating"]
            rating = Rating(user_id=g.user.id, lyric_id=lyric_id, rating=r)
            db.session.add(rating)
            db.session.commit()
            
            
        except IntegrityError:
            flash("You've already given this rating.")
            return render_template('rating.html', form=form)
        
        return redirect(f"/lyrics/{lyric.path}")
    

    return render_template("rating.html", lyric=lyric, form=form)

@app.route('/update_rating/<int:rating_id>', methods=["GET", "POST"])
def update_rating(rating_id):
    """Update current rating."""

    rating = Rating.query.get_or_404(rating_id)

    if not g.user:
        flash("Access unauthorized.")
        return redirect(f"/lyrics/{rating.lyric.path}")

    form = UpdateRatingForm(obj=rating)

    if form.validate_on_submit():
        rating.rating = form.rating.data
        db.session.commit()
        return redirect(f"/lyrics/{rating.lyric.path}")
    
    else:

        return render_template("update_rating.html", rating=rating, form=form)


@app.route('/saves/<int:user_id>/')
def show_saves(user_id):
    """Shows saved lyrics on page."""

    if not g.user:
        flash("Access unauthorized.")
        return redirect("/login")

    user = User.query.get_or_404(user_id)
    

    return render_template('user_saves.html', user=user)


@app.route('/delete_rating/<int:rating_id>')
def delete_rating(rating_id):

    """Deletes rating."""

    if not g.user:
        flash("Access unauthorized.")
        return redirect(f"/login")
   
    rating = Rating.query.get_or_404(rating_id)

    db.session.delete(rating)
    db.session.commit()

    return redirect(f"/profile/{g.user.id}")