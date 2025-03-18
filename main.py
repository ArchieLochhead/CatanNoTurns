# Creating a script to play Catan without turns and dice rolling
# Needs to randomly show a number 1-12 at specific time intervals

import tkinter as tk
import random
import subprocess


dice_roll_sound = '/Users/Archie/Documents/Python Projects/CatanNoTurns/DiceRollSound.mp3'
oh_yeh_sound = '/Users/Archie/Documents/Python Projects/CatanNoTurns/OhYehSound.mp3'

rolling = None  # To store the scheduled task ID

players = ["Harris", "Archie"]
def roll_dice():
    global rolling
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    result_label_1.config(text=f"{total}")

    subprocess.Popen(['afplay', dice_roll_sound])

    if total == 7:
        robber_label.config(text=f"Robber is {random.choice(players)}")
        subprocess.Popen(['afplay', oh_yeh_sound])
    else:
        robber_label.config(text="")


    # Schedule the next roll after 60 seconds (60000 ms)
    rolling = root.after(15000, roll_dice)

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

# Start button
start_button = tk.Button(root, text="Start", command=start_rolling, font=("Arial", 14), highlightbackground=background_colour)
start_button.pack(side="left", padx=100, pady=50)

# Bind spacebar to start rolling
root.bind('<space>', lambda event: start_rolling())

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_rolling, font=("Arial", 14), highlightbackground=background_colour)
stop_button.pack(side="right", padx=100, pady=50)

# Bind spacebar to stop rolling
root.bind('<Return>', lambda event: stop_rolling())

# Start the main loop
root.mainloop()
