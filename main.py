# Creating a script to play Catan without turns and dice rolling
# Needs to randomly show a number 1-12 at specific time intervals

import tkinter as tk
import random
import subprocess


dice_roll_sound = '/Users/Archie/Documents/Python Projects/CatanNoTurns/DiceRollSound.mp3'

rolling = None  # To store the scheduled task ID

players = ["Harris", "Niven", "Archie"]
def roll_dice():
    global rolling
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    result_label_1.config(text=f"{total}")

    subprocess.run(['afplay', dice_roll_sound])

    if total == 7:
        robber_label.config(text=f"Robber is {random.choice(players)}")
    else:
        robber_label.config(text="")


    # Schedule the next roll after 60 seconds (60000 ms)
    rolling = root.after(10000, roll_dice)

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
root = tk.Tk()
root.title("Dice Roller")

# Label to display the result
result_label_1 = tk.Label(root, text="", font=("Arial", 300))
result_label_1.pack(pady=10)

robber_label = tk.Label(root, text="", font=("Arial", 100), fg="red")
robber_label.pack(pady=2)

# Start button
start_button = tk.Button(root, text="Start", command=start_rolling, font=("Arial", 14), highlightbackground='#00cc00')
start_button.pack(side="left", padx=100, pady=50)

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_rolling, font=("Arial", 14), highlightbackground='#cc0000')
stop_button.pack(side="right", padx=100, pady=50)

# Start the main loop
root.mainloop()
