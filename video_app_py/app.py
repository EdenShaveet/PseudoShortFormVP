from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    videos = [ #for embedding video URLs from online sources (most likely YouTube shorts)
        "<URl>", 
        "<URL>",
        "<URL>"
    ]
    return render_template('index.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)