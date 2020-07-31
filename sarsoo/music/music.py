from flask import Blueprint, render_template
from fmframework.net.network import Network
from google.cloud import firestore

fs = firestore.Client()

urlprefix = 'music'
fm_url = 'https://ws.audioscrobbler.com/2.0/'

music_print = Blueprint('music', __name__, template_folder='templates')


@music_print.route('/')
def root():
    fmkey = fs.document('config/music-tools').get().to_dict()['last_fm_client_id']
    fmnet = Network(username='sarsoo', api_key=fmkey)
    albums = fmnet.get_top_albums(Network.Range.MONTH, limit=6)

    return render_template('music/index.html', albums=albums)
