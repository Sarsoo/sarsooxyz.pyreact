from flask import Blueprint, jsonify, abort
from google.cloud import firestore, exceptions

fs = firestore.Client()

dev_api_print = Blueprint('devapi', __name__)


@dev_api_print.route('/', methods=['GET'])
def collections():

    dev_collection = fs.collection(u'dev')

    try:
        tags = dev_collection.get()
    except exceptions.NotFound:
        abort(404)

    dicts = list(map(lambda x: x.to_dict(), tags))

    dev_documents = []

    for dev_dict in dicts:
        dev_documents.append({
            'name': dev_dict['name'],
            'description': [i for i in dev_dict['description']],
            'url': dev_dict['url'],
            'index': dev_dict['index']
        })

    response = {'dev': sorted(dev_documents, key=lambda k: k['index'])}

    return jsonify(response)


@dev_api_print.errorhandler(404)
def error400(error):

    errorresponse = {'error': 'collection not found'}

    return jsonify(errorresponse), 404
