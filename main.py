from flask import Flask, render_template
from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()

app = Flask(__name__)

staticbucketurl = 'https://storage.googleapis.com/sarsooxyzstatic/'

@app.route('/')
def main():
    return render_template('index.html', staticroot = staticbucketurl)

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/art')
def art():
    art_collection = db.collection(u'art')
    #art_tags_collection = db.collection(u'art_tags')    
    
    try:
        pics = art_collection.get()
        #tags = art_tags_collection.get()
    except google.cloud.exceptions.NotFound:
        return 'no such document'

    #categories = []
    #for tag in tags:
        #taglist = {
            #tag.to_dict()['name'] : []
        #}
        #print(tag.to_dict())
        #categories.append(taglist)
    
    #print(categories)

    images = []
    for doc in pics:
        #image = doc.to_dict()
        images.append(doc.to_dict())
        #categories[categories.index(image['tag'])].append(image)

    return render_template('art.html', staticroot = staticbucketurl, images=images)

@app.route('/dev')
def dev():
    return render_template('dev.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
