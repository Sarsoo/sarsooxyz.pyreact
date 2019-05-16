from google.cloud import firestore

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'

fs = firestore.Client()


def getTagDicts():

    art_tags_collection = fs.collection(u'art_tags')

    try:
        tags = art_tags_collection.get()
    except google.cloud.exceptions.NotFound:
        return 'no such document'

    dicts = list(map(lambda x: x.to_dict(), tags))

    for artdict in dicts:
        artdict['splash'] = artdict['splash'].get().to_dict()

    return sorted(dicts, key=lambda k: k['index'])


def getPopulatedTagDict(name):
    
    name_doc = fs.document(u'art_tags/{}'.format(name))

    tag_dicts = name_doc.get().to_dict()

    image_list = []
    for image in tag_dicts['art']:
        image_list.append(image.get().to_dict())
    
    tag_dicts['images'] = sorted(image_list, key = lambda k: k['date'], reverse = True)
       
    return tag_dicts


def getPopulatedTagDicts():
    
    tag_dicts = getTagDicts()

    for tag in tag_dicts:    
        image_list = []
        for image in tag['art']:
            image_list.append(image.get().to_dict())
            tag['images'] = image_list
       
    return tag_dicts
