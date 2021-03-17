# Lyrically
[Lyrically.](https://lyrically-by-ryland.herokuapp.com/) A web app for finding, saving, and rating lyrics.

Lyrically is designed to give lyric fans and lyricicsts more of a social aspect to when it comes to searching for lyrics they are looking for. It's simple design makes it helpful for users wanting to save lyrics to easily access. While also being able to rate lyrics that they love or ...hate.

User flow starts with the home page where you presented with a logo and a search form. Non registered users are able to search for lyrics by song name, artist name, or any of the lyrics from a song that they know. They are given 10 results back from their search. If a user signs up they are given access to saving lyrics and rating lyrics which a page dedicated for all the saves and lyrics they've rated displayed on their profile page.

API being used is [Genius API](doc.genius.com). I did wish this API included the actual lyrics instead of a "path" for the genius.com site for the lyrics. This made it where I had to scrape the lyrics from the path to access the lyrics data/text.

Tech used: Python, Flask, SQL-Alchemy, Flask-SQLAlchemy, WTForms, BeautifulSoup, Flask-Bcrypt and Tailwind.
