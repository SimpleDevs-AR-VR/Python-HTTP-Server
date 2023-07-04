from flask import Flask, jsonify, request
import os
import math
import json

from sph import SPH_SESSION

app = Flask(__name__)
current_session = SPH_SESSION()

@app.route("/snapshot", methods=["GET"])
def check_session():
    # Extract a query param from the URL request
    # In this case, we are isolating whether we want to include  particle data
    include_particle_query = request.args.get("include_particles","false")
    include_particles = include_particle_query.lower() in ['true', '1', 't']
    # Get the payload
    payload = current_session.GetSnapshot(include_particles)
    # Return the payload
    return jsonify(payload)

@app.route("/create", methods=['POST'])
def init():
    # PURPOSE: creates a new SPH session using the provided credentials:
    # - "session_name" 
    # - "timestamp" 
    # - "dt"
    # - "num_particles" 
    # - "render_radius"
    # - "h"
    # - "rest_density"
    # - "mu"
    # - "k"
    
    payload = request.get_json()
    current_session.Initialize(payload)
    return jsonify(payload)

print("Running recorder.py server, skip to my lou, bibbity-bobbity-boo!")
# To run: 
# flask --app hello runexport 