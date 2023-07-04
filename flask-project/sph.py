import os
import math
import json

class SPH_SESSION:
    details = {
        "session_name": "",
        "timestamp": ""
    }
    configurations = {
        "num_particles": 0,
        "dt": 0,
        "render_radius": 0,
        "h": 0,
        "rest_density": 0,
        "mu": 0,
        "k": 0
    }
    data = []
    results = {
        "duration": 0,
        "frames": 0,
        "success": 0
    }
    def Initialize(self, payload):
        self.details = {
            "session_name": payload["session_name"],
            "timestamp": payload["timestamp"]
        }
        self.configurations = {
            "num_particles": payload["num_particles"],
            "dt": payload["dt"],
            "render_radius": payload["render_radius"],
            "h": payload["h"],
            "rest_density": payload["rest_density"],
            "mu": payload["mu"],
            "k": payload["k"]
        }
        
        self.data = []
        for i in range(self.configurations["num_particles"]):
            self.data.append(SPH_PARTICLE_RECORD({"particle_id":i}))

    def Update(self, payload):
        timestamp = payload["timestamp"]
        frame = payload["frame"]
        for p in payload["particles"]:
            self.data[p["particle_id"]].AddRecord({
                "timestamp":timestamp,
                "frame":frame,
                "position":p["position"],
                "velocity":p["velocity"],
                "density":p["density"],
                "pressure":p["pressure"]
            })
    
    def Terminate(self, payload):
        # Get the results from payload
        self.results = {
            "duration": payload["duration"],
            "frames": payload["frames"],
            "success": payload["success"]
        }
        # Create a directory inside of the "Recordings" directory, create "Recordings" if it doesn't exist
        os_dirname = os.path.dirname(os.path.abspath(__file__))
        recordingDirPath = os.path.join(os_dirname,"Recordings")
        if not os.path.exists(recordingDirPath):
            os.mkdir(recordingDirPath)
        dirPath = os.path.join(os_dirname, "Recordings" , self.details["session_name"] + "_" + self.details["timestamp"]) + "/"
        # Create a directory inside "Recordings"
        os.mkdir(dirPath)
        # Create a subdirectory inside the newly-created folder specifically for particles
        recordDirPath = dirPath + "/particles/"
        os.mkdir(recordDirPath)
        # Let's save our session data first
        session_dump = json.dumps({
            "details":self.details,
            "configurations":self.configurations,
            "results":self.results
        })
        with open(dirPath+"session.json","w") as outfile:
            outfile.write(session_dump)
        # Let's now save each individual particle recording
        for p in self.data:
            p.SortRecords()
            p.SaveRecords(recordDirPath)
    
    def GetSnapshot(self, include_particles=False):
        # Initialize return payload
        payload = {
            "details":self.details,
            "configurations":self.configurations,
            "results":self.results,
        }
        # Include particle data if prompted
        if include_particles:
            payload["data"] = []
            for p in self.data:
                payload["data"].append(p.__dict__)
        # Send the payload back
        return payload

class SPH_PARTICLE_RECORD:
    particle_id = 0
    positions = []
    velocities = []
    densities = []
    pressures = []
    
    def __init__(self, payload):
        self.particle_id = payload["particle_id"]
        self.positions = []
        self.velocities = []
        self.densities = []
        self.pressures = []
    
    def AddRecord(self,payload):
        timestamp = payload["timestamp"]
        frame = payload["frame"]
        # We expect position to be a dictionary with "x", "y", and "z"
        self.positions.append({
            "timestamp":timestamp, "frame":frame, 
            "value":payload["position"]
        })
        # We expect velocity to be a dictionary with "x","y", and "z"
        self.velocities.append({
            "timestamp":timestamp, "frame":frame,
            "value":payload["velocity"]
        })
        # We expect density to be a singular float
        self.densities.append({
            "timestamp":timestamp, "frame":frame,
            "value":payload["density"]
        })
        # We expect pressure to be a dictionary with "x", "y", and "z"
        self.pressures.append({
            "timestamp":timestamp, "frame":frame,
            "value":payload["pressure"]
        })
    
    def SortRecords(self):
        self.positions.sort(key=lambda x: x["frame"], reverse=False)
        self.velocities.sort(key=lambda x: x["frame"], reverse=False)
        self.densities.sort(key=lambda x: x["frame"], reverse=False)
        self.pressures.sort(key=lambda x: x["frame"], reverse=False)

    def SaveRecords(self,dirPath):
        # Note that we expect dirPath to end with "/"
        saveIn = dirPath
        if not dirPath.endswith("/"):
            saveIn += "/"            
        # double-check that the path is valid
        if not os.path.exists(saveIn):
            print("ERROR [{}]: Directory path doesn't exist: {}".format(self.particle_id,saveIn))
            return
        # define the data to be written
        json_payload = json.dumps(self.__dict__)
        filename = saveIn + str(self.particle_id) + ".json"
        with open(filename,"w") as outfile:
            outfile.write(json_payload)