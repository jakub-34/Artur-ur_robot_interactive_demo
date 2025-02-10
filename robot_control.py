import requests
import sys


url = "http://localhost:5012"

velocity = 50
payload = 0


class Pose:
    def __init__(self, orientation, position):
        self.orientation = orientation
        self.position = position

    def __repr__(self):
        return str({
            "orientation": self.orientation,
            "position": self.position
        })
    
    def to_dict(self):
        return {
            "orientation": self.orientation,
            "position": self.position
        }


test_pose = Pose(
    orientation={
        "w": 0.012478298327523696,
        "x": 0.9998434779226774,
        "y": 0.0003918678270916007,
        "z": -0.012536274005463543
    },
    position={
        "x": 0.14396865671352158,
        "y": 0.4356200608031923,
        "z": 0.20203002542838552
    }
)


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

    response = requests.put(start_url, json=data)

    if response.status_code == 200 or response.status_code == 204:
        print("Robot started")
        return
    
    else:
        print("Error starting robot")
        sys.exit(1)


def put_pose(position: Pose):
    pose_url = url + "/eef/pose"

    params = {
        "velocity": velocity,
        "payload": payload
    }

    data = position.to_dict()

    response = requests.put(pose_url, params=params, json=data)

    print(response.status_code)

    if response.status_code == 200 or response.status_code == 204:
        print("Set pose finished")
        return

    else:
        print("Error setting pose")
        sys.exit(1)


put_pose(test_pose)