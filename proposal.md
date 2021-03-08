## Capstone 1 Project Proposal: Lyrically

1. The goal of my website will be designed as a place for a user to find lyrics from songs that they want to know and be able to have a place to store and save them. Also being a place for lyric/music fans to save their favorite lyrics.

2. The demographic of the users will be music fans, lyric fans, and lyricists. 

3. I plan on using the musicxmatch API.. Data I would like to obtain is lyrics of a song, the name of the song/artist/album, and also the album artwork for the given album. Would possibly use the Spotify/Apple Music/YouTube API to provide links to audio of the song being searched as well.

4. a.  ![Lyrically Shecma](https://github.com/rylandinthesun/Lyrically/blob/main/lyrically_schema.png)

   b.  Issues I might run into with the Genius API is with the AOuth for authentication. I will have to look more into that before I decide if I want to use it since it seems like if I am wanting to use the API, then users will technically be logged in to my account with the token that was provided. I’ll have to do more research into that.
   
   c.  Sensitive information I’d need to secure is that password for the login to the site and possibly my own token login for the Genius API.
   
   d.  Functionality of the app will include:
      
      *  Register/Login
      *  Users will be able to search lyrics or artist and/or song name to find either the song they are looking for or the lyrics they are looking for.
      *  Users will have a profile page where they can add/save or remove lyrics to. They will also be able to  favorite/unfavorite lyrics as well.
      *  Users will be able to edit their basic info and delete their profile.
      *  Ideally I would like the search form to save recent searches to display as well.

   e.  User flow:
      
      *  Landing page where you are prompted to Register/Create an account or Login.
      *  After Registration/Login the user is brought to a Search page/form where you are able to provide lyrics of a song to find the song you might be looking for. Or you can click to view another form where you can search the song title and/or artist of the song you already know and want the lyrics for.
      *  Once that info is provided by the user, the search will find that data in the API while the user will be sent to the result page where it will provide result(s) of the song/lyrics they are looking for. If there aren't any results availabe they will be shown a no result page and can chose to go back to the search form/page.
      *  While viewing the lyrics they will be able to favorite or unfavorite them and also have the option of saving the lyrics to their user profile page. 
      *  A favorite will add them to a top portion of the profile and the "added/saved" section will be on the lower part of the user profile. I will most likely have these displayed as a clickable element which includes the artist, track name, and album image that when clicked while direct you to the page that displays the lyrics for that song.

   f. I think that the search aspect could have features that make this app more than CRUD.



