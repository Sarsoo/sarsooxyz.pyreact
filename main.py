from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/art')
def art():
    return render_template('art.html')

@app.route('/dev')
def dev():
    return render_template('dev.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
