#!/usr/bin/env python3

import threading
import sys
import time
import random
from robot_eyes import run_eyes
from detect_functions import detect_person, head_movement
from sound_player import play_mp3
import robot_control as robot
from poses import *


server_ip = ""


# Start the robot eyes
eye_thread = threading.Thread(target=run_eyes)


# Print help message
def print_help():
    print("Usage: ./Artur.py -a <IP:PORT> [-s] [-h]")
    print("  -a <IP:PORT>  Specify the server IP address and port (required)")
    print("  -s            Start the robot (optional)")
    print("  -h            Show this help message and exit")
    sys.exit(0)


# Ask a question to the person
# Return the answer or "QUIT" if the person left
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
        

def show_cube(server_ip: str, cube: Pose, setup: Pose, sound="none") -> None:
    robot.put_pose(server_ip, setup)
    robot.put_pose(server_ip, cube)
    robot.suck(server_ip)
    robot.put_pose(server_ip, setup, 0.12)
    robot.put_pose(server_ip, show_cube_pose, 0.12)

    if sound != "none":
        play_mp3(sound)

    robot.put_pose(server_ip, setup, 0.12)
    robot.put_pose(server_ip, cube, 0.12)
    robot.release(server_ip)
    robot.put_pose(server_ip, setup)
    robot.put_pose(server_ip, standby_pose)


def ask_color_question(server_ip: str, cube: Pose, setup: Pose, color: str, game_colors) -> str:
    # Show cube
    robot.put_pose(server_ip, setup)
    robot.put_pose(server_ip, cube)
    robot.suck(server_ip)
    robot.put_pose(server_ip, setup, 0.12)
    robot.put_pose(server_ip, show_cube_pose, 0.12)

    # Ask question
    answer = ask_question("sounds/color_question.mp3")

    # Person left
    if answer == "QUIT":
        # Return the cube
        robot.put_pose(server_ip, setup, 0.12)
        robot.put_pose(server_ip, cube, 0.12)
        robot.release(server_ip)
        robot.put_pose(server_ip, setup)
        robot.put_pose(server_ip, standby_pose)
        return "QUIT"
    
    # Person guessed the color
    elif answer == "YES":
        robot.put_pose(server_ip, win_pose)
        play_mp3("sounds/yay.mp3")
        robot.put_pose(server_ip, standby_pose)
        # Return the cube
        robot.put_pose(server_ip, setup, 0.12)
        robot.put_pose(server_ip, cube, 0.12)
        robot.release(server_ip)
        robot.put_pose(server_ip, setup)
        robot.put_pose(server_ip, standby_pose)
        play_mp3("sounds/thank.mp3")
        return "YES"
    
    # Person didn't guess the color
    else:
        # Return the cube
        robot.put_pose(server_ip, setup, 0.12)
        robot.put_pose(server_ip, cube, 0.12)
        robot.release(server_ip)
        robot.put_pose(server_ip, setup)
        robot.put_pose(server_ip, standby_pose)
        game_colors.remove(color)

        # Try again
        if game_colors:
            play_mp3("sounds/try_again.mp3")
            return "NO"
        else:
            robot.put_pose(server_ip, show_cube_pose)
            play_mp3("sounds/lying.mp3")
            robot.put_pose(server_ip, standby_pose)
            return "QUIT"
    

def main() -> None:
    # Parse arguments
    if "-h" in sys.argv:
        print_help()
    
    if "-a" not in sys.argv:
        print("Error: Missing required argument -a")
        print_help()
    
    try:
        a_index = sys.argv.index("-a")
        server_ip = sys.argv[a_index + 1]
    except (ValueError, IndexError):
        print("Error: Missing value for -a")
        print_help()
    
    # Check if -s is provided
    if "-s" in sys.argv:
        robot.start(server_ip)

    # Start the robot eyes
    eye_thread.start()

    next = False
    colors = ["red", "green", "blue"]

    robot.put_pose(server_ip, standby_pose)

    while True:
        # Check if a person is detected
        if detect_person(infinite = True, show_camera = True):
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
                show_cube(server_ip, red_cube_pose, red_setup_pose, "sounds/the_red_one.mp3")
                show_cube(server_ip, green_cube_pose, green_setup_pose, "sounds/green_one.mp3")
                show_cube(server_ip, blue_cube_pose, blue_setup_pose, "sounds/and_a_blue_one.mp3")

                # Ask if the person is ready
                play_mp3("sounds/explaining_finished.mp3")
                answer = ask_question("sounds/ready.mp3")

                # Person is not ready or left
                while answer != "YES":
                    # Person left
                    if answer == "QUIT":
                        next = True
                        break

                    play_mp3("sounds/time.mp3")
                    time.sleep(5)
                    answer = ask_question("sounds/ready.mp3")

                # Person is left
                if next:
                    next = False
                    continue

                # Person is ready
                play_mp3("sounds/okay_so.mp3")

                # Guess the color
                game_colors = colors.copy()
                while True:
                    # Pick one color
                    color = random.choice(game_colors)

                    # Red cube guess
                    if color == "red":
                        answer = ask_color_question(server_ip, red_cube_pose, red_setup_pose, color, game_colors)
                        if answer == "QUIT" or answer == "YES":
                            break

                    # Green cube guess
                    elif color == "green":
                        answer = ask_color_question(server_ip, green_cube_pose, green_setup_pose, color, game_colors)
                        if answer == "QUIT" or answer == "YES":
                            break

                    # Blue cube guess
                    else:
                        answer = ask_color_question(server_ip, blue_cube_pose, blue_setup_pose, color, game_colors)
                        if answer == "QUIT" or answer == "YES":
                            break
                

if __name__ == "__main__":
   main()