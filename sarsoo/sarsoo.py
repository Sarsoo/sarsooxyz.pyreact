from flask import Flask, render_template
from google.cloud import firestore
import os

from .art import art_print
from .music import music_print

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'), template_folder="templates")

app.register_blueprint(art_print, url_prefix='/art')
app.register_blueprint(music_print, url_prefix='/music')

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'


@app.route('/')
def main():
    
    index_doc = db.collection(u'pages').document(u'index')
    doc = index_doc.get()
    index_dict = doc.to_dict()
    
    splashtext = index_dict['splash_text']

    art = []
    for image in index_dict['art']:
        art.append(image.get().to_dict())

    print(index_dict['art'][0].get().to_dict())

    return render_template('index.html', staticroot = staticbucketurl, splash = splashtext, art=art)


@app.route('/dev')
def dev():
    return render_template('dev.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
