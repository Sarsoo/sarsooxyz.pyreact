from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

from google.cloud import firestore

urlprefix = 'music'

music_print = Blueprint('music', __name__, template_folder='templates')


@music_print.route('/')
def root():
    return render_template('music/index.html')
