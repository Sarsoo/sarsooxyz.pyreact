from flask import Flask, render_template
from google.cloud import firestore
import os

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'), template_folder = "templates")

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'

@app.route('/')
def main():
    
    index_doc = db.collection(u'pages').document(u'index')
    doc = index_doc.get()
    index_dict = doc.to_dict()
    
    splashtext = index_dict['splash_text']

    art = []
    for image in index_dict['art']:
        art.append(image.get().to_dict())

    print(index_dict['art'][0].get().to_dict())

    return render_template('index.html', staticroot = staticbucketurl, splash = splashtext, art=art)

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/art')
def art():
    art_collection = db.collection(u'art')
    art_tags_collection = db.collection(u'art_tags')    

    try:
        tags = art_tags_collection.get()
    except google.cloud.exceptions.NotFound:
        return 'no such document'

    sections = []
    
    for tag in tags:
        tag_dict = tag.to_dict()
        query_ref = art_collection.where(u'tag', u'==', u'{}'.format(tag_dict['name']))
        query = query_ref.get()

        image_list = []
            
        for image in query:
            image_list.append(image.to_dict())

        #sections.append({tag_dict['name']: image_list})
        sections.append({'images': image_list, 'name': tag_dict['name'], 'description': tag_dict['description'], 'index': tag_dict['index']})

    return render_template('art.html', staticroot = staticbucketurl, tags=sections)

@app.route('/dev')
def dev():
    return render_template('dev.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
