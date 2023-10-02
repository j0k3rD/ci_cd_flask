import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.jsonify({'message': 'Hello World! Now Building...'})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')