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

@app.route("/update", methods=['post'])
def update():
    # PURPOSE: Update each particle in our current session with their new position, velocity, density, and pressure
    # Inside the payload, we are expecting the following formatting:
    # - timestamp:float
    # - frame:int
    # - positions:[{x,y,z},...]
    # - velocities:[{x,y,z},...]
    # - densities:[...]
    # - pressures:[{x,y,z},...]
    payload = request.get_json()
    for i in range(len(current_session.data)):
        current_session.data[i].AddRecord({
            "timestamp":payload["timestamp"],
            "frame":payload["frame"],
            "position":payload["positions"][current_session.data[i].particle_id],
            "velocity":payload["velocities"][current_session.data[i].particle_id],
            "density":payload["densities"][current_session.data[i].particle_id],
            "pressure":payload["pressures"][current_session.data[i].particle_id]
        })
    return "Session updated!"



@app.route("/terminate", methods=['POST'])
def terminate():
    # PURPOSE: ending a recording session and saving all files
    current_session.Terminate(request.get_json())
    return "Session terminated!"

print("Running recorder.py server, skip to my lou, bibbity-bobbity-boo!")
# To run: 
# flask --app hello runexport 