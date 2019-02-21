from google.cloud import firestore

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'

fs = firestore.Client()

def getTagDicts():

    art_tags_collection = fs.collection(u'art_tags')

    try:
        tags = art_tags_collection.get()
    except google.cloud.exceptions.NotFound:
        return 'no such document'

    dicts = []
    for tag in tags:
        dicts.append(tag.to_dict())

    return dicts

def getPopulatedTagDict(name):
    
    name_doc = fs.document(u'art_tags/{}'.format(name))

    tag_dicts = name_doc.get().to_dict()

    image_list = []
    for image in tag_dicts['art']:
        image_list.append(image.get().to_dict())
        tag_dicts['images'] = image_list
       
    return tag_dicts

def getPopulatedTagDicts():
    
    tag_dicts = getTagDicts()

    for tag in tag_dicts:    
        image_list = []
        for image in tag['art']:
            image_list.append(image.get().to_dict())
            tag['images'] = image_list
       
    return tag_dicts
