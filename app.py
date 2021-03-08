from flask import Flask, render_template, redirect, session, flash
import requests

app = Flask(__name__)

@app.route('/')
def show_page():

    return '<h1>Hello World</h1>'

@app.route('/redirect')
def redirect_page():

    return '<h1>Redirect</h1>'

