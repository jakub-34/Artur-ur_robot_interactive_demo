import threading
from robot_eyes import run_eyes
from detect_functions import detect_person, head_movement
from sound_player import play_mp3


# Start the robot eyes
eye_thread = threading.Thread(target=run_eyes)
eye_thread.start()


def main() -> None:
    while True:
        # Check if a person is detected
        if detect_person(infinite = True):
            play_mp3("sounds/game_invite.mp3")
            answer = head_movement()

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