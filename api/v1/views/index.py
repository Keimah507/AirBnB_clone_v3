#!/usr/bin/python3
"""Flask route that returns json status response"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    """Status route that returns status"""
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route('/stats', methods=['GET'])
def stats():
    """Function to return count of all class objs"""
    if request.method == 'GET':
        response = {}
        PLURALS = {
                "Amenity": "amenities",
                "City": "cities",
                "Place": "places",
                "Review" : "reviews",
                "State" : "states",
                "User": "users"
                }
        for key, value in PLURALS.items():
            response[value] = storage.count(key)
        return jsonify(response)
