import threading
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

def play_sound(sound_file):
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except Exception as e:
        print("Sound error:", e)

def check_crowd_alert(frame_count, people_count, threshold):
    """
    Plays sound alert if people_count > threshold.
    Non-blocking using threading.
    """
    if people_count > threshold:
        print(f"⚠ Crowd alert at frame {frame_count}! People count: {people_count}")

        sound_file = r"C:\Users\kritk\OneDrive\Desktop\censor-beep-1-372459.mp3"
        if os.path.exists(sound_file):
            threading.Thread(target=play_sound, args=(sound_file,), daemon=True).start()
        else:
            print("Sound file not found:", sound_file)