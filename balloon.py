"""
A simple game that gives the user left and right control of a
hot-air balloon that has to avoid the quickly moving bullet BULLET_BILLs.
"""
# import nessicary modules
from random import randint as rint
from time import sleep
from math import sqrt
import tkinter as tk

# create the tk window
ROOT = tk.Tk()
# change the title of the window to 'balloon'
ROOT.title("Balloon")
# change the 'iconphoto' of the window
ROOT.tk.call("wm", "iconphoto", ROOT._w, tk.PhotoImage(file="balloon.gif"))


def get_coords(id_num):
    """
    get the coordinates of a sppecified tk canvas object
    """
    # get the coords
    pos = C.coords(id_num)
    # return the respective X and Y values
    return pos[0], pos[1]


def distance(id1, id2):
    """
    get the distance between two specified canvas objects
    """
    # get the coords
    id1x1, id1y1 = get_coords(id1)
    id2x2, id2y2 = get_coords(id2)
    # do the calculations and return the answer
    return sqrt((id1x1 - id2x2) ** 2 + (id1y1 - id2y2) ** 2)


def collision():
    """
    see if the player and the current bullet have collided.
    """
    # initalize the varible
    popped = False
    # if the distance between the player and the current bullet...
    if distance(PLAYER, BULLET_BILL) < 50:
        # ...then say the balloon is popped
        popped = True
    return popped


def move_balloon(event):
    """
    move the player`s hot-air balloon, and bounce off walls
    """
    # if the player presses the left arrow key...
    if event.keysym == "Left":
        # move the balloon to the left.
        C.move(PLAYER, -10, 0)
        # also, bounce off the left wall if the player hits it.
        play_x, _ = get_coords(PLAYER)
        if play_x < 50:
            C.move(PLAYER, 10, 0)

    # do the same thing for the right arrow key
    if event.keysym == "Right":
        C.move(PLAYER, 10, 0)
        player_x, _ = get_coords(PLAYER)
        if player_x > 450:
            C.move(PLAYER, -10, 0)


def update_score(score):
    """
    update the score text object.
    """
    C.itemconfig(SCORE_TXT, text=(str(score) + " POINTS"))


# create the canvas and pack it
C = tk.Canvas(ROOT, bg="lightblue", width=500, height=500)
C.pack()

# set the player`s original coords
COORDS = [50, 50]

# create the player
FILER = tk.PhotoImage(file="balloon.gif")
PLAYER = C.create_image(*COORDS, image=FILER)

# initalize the 'POINTS' varible
POINTS = 0

# create the score and countdown text objects
SCORE_TXT = C.create_text(250, 490, text=(str(POINTS) + " POINTS"), fill="green")
COUNT_TXT = C.create_text(250, 250, text="", fill="black", font=("Droid Sans", 40))

# create a count-down
for i in range(3, 0, -1):
    C.itemconfig(COUNT_TXT, text=str(i))
    ROOT.update()
    sleep(1)
# delete the count-down text, for it is not needed any more
C.delete(COUNT_TXT)

# put the main game loop into a try-except clause to catch any errors on game completion
try:
    # game loop
    while True:
        # if a key is pressed, see if it is a valid key, and if
        # so, move the balloon.
        C.bind_all("<Key>", move_balloon)
        # if tk is NOT able to get the coords of BULLET_BILL, he must not exist...
        try:
            get_coords(BULLET_BILL)
        # ...so create him!
        except NameError:
            FILE1 = tk.PhotoImage(file="bullet.gif")
            BULLET_BILL = C.create_image(rint(50, 450), 450, image=FILE1)
        except IndexError:
            FILE1 = tk.PhotoImage(file="bullet.gif")
            BULLET_BILL = C.create_image(rint(50, 450), 450, image=FILE1)
        # if BULLET_BILL exists...
        try:
            # ...move him...
            C.move(BULLET_BILL, 0, -6)
            # ...and check if he has gone off the screen...
            POS_X, POS_Y = get_coords(BULLET_BILL)
            if POS_Y < 1:
                # ...and if so, add one point to the player and delete BULLET_BILL.
                POINTS += 1
                C.delete(BULLET_BILL)
        except tk.TclError:
            pass

        # update the score text
        update_score(POINTS)
        # update the window to apply all the changes we`ve made.
        ROOT.update()

        # prevent an error if the bullet has just been deleted.
        try:
            # if the player collides with the current bullet:
            if collision():
                # display the appropriate message
                if POINTS < 5:
                    C.create_text(
                        250,
                        100,
                        text="You SUCK!",
                        font=("Droid Sans", 20),
                        fill="tomato",
                    )
                elif POINTS > 50:
                    C.create_text(
                        250,
                        100,
                        text="You're GOOD at this!",
                        font=("Droid Sans", 20),
                        fill="blue",
                    )

                # also, display the 'GAME OVER' text.
                C.create_text(
                    250, 200, text="GAME OVER", font=("Droid Sans", 40), fill="red"
                )
                # and with it, the final score
                C.create_text(
                    250,
                    250,
                    text="Final Points:",
                    font=("Droid Sans", 40),
                    fill="green",
                )
                C.create_text(
                    250, 300, text=str(POINTS), font=("Droid Sans", 40), fill="green"
                )

                # next, get the final coords of the player:
                POS_X2, POS_Y2 = get_coords(PLAYER)
                COORDS = [POS_X2, POS_Y2]
                # delete the player
                C.delete(PLAYER)

                # create the 'popped' image and place it in the spot the player was
                FILER2 = tk.PhotoImage(file="pow.gif")
                C.create_image(*COORDS, image=FILER2)
                # finally, break the game loop
                break
        except IndexError:
            pass

        # a small delay here so the bullets and player don't zoom across the screen.
        sleep(0.01)
except IndexError:
    pass

# a NON-ANIMATING main loop that lets the window (and the 'GAME OVER')
# contiue to show after the player has lost.
ROOT.mainloop()
