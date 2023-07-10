from flask import Flask, jsonify, request
import os
import math
import json

from sph import SPH_SESSION

app = Flask(__name__)
current_session = SPH_SESSION()

@app.route("/", methods=["GET"])
def do_get():
    return "<html><body><h1>Hello</h1></body></html>"

@app.route("/snapshot", methods=["GET"])
def check_session():
    # Extract a query param from the URL request
    # In this case, we are isolating whether we want to include  particle data
    include_particle_query = request.args.get("include_particles","false")
    include_particles = include_particle_query.lower() in ['true', '1', 't']
    start_index = int(request.args.get("start","0"))
    end_index = min(int(request.args.get("end",current_session.configurations["num_particles"])),200)
    # Get the payload
    payload = current_session.GetSnapshot(start_index,end_index,include_particles)
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

###@app.route("/update", methods=['POST'])
###def update():
    # PURPOSE: Update each particle in our current session with their new position, velocity, density, and pressure
    # Inside the payload, we are expecting the following formatting:
    # - timestamp:float
    # - frame:int
    # - positions:[{x,y,z},...]
    # - velocities:[{x,y,z},...]
    # - densities:[...]
    # - pressures:[{x,y,z},...]
###    payload = request.get_json()
###    for i in range(len(current_session.data)):
###        current_session.data[i].AddRecord({
###            "timestamp":payload["timestamp"],
###            "frame":payload["frame"],
###            "value":payload["value"]
###            "position":payload["positions"][current_session.data[i].particle_id],
###            "velocity":payload["velocities"][current_session.data[i].particle_id],
###            "density":payload["densities"][current_session.data[i].particle_id],
###            "pressure":payload["pressures"][current_session.data[i].particle_id]
###        })
###    return "Session updated!"

@app.route("/update_batch", methods=['POST'])
def update_batch():
    # PURPOSE: Update a batch of recordings. Each recording is agnostic to particle ID, as the items inside will indicate what particle they need to udpate
    # insid the payload, we expect the following format:
    # - batch : [{<LOOK AT update_particle() FOR REFERENCE ON STRUCTURE>}...]
    payload = request.get_json();
    for bi in payload["batch"]:
        pi = int(bi["particle_id"])
        current_session.data[pi].AddRecord({
            "timestamp":bi["timestamp"],
            "frame":bi["frame"],
            "value":bi["value"],
        })
    return "Batch_Updated!"

@app.route("/update_particle", methods=['POST'])
def update_particle():
    # PURPOSE: update a single particle in our current session with their new position, velocity, density, and pressure
    # Inside the payload, we expect the following formatting:
    # - particle_id : int
    # - timestamp : float
    # - frame : int
    # - position : {x,y,z}
    # - velocity: {x,y,z},
    # - density : float
    # - pressure : {x,y,z}
    payload = request.get_json()
    current_session.data[int(payload["particle_id"])].AddRecord({
        "timestamp":payload["timestamp"],
        "frame":payload["frame"],
        "value":payload["value"],
    })
    return "Particle updated!"

@app.route("/update_session", methods=['POST'])
def update_session():
    payload = request.get_json()
    current_session.Self_Update(payload)
    return "Session updated!"

@app.route("/save", methods=['Get'])
def save():
    # PURPOSE: ending a recording session and saving all files
    filetype_query = request.args.get("filetype","json")
    current_session.Save(filetype_query)
    return "Session terminated!"

print("Running recorder.py server, skip to my lou, bibbity-bobbity-boo!")
# To run: 
# flask --app hello runexport 