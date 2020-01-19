from flask import Blueprint, jsonify, abort
from google.cloud import firestore, exceptions

fs = firestore.Client()

eng_api_print = Blueprint('engapi', __name__)


@eng_api_print.route('/', methods=['GET'])
def get_all_collections():

    eng_collection = fs.collection(u'eng')

    try:
        tags = eng_collection.get()
        response = {'eng': sorted([i.to_dict() for i in tags], key=lambda k: k['index'])}
        return jsonify(response)

    except exceptions.NotFound:
        abort(404)


@eng_api_print.errorhandler(404)
def error400(error):
    errorresponse = {'error': 'collection not found'}
    return jsonify(errorresponse), 404
