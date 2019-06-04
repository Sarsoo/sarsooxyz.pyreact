from flask import Blueprint, jsonify, abort
from sarsoo.art import db
from sarsoo.art.art import getAssetUrl

art_api_print = Blueprint('artapi', __name__)


@art_api_print.route('/', methods=['GET'])
def collections():

    tagdicts = db.getTagDicts()

    collections = []

    for dict in tagdicts:
        collections.append({
            'name': dict['name'],
            'id': dict['doc_name'],
            'description': dict['description'],
            'index': dict['index'],
            'splash_url': getAssetUrl(dict['splash']['file_name'])
        })

    response = {'collections': collections}

    return jsonify(response)


@art_api_print.route('/<id>', methods=['GET'])
def getcollection(id):

    try:
        tagdict = db.getPopulatedTagDict(id)
    except TypeError as e:
        abort(404)

    artlist = []

    for image in tagdict['images']:
        artlist.append({
            'file_url': getAssetUrl(image['file_name']),
            'date': image['date'].strftime('%d %B %y')
        })

    response = {'name': tagdict['name'],
                'description': tagdict['description'],
                'art': artlist}

    return jsonify(response)


@art_api_print.errorhandler(404)
def error400(error):

    errorresponse = {'error': 'collection not found'}

    return jsonify(errorresponse), 404
