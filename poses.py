class Pose:
    def __init__(self, orientation, position):
        self.orientation = orientation
        self.position = position

    def __repr__(self):
        return str({
            "orientation": self.orientation,
            "position": self.position
        })
    
    def to_dict(self) -> dict:
        return {
            "orientation": self.orientation,
            "position": self.position
        }


def height_to_z(height_cm: float) -> float:
    height_m = height_cm / 100
    return height_m - 0.78682704677


table_height = 0.0
cube_height = 0.0
cube_setup_height = 0.0

red_cube_pose = None
red_setup_pose = None
blue_cube_pose = None
blue_setup_pose = None
green_cube_pose = None
green_setup_pose = None


def initialize_poses(table_height_cm: float):
    global table_height, cube_height, cube_setup_height
    global red_cube_pose, red_setup_pose, green_cube_pose, green_setup_pose, blue_cube_pose, blue_setup_pose
    table_height = height_to_z(table_height_cm)
    cube_height = table_height + 0.1
    cube_setup_height = table_height + 0.2

    red_cube_pose = Pose(
        orientation = {
            "w": -0.00514295756539651,
            "x": -0.720693245039779,
            "y": -0.6932275512302452,
            "z": 0.003218502265262573
        },
        position = {
            "x": 0.21098386329,
            "y": 0.9695235132079939,
            "z": cube_height
        }
    )

    red_setup_pose = Pose(
        orientation = {
            "w": -0.00514295756539651,
            "x": -0.720693245039779,
            "y": -0.6932275512302452,
            "z": 0.003218502265262573
        },
        position = {
            "x": 0.21098386329,
            "y": 0.9695235132079939,
            "z": cube_setup_height
        }
    )

    green_cube_pose = Pose(
        orientation = {
            "w": -0.00514295756539651,
            "x": -0.720693245039779,
            "y": -0.6932275512302452,
            "z": 0.003218502265262573
        },
        position = {
            "x": 0.030983863296055923,
            "y": 0.9695235132079939,
            "z": cube_height
        }
    )
    
    green_setup_pose = Pose(
        orientation = {
            "w": -0.00514295756539651,
            "x": -0.720693245039779,
            "y": -0.6932275512302452,
            "z": 0.003218502265262573
        },
        position = {
            "x": 0.030983863296055923,
            "y": 0.9695235132079939,
            "z": cube_setup_height
        }
    )

    blue_cube_pose = Pose(
        orientation = {
            "w": -0.00514295756539651,
            "x": -0.720693245039779,
            "y": -0.6932275512302452,
            "z": 0.003218502265262573
        },
        position = {
            "x": -0.1490161367,
            "y": 0.9695235132079939,
            "z": cube_height
        } 
    )

    blue_setup_pose = Pose(
        orientation = {
            "w": -0.00514295756539651,
            "x": -0.720693245039779,
            "y": -0.6932275512302452,
            "z": 0.003218502265262573
        },
        position = {
            "x": -0.1490161367,
            "y": 0.9695235132079939,
            "z": cube_setup_height
        }
    )


standby_pose = Pose(
    orientation = {
        "w": 0.05430049823231364,
        "x": -0.7093649746130042,
        "y": -0.7014148857904697,
        "z": -0.04324288005622226
    },
    position = {
        "x": 0.08320715794882973,
        "y": 0.7751766550910051,
        "z": 0.42919554218026174
    }
)

show_cube_pose = Pose(
    orientation = {
        "w": 0.53417401936446,
        "x": -0.46104886510921317,
        "y": -0.4955661338938372,
        "z": -0.5064644784731102
    },
    position = {
        "x": 0.07167873480173187,
        "y": 0.8536525577470017,
        "z": 0.5731361369621198
    }
)

win_pose = Pose(
    orientation = {
        "w": 0.6980102945205288,
        "x": -0.20225462381937637,
        "y": -0.24192131451928583,
        "z": -0.6429220586263221
    },
    position = {
        "x": 0.1896764586445854,
        "y": 0.35746743952571275,
        "z": 0.9949658810228532
    }
)