#!/usr/bin/python3
"""
Flask app that intergrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flassger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Global Flask app variable: app
app = Flask(__name__)
swagger = Swagger(app)

#global strict slashes
app.url_map.strict_slashes = False

#flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

#Cross-Origin Resource Sharing
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

#app_views BluePrint defined in api.vi.views
app.register_blueprint(app_views)

#begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    After each request, this method calls .close() (i.e .remove()) or the current SQLAlchemy session
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """Handles 404 errors"""
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(400)
def handle_400(exception):
    """handles 400 errors"""
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)

@app.errorhandler(Exception)
def global_error_handler(err):
    """Global route to handle all Error Status Codes"""
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)

def setup_global_errors():
    """This updates HTTPException class with custom error function"""
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)

if __name__ == "__main__":
    """MAIN Flask App"""
    #initializes global error handling
    setup_global_errors()
    #start flask app
    app.run(host=host, port=port)
