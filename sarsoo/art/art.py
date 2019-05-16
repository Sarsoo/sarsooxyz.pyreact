from flask import Blueprint, render_template

from .db import getTagDicts, getPopulatedTagDict, getPopulatedTagDicts

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'
urlprefix = 'art'

art_print = Blueprint('art', __name__, template_folder='templates')


@art_print.route('/')
def root():
    tags = getTagDicts()
    #print(tags)
    return render_template('art/index.html', tags = tags, staticroot = staticbucketurl, urlprefix = urlprefix)


@art_print.route('/<tag>')
def tag_view(tag):
    tags = getPopulatedTagDict(tag)
    return render_template('art/all.html', staticroot = staticbucketurl, tags = [tags])


@art_print.route('/all')
def all():
    sections = getPopulatedTagDicts()
    return render_template('art/all.html', staticroot = staticbucketurl, tags=sections)
