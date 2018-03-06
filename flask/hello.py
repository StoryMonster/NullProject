from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", title="Hello, world")

@app.route('/sources/images/Desert.jpg')
def image_scaner():
    return render_template("image_scaner.html", title="Desert", image_path="Desert.jpg")

if __name__ == '__main__':
    app.run()
