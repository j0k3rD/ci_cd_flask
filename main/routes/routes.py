from flask import jsonify, Blueprint

app = Blueprint('app', __name__, url_prefix='/')


@app.route('/')
def index():
    return jsonify({'message': 'Hello World! Parcial'})