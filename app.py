import flask

app = flask.Flask(__name__)

@app.route('/')
# devolver 'hola' en json
def index():
    return flask.jsonify({'message': 'Hello World! My name is Aaron!!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')