from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from google.cloud import firestore

fs = firestore.Client()

urlprefix = 'music'

music_print = Blueprint('music', __name__, template_folder='templates')


@music_print.route('/')
def root():
    fmkey = fs.document('key/fm').get().to_dict()['clientid']
    
    
    return render_template('music/index.html')
