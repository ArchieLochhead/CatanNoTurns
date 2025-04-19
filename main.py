# Creating a script to play Catan without turns and dice rolling
# Needs to randomly show a number 1-12 at specific time intervals

import tkinter as tk
import random
import subprocess


dice_roll_sound = '/Users/Archie/Documents/Python Projects/CatanNoTurns/DiceRollSound.mp3'
oh_yeh_sound = '/Users/Archie/Documents/Python Projects/CatanNoTurns/OhYehSound.mp3'
catan_music = None
volume = 0.2 # default volume = 100%


rolling = None  # To store the scheduled task ID
time_between_rolls = 15000 #default

players = ["Archie", "Harris", "Niven", "Newman"]

def roll_dice():
    global rolling
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    result_label_1.config(text=f"{total}")

# Make it 'subprocess.Popen()' or '.run' to have the number show before the audio is done.
    #subprocess.Popen(['ffmpeg', '-i', dice_roll_sound, '-f', 'wav', 'pipe:1', '|', 'ffplay', '-nodisp', '-autoexit', '-'])
    subprocess.Popen(['ffplay', '-nodisp', '-autoexit', dice_roll_sound])

    if total == 7:
        robber_label.config(text=f"Robber is {random.choice(players)}")
        subprocess.Popen(['afplay', oh_yeh_sound])
    else:
        robber_label.config(text="")


    # Schedule the next roll after 60 seconds (60000 ms)
    rolling = root.after(time_between_rolls, roll_dice)

def start_rolling():
    global rolling
    if rolling is None:
        roll_dice()

def stop_rolling():
    global rolling
    if rolling is not None:
        root.after_cancel(rolling)
        rolling = None
        result_label_1.config(text="Paused")

# Music
def start_music():
    global catan_music
    if catan_music:
        catan_music.kill()  # Kill previous music if it's already playing

    # Using afplay directly for simpler music playback and volume control
    catan_music = subprocess.Popen([
        'afplay', '/Users/Archie/Documents/Python Projects/CatanNoTurns/CatanMusic.mp3',
        '-v', str(volume)  # Set volume directly with afplay
    ])


def stop_music():
    global catan_music
    if catan_music:
        catan_music.kill()
        catan_music = None


def update_volume(val):
    global volume
    volume = float(val) / 100
    print(f"Volume set to {volume * 100}%")
    # Restart music with the updated volume
    if catan_music:
        stop_music()  # Stop current music
        start_music()  # Start music with new volume

# Create the main window
background_colour = "#bc2127"

root = tk.Tk()
root.geometry("1500x800")
root.title("Dice Roller")
root['bg'] = background_colour

# Create Title

Title = tk.Label(root, text="Catan: No-Turns Mode", font=("Minion Pro SmBd", 100), fg="#fec907")
Title.pack(pady=0)
Title['bg'] = background_colour

# Label to display the result
result_label_1 = tk.Label(root, text="", font=("Arial", 300), fg="white")
result_label_1.pack(pady=10)
result_label_1['bg'] = background_colour

robber_label = tk.Label(root, text="", font=("Arial", 100), fg="white")
robber_label.pack(pady=2)
robber_label['bg'] = background_colour

# Time input label and field
time_frame = tk.Frame(root, bg=background_colour)
time_frame.pack(pady=(20, 0))

time_label = tk.Label(time_frame, text="Time between rolls (s):", font=("Arial", 20), fg="white", bg=background_colour)
time_label.pack(side="left", padx=5)

time_input = tk.Entry(time_frame, font=("Arial", 20), justify="center", bg="#444", fg="white", width=10)
time_input.insert(0, "15")  # Default value
time_input.pack(side="left", padx=5)

def update_time(event=None):
    global time_between_rolls
    try:
        new_time = int(time_input.get()) * 1000  # Convert to milliseconds
        if new_time > 0:
            time_between_rolls = new_time
            print(f"Time between rolls set to {new_time / 1000} seconds")

            #remove focus from input box
            root.focus_set()
        else:
            print("Time must be greater than zero.")
    except ValueError:
        print("Please enter a number.")

# Bind Enter key to update time
root.bind('<Return>', update_time)

# Button frame (keeps them aligned)
button_frame = tk.Frame(root, bg=background_colour)
button_frame.pack(pady=20)

# Start button
start_button = tk.Button(button_frame, text="Start", command=start_rolling, font=("Arial", 14), highlightbackground=background_colour)
start_button.pack(side="left", padx=20)

# Stop button
stop_button = tk.Button(button_frame, text="Stop", command=stop_rolling, font=("Arial", 14), highlightbackground=background_colour)
stop_button.pack(side="right", padx=20)

# Volume Slider
volume_slider = tk.Scale(
    root,
    from_=20, to=0,
    orient="vertical",
    label="",
    command=update_volume,
    bg=background_colour,  # Background color
    fg="white",  # Text color
    troughcolor=background_colour,  # Track color
    highlightbackground="#333",  # Border color
    activebackground="yellow"  # Color when active
)
volume_slider.set(3)  # Default to 100%
volume_slider.place(x=50,y=250,width=50,height=300)

# Music button start
start_music_button = tk.Button(button_frame, text="Music On", command=start_music, font=("Arial", 14), highlightbackground=background_colour)
start_music_button.pack(side="left", padx=0)

# Music button stop
stop_music_button = tk.Button(button_frame, text="Music Off", command=stop_music, font=("Arial", 14), highlightbackground=background_colour)
stop_music_button.pack(side="left", padx=0)


# Function that determines if it's on or off to use spacebar as toggle
def toggle_rolling(event=None):
    if rolling is None:
        start_rolling()
    else:
        stop_rolling()


# Bind spacebar to toggle rolling
root.bind('<space>', toggle_rolling)


# Start the main loop
root.mainloop()
