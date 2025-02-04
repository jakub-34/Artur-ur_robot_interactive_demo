import tkinter as tk
import threading
import time
import random
from detect_functions import detect_person, head_movement
# import robot_functions as robot

# Global variables
current_screen = "first"
previous_screen = None
colors = ["red", "green", "blue"]

class App(tk.Tk):
    # Main application window to manage different screens
    def __init__(self):
        super().__init__()
        self.title("Screen Manager")
        self.attributes("-fullscreen", True)
        self.configure(bg="black")

        # Dictionary to store all screens
        self.screens = {}

        # Initialize all screens
        self.init_screens()


    def init_screens(self):
        # Initialize all screens
        self.screens["first"] = FirstScreen(self)
        self.screens["first"].pack(fill="both", expand=True)

        # Game invite screen
        self.screens["invite"] = GameInviteScreen(self)
        self.screens["invite"].pack_forget()

        # Tutorial screen
        self.screens["tutorial"] = TutorialScreen(self)
        self.screens["tutorial"].pack_forget()

        # Tutorial red screen
        self.screens["tutorial_red"] = TutorialRedScreen(self)
        self.screens["tutorial_red"].pack_forget()

        # Tutorial green screen
        self.screens["tutorial_green"] = TutorialGreenScreen(self)
        self.screens["tutorial_green"].pack_forget()

        # Tutorial blue screen
        self.screens["tutorial_blue"] = TutorialBlueScreen(self)
        self.screens["tutorial_blue"].pack_forget()

        # Guessing screen blue
        self.screens["guessing_screen_blue"] = GuessingScreenBlue(self)
        self.screens["guessing_screen_blue"].pack_forget()

        # Guessing screen green
        self.screens["guessing_screen_green"] = GuessingScreenGreen(self)
        self.screens["guessing_screen_green"].pack_forget()

        # Guessing screen red
        self.screens["guessing_screen_red"] = GuessingScreenRed(self)
        self.screens["guessing_screen_red"].pack_forget()

        # Congratulations screen
        self.screens["congratulations"] = CongratulationsScreen(self)
        self.screens["congratulations"].pack_forget()

        # Lying screen
        self.screens["lying_screen"] = LyingScreen(self)
        self.screens["lying_screen"].pack_forget()


    def show_screen(self, screen_name):
        # Switch between different screens
        global previous_screen
        if previous_screen != screen_name:
            for screen in self.screens.values():
                screen.pack_forget()
            self.screens[screen_name].pack(fill="both", expand=True)
            previous_screen = screen_name


class FirstScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightblue")
        label_main = tk.Label(self, text="Waiting for somebody to show up", font=("Helvetica", 56), bg="lightblue", fg="white")
        label_main.pack(expand=True)

class GameInviteScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightblue")
        label_main = tk.Label(self, text="Would you like to play a game?", font=("Helvetica", 56), bg="lightblue", fg="white")
        label_main.pack(expand=True)
        label_sub = tk.Label(self, text="Nod your head to answer", font=("Helvetica", 20), bg="lightblue", fg="white")
        label_sub.pack()

class TutorialScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightblue")
        label_main = tk.Label(self, text= "Okey, so here are the rules:\nYou will think of one of the three colors and I will try to guess it.\nHere are our possible colors:", font=("Helvetica", 46), bg="lightblue", fg="white")
        label_main.pack(expand=True)

class TutorialRedScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="red")
        label_main = tk.Label(self, text= "Red", font=("Helvetica", 56), bg="red", fg="white")
        label_main.pack(expand=True)

class TutorialGreenScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="green")
        label_main = tk.Label(self, text= "Green", font=("Helvetica", 56), bg="green", fg="white")
        label_main.pack(expand=True)

class TutorialBlueScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="blue")
        label_main = tk.Label(self, text= "Blue", font=("Helvetica", 56), bg="blue", fg="white")
        label_main.pack(expand=True)

class GuessingScreenBlue(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="blue")
        label_main = tk.Label(self, text="I thing, your color is blue.\nAm I right?", font=("Helvetica", 56), bg="blue", fg="white")
        label_main.pack(expand=True)
        label_sub = tk.Label(self, text="Nod your head to answer", font=("Helvetica", 20), bg="blue", fg="white")
        label_sub.pack()

class GuessingScreenGreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="green")
        label_main = tk.Label(self, text="I thing, your color is green.\nAm I right?", font=("Helvetica", 56), bg="green", fg="white")
        label_main.pack(expand=True)
        label_sub = tk.Label(self, text="Nod your head to answer", font=("Helvetica", 20), bg="green", fg="white")
        label_sub.pack()

class GuessingScreenRed(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="red")
        label_main = tk.Label(self, text="I thing, your color is red.\nAm I right?", font=("Helvetica", 56), bg="red", fg="white")
        label_main.pack(expand=True)
        label_sub = tk.Label(self, text="Nod your head to answer", font=("Helvetica", 20), bg="red", fg="white")
        label_sub.pack()

class CongratulationsScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightblue")
        label_main = tk.Label(self, text="We did it!!!", font=("Helvetica", 56), bg="lightblue", fg="white")
        label_main.pack(expand=True)

class LyingScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightblue")
        label_main = tk.Label(self, text="You are lying, we're done!", font=("Helvetica", 56), bg="lightblue", fg="white")
        label_main.pack(expand=True)


def tkinter_screen_manager():
    # Manage the tkinter screen
    global current_screen

    app = App()

    def update_screen():
        # Update the screen based on the current state
        app.show_screen(current_screen)
        app.after(100, update_screen)

    update_screen()
    app.bind("<Escape>", lambda event: app.destroy())  # Press 'Esc' to exit the app
    app.mainloop()

def main():
    global current_screen

    # robot.start()

    while True:
        # Set the current screen to first and check for person detection
        current_screen = "first"
        if detect_person(infinite=True):
            # Change the screen to the game invite screen
            current_screen = "invite"

            # Read the head movement response
            result = head_movement()

            if result == "NO":
                # If the person shakes their head NO, set the screen to first
                current_screen = "first"
                continue
            elif result == "YES":
                # Start tutorial
                current_screen = "tutorial"
                time.sleep(6)  # Wait for 6 seconds

                # Check if the person is still present
                if not detect_person():
                    continue

                # Show the red screen and red cube
                current_screen = "tutorial_red"
                # TODO: Add robot movement to show the red cube
                time.sleep(2) # Simulate the time taken to show the red cube
                # TODO: Add robot movement to show the red cube

                # Show the green screen and green cube
                current_screen = "tutorial_green"
                # TODO: Add robot movement to show the green cube
                time.sleep(2) # Simulate the time taken to show the green cube
                # TODO: Add robot movement to show the green cube

                # Show the blue screen and blue cube
                current_screen = "tutorial_blue"
                # TODO: Add robot movement to show the blue cube
                time.sleep(2)
                # TODO: Add robot movement to show the blue cube
                
                # Check if the person is still present
                if not detect_person():
                    continue

                # Start the game
                game_colors = colors.copy()
                guessed = False
                while not guessed:
                    # Check if the person is not lying
                    if not game_colors:
                        current_screen = "lying_screen"
                        time.sleep(6)
                        break
                    color = random.choice(game_colors)
                    # TODO: Add robot movement to show the game color everywhere
                    if color == "red":
                        current_screen = "guessing_screen_red"

                        # Check if the person is still present
                        if not detect_person():
                            break

                        result = head_movement()
                        if result == "YES":
                            guessed = True
                        elif result == "NO":
                            game_colors.remove("red")

                    elif color == "green":
                        current_screen = "guessing_screen_green"

                        # Check if the person is still present
                        if not detect_person():
                            break

                        result = head_movement()
                        if result == "YES":
                            guessed = True
                        elif result == "NO":
                            game_colors.remove("green")

                    elif color == "blue":
                        current_screen = "guessing_screen_blue"

                        # Check if the person is still present
                        if not detect_person():
                            break

                        result = head_movement()
                        if result == "YES":
                            guessed = True
                        elif result == "NO":
                            game_colors.remove("blue")

                if not guessed:
                    continue

                # Congratulate
                current_screen = "congratulations"
                time.sleep(6)



# Create a thread for the tkinter screen manager
tkinter_thread = threading.Thread(target=tkinter_screen_manager)
tkinter_thread.daemon = True
tkinter_thread.start()

if __name__ == "__main__":
    main()
