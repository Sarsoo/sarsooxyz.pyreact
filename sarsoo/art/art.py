from flask import Blueprint, render_template

from .db import pull_all_tags, pull_named_tag, get_populated_tags

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'
urlprefix = 'art'

art_print = Blueprint('art', __name__, template_folder='templates')


@art_print.route('/')
def view_root():
    tags = pull_all_tags()
    return render_template('art/index.html', tags=tags, staticroot=staticbucketurl, urlprefix=urlprefix)


@art_print.route('/<tag>')
def view_named_tag(tag):
    tags = pull_named_tag(tag)
    return render_template('art/all.html', staticroot=staticbucketurl, tags=[tags])


@art_print.route('/all')
def view_all_tags():
    sections = get_populated_tags()
    return render_template('art/all.html', staticroot=staticbucketurl, tags=sections)


def get_asset_url(name):
    return staticbucketurl + 'art/' + name + '.jpg'
