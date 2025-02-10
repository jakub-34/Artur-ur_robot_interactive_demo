#!/usr/bin/env python3

import threading
from robot_eyes import run_eyes
from detect_functions import detect_person, head_movement
from sound_player import play_mp3


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


def main() -> None:
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
                break


if __name__ == "__main__":
   main()