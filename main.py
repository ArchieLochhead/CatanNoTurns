# Creating a script to play Catan without turns and dice rolling
# Needs to randomly show a number 1-12 at specific time intervals

import random
import sched, time

def roll_dice(scheduler):
    # Rolls dice every 60 seconds.
    scheduler.enter(60, 1, roll_dice, (scheduler,))
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    two_dice = dice1 + dice2
    print(two_dice)

    if two_dice == 7:
        print("ROBBER")

my_scheduler = sched.scheduler(time.time, time.sleep)
my_scheduler.enter(60, 1, roll_dice, (my_scheduler,))
my_scheduler.run()


