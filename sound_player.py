import pygame
import time

def play_mp3(filename):
    # Initialize the mixer
    pygame.mixer.init()

    try:
        # Load the mp3 file
        pygame.mixer.music.load(filename)

        # Play the mp3 file
        pygame.mixer.music.play()

        # Wait for the mp3 file to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(1)

    except pygame.error as e:
        print("Error playing mp3 file:", e)

    finally:
        # Stop the mixer
        pygame.mixer.quit()