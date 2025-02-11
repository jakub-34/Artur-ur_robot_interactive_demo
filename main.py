#!/usr/bin/env python3

import threading
import sys
from robot_eyes import run_eyes
from detect_functions import detect_person, head_movement
from sound_player import play_mp3
import robot_control as robot
from poses import *


# Start the robot eyes
eye_thread = threading.Thread(target=run_eyes)
eye_thread.start()


def ask_question(filename: str) -> str:
    while True:
        if not detect_person():
            return "QUIT"
        
        play_mp3(filename)
        answer = head_movement(timed = True, timer = 10)
        if answer == "NA":
            continue
        else:
            return answer
        

def show_cube(cube: Pose, setup: Pose, sound: str) -> None:
    robot.put_pose(setup)
    robot.put_pose(cube)
    robot.suck()
    robot.put_pose(setup)
    robot.put_pose(show_cube_pose)
    play_mp3(sound)
    robot.put_pose(setup)
    robot.put_pose(cube)
    robot.release()
    robot.put_pose(setup)
    robot.put_pose(standby_pose)


def main() -> None:
    # Start the robot if needed
    if len(sys.argv) > 1 and sys.argv[1] == "-s":
        robot.start()

    robot.put_pose(standby_pose)

    while True:
        # Check if a person is detected
        if detect_person(infinite = True):
            answer = ask_question("sounds/game_invite.mp3")

            # Person left
            if answer == "QUIT":
                continue

            # Person don't want to play
            if answer == "NO":
                play_mp3("sounds/dont_want_to_play.mp3")
                continue

            # Person want to play
            if answer == "YES":
                play_mp3("sounds/explain_rules_start.mp3")
                
                # Show the cubes
                show_cube(red_cube_pose, red_setup_pose, "sounds/the_red_one.mp3")
                show_cube(green_cube_pose, green_setup_pose, "sounds/green_one.mp3")
                show_cube(blue_cube_pose, blue_setup_pose, "sounds/and_a_blue_one.mp3")
                

if __name__ == "__main__":
   main()