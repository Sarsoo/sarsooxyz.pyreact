from google.cloud import firestore
from google.cloud import exceptions

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'

fs = firestore.Client()


def pull_all_tags():

    art_tags_collection = fs.collection(u'art_tags')

    try:
        tags = art_tags_collection.get()
    except exceptions.NotFound:
        return 'no such document'

    dicts = list(map(lambda x: x.to_dict(), tags))

    for artdict in dicts:
        artdict['splash'] = artdict['splash'].get().to_dict()

    return sorted(dicts, key=lambda k: k['index'])


def pull_named_tag(name):
    
    name_doc = fs.document(u'art_tags/{}'.format(name))

    tag_dicts = name_doc.get().to_dict()

    image_list = []
    for image in tag_dicts['art']:
        image_list.append(image.get().to_dict())
    
    tag_dicts['images'] = sorted(image_list, key=lambda k: k['date'], reverse=True)
       
    return tag_dicts


def get_populated_tags():
    
    tag_dicts = pull_all_tags()

    for tag in tag_dicts:    
        image_list = []
        for image in tag['art']:
            image_list.append(image.get().to_dict())
            tag['images'] = image_list
       
    return tag_dicts
