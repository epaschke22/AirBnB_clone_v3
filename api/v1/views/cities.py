#!/usr/bin/python3
"""creates a new view for City objects"""
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def city_list(state_id):
    """retrieves the list of all city objects of a state object"""
    stateobj = storage.get(State, state_id)
    if stateobj is None:
        abort(404)
    city_list = []
    for city in stateobj.cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def city_id(city_id):
    """retrieves a city object"""
    try:
        cityobj = storage.get(City, city_id).to_dict()
        return jsonify(cityobj)
    except Exception:
        abort(404)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def city_delete(city_id):
    """deletes a city object"""
    cityobj = storage.get(City, city_id)
    if cityobj is not None:
        storage.delete(cityobj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create(state_id):
    """creates a city object"""
    try:
        if not request.get_json():
            return jsonify({"error": "Not a JSON"}), 400
        body_dict = request.get_json()
    except:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in body_dict:
        return jsonify({"error": "Missing name"}), 400
    if storage.get(State, state_id) is None:
        abort(404)
    city = City(**body_dict)
    for key, value in request.get_json().items():
        setattr(city, key, value)
    setattr(city, "state_id", state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update(city_id):
    """updates existing city object"""
    cityobj = storage.get(City, city_id)
    if cityobj is None:
        abort(404)
    try:
        body_dict = request.get_json()
    except:
        return jsonify({"error": "Not a JSON"}), 400
    if body_dict is None:
        abort(400, "Not a JSON")
    body_dict.pop("id", None)
    body_dict.pop("created_at", None)
    body_dict.pop("updated_at", None)
    for key, value in body_dict.items():
        setattr(cityobj, key, value)
    cityobj.save()
    return jsonify(cityobj.to_dict()), 200
