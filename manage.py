from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World! 6666'


if __name__ == '__main__':
    app.run(debug=True)
