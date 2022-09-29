from tkinter import *
import random
# Initialize window
root = Tk()
screensize = 9
squaresize = 50
root.geometry(f"{screensize*squaresize}x{screensize*squaresize}")
root.title("snake lol")
# Create canvas
_canvas = Canvas(root, height=screensize*squaresize,
                 width=screensize*squaresize)
_canvas.pack()


snake = []  # list of [x,y] for snake body parts
moveQueue = []  # so when multiple inputs are pressed quickly, they can queue up
lastmove = [1, 0]


class Globe():
    def __init__(self):
        self.death = False
        self.frozen = True
        self.snakeLength = 1
        self.screenUpdateDelay = 400
        self.apple = []  # x, y for the apple


globe = Globe()


def popSnake():
    # get of end of snake when moving to the next spot
    snake.pop(0)


def controlSnake(x, y):

    if len(moveQueue) < 3:
        moveQueue.append([x, y])

    if (globe.frozen):
        globe.frozen = False
        loop()


# Controls
root.bind("<Up>", lambda event, x=0, y=-1:
          controlSnake(x, y))
root.bind("<Down>", lambda event, x=0, y=1:
          controlSnake(x, y))
root.bind("<Left>", lambda event, x=-1, y=0:
          controlSnake(x, y))
root.bind("<Right>", lambda event, x=1, y=0:
          controlSnake(x, y))


def nextSnake(move):
    # Remove that move from the queue

    x = move[0]
    y = move[1]

    if x > -1:
        x = snake[-1][0] + x
        y = snake[-1][1] + y
        lastmove[0] = x
        lastmove[1] = y
    else:
        x = snake[-1][0] + lastmove[0]
        y = snake[-1][1] + lastmove[1]

    # Check if you hit a wall
    if x > 8 or x < 0 or y > 8 or y < 0:
        killSnake()

    # make next body part of snake
    snake.append([x, y])


def newApple():
    # get a new random spot for the apple
    x = random.randrange(0, 8)
    y = random.randrange(0, 8)
    if [x, y] in snake:
        newApple()
    else:
        globe.apple = [x, y]


def detectApple():
    if globe.apple == snake[-1]:
        newApple()
        globe.snakeLength += 1


def loop():
    if (len(moveQueue) > 0):
        nextSnake(moveQueue[0])
        moveQueue.pop(-1)
    else:
        nextSnake([-1, -1])
    popSnake()
    detectApple()
    draw()
    if not globe.frozen:
        root.after(globe.screenUpdateDelay, loop)


def killSnake():
    globe.death = True

    root.after(3000, resetGame)


def draw():
    # fill squares with red for apple, green for snake, and black for empty
    for x in range(9):
        for y in range(9):

            if [x, y] in snake:
                _canvas.create_rectangle(
                    50*x, 50*y, 50*(x+1), 50*(y+1), fill="green", outline="green")

            elif [x, y] == globe.apple:
                _canvas.create_rectangle(
                    50*x, 50*y, 50*(x+1), 50*(y+1), fill="red", outline="red")

            else:
                if globe.death:
                    # Red screen on death
                    _canvas.create_rectangle(
                        50*x, 50*y, 50*(x+1), 50*(y+1), fill="red", outline="red")
                    continue
                _canvas.create_rectangle(
                    50*x, 50*y, 50*(x+1), 50*(y+1), fill="black")


# starting spots
def resetGame():
    globe.death = False

    # Reset positions
    snake.append([2, 4])
    globe.apple = [7, 4]

    globe.death = False
    globe.frozen = True
    draw()


# Set everything up
resetGame()

# Needs to be here for tkinter
root.mainloop()
