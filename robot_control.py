import requests
import sys
from poses import Pose


url = "http://192.168.104.100:5012"
max_attempts = 3


def start():
    start_url = url + "/state/start"

    data = {
        "orientation": {
            "w": 1,
            "x": 0,
            "y": 0,
            "z": 0
        },
        "position": {
            "x": 0,
            "y": 0,
            "z": 0
        }
    }

    attempts = 0

    while attempts < max_attempts:
        response = requests.put(start_url, json=data)

        if response.status_code == 200 or response.status_code == 204:
            return
        
        attempts += 1
        print("Error starting robot", file=sys.stderr)
    
    print("Final error starting robot", file=sys.stderr)
    sys.exit(1)


def put_pose(position: Pose, payload = 0):
    pose_url = url + "/eef/pose"

    params = {
        "velocity": 50,
        "payload": payload
    }

    data = position.to_dict()

    attempts = 0

    while attempts < max_attempts:
        response = requests.put(pose_url, params=params, json=data)

        if response.status_code == 200 or response.status_code == 204:
            return

        attempts += 1
        print("Error setting pose", file=sys.stderr)

    print("Final error setting pose", file=sys.stderr)
    sys.exit(1)


def suck():
    suck_url = url + "/suction/suck"

    params = {
        "vacuum" : 80
    }

    attempts = 0

    while attempts < max_attempts:
        response = requests.put(suck_url, params=params)
        if response.status_code == 200 or response.status_code == 204:
            return
        attempts += 1
        print("Error, failed to suck", file=sys.stderr)

    print("Final error, failed to suck", file=sys.stderr)
    sys.exit(1)


def release():
    release_url = url + "/suction/release"

    attempts = 0

    while attempts < max_attempts:
        response = requests.put(release_url)
        if response.status_code == 200 or response.status_code == 204:
            return
        attempts += 1
        print("Error, failed to release", file=sys.stderr)

    
    print("Final error, failed to release", file=sys.stderr)
    sys.exit(1)