from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
import requests

from google.cloud import firestore

fs = firestore.Client()

urlprefix = 'music'
fm_url = 'https://ws.audioscrobbler.com/2.0/'

music_print = Blueprint('music', __name__, template_folder='templates')


@music_print.route('/')
def root():
    fmkey = fs.document('key/fm').get().to_dict()['clientid']
    
    params = {
            'method':'user.gettopalbums',
            'user':'sarsoo',
            'period':'1month',
            'limit':'6',
            'api_key':fmkey,
            'format':'json'
            }

    req = requests.get(fm_url, params = params)

    albums = req.json()['topalbums']['album']
    
    for album in albums:
        for image in album['image']:
            image['text'] = image['#text']

    return render_template('music/index.html', albums = albums)
