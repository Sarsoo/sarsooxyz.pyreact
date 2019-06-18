from flask import Blueprint, jsonify, abort
from sarsoo.art import db
from sarsoo.art.art import get_asset_url

art_api_print = Blueprint('artapi', __name__)


@art_api_print.route('/', methods=['GET'])
def get_all_collections():

    tagdicts = db.pull_all_tags()

    art_collections = []

    for tag_dict in tagdicts:
        art_collections.append({
            'name': tag_dict['name'],
            'id': tag_dict['doc_name'],
            'description': tag_dict['description'],
            'index': tag_dict['index'],
            'splash_url': get_asset_url(tag_dict['splash']['file_name'])
        })

    response = {'collections': art_collections}

    return jsonify(response)


@art_api_print.route('/<id>', methods=['GET'])
def get_named_collection(art_id):

    try:
        tagdict = db.pull_named_tag(art_id)
    except TypeError as e:
        abort(404)

    artlist = []

    for image in tagdict['images']:
        artlist.append({
            'file_url': get_asset_url(image['file_name']),
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
