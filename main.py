import tkinter as tk
import threading
from detect_functions import detect_person, head_movement

# Global variables
current_screen = "first"
previous_screen = None

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
        # Black screen
        self.screens["first"] = FirstScreen(self)
        self.screens["first"].pack(fill="both", expand=True)

        # Game invite screen
        self.screens["invite"] = GameInviteScreen(self)
        self.screens["invite"].pack_forget()

    def show_screen(self, screen_name):
        # Switch between different screens
        global previous_screen
        if previous_screen != screen_name:
            for screen in self.screens.values():
                screen.pack_forget()
            self.screens[screen_name].pack(fill="both", expand=True)
            previous_screen = screen_name

class FirstScreen(tk.Frame):
    # First screen
    def __init__(self, parent):
        super().__init__(parent, bg="lightblue")
        label_main = tk.Label(self, text="Waiting for somebody to show up", font=("Helvetica", 32), bg="lightblue", fg="white")
        label_main.pack(expand=True)

class GameInviteScreen(tk.Frame):
    # Game invite screen
    def __init__(self, parent):
        super().__init__(parent, bg="lightblue")
        label_main = tk.Label(self, text="Would you like to play a game?", font=("Helvetica", 32), bg="lightblue", fg="white")
        label_main.pack(expand=True)
        label_sub = tk.Label(self, text="Nod your head to answer", font=("Helvetica", 20), bg="lightblue", fg="white")
        label_sub.pack()

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

    while True:
        # Set the current screen to first and check for person detection
        current_screen = "first"
        if detect_person():
            # Change the screen to the game invite screen
            current_screen = "invite"

            # Read the head movement response
            result = head_movement()

            if result == "NO":
                # If the person shakes their head NO, set the screen to first
                current_screen = "first"
                continue
            elif result == "YES":
                # TODO
                break

# Create a thread for the tkinter screen manager
tkinter_thread = threading.Thread(target=tkinter_screen_manager)
tkinter_thread.daemon = True
tkinter_thread.start()

if __name__ == "__main__":
    main()
