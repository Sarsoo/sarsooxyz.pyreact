from flask import Flask, render_template
from google.cloud import firestore
import os

from .art import art_print
from .music import music_print
from .api import art_api_print
from .api import dev_api_print

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'build'), template_folder="templates")

app.register_blueprint(art_print, url_prefix='/art')
app.register_blueprint(music_print, url_prefix='/music')
app.register_blueprint(art_api_print, url_prefix='/api/art')
app.register_blueprint(dev_api_print, url_prefix='/api/dev')

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'


@app.route('/')
def main():
    
    index_query = db.collection(u'pages').document(u'index')
    index_dict = index_query.get().to_dict()
    
    main_text = index_dict['main_text']

    art = []
    for image in index_dict['art']:
        art.append(image.get().to_dict())

    return render_template('index.html', staticroot=staticbucketurl, art=art, main_text=main_text)


@app.route('/dev')
def dev():
    return render_template('dev.html')

# [END gae_python37_app]
