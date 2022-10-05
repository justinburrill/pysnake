from tkinter import *
import random
# Initialize window
root = Tk()
screensize = 15 # odd number works nicely, >= 5
squaresize = 50 # pixel size of each square
root.geometry(f"{screensize*squaresize}x{screensize*squaresize}")
root.title("snake lol")
# Create canvas
_canvas = Canvas(root, height=screensize*squaresize,
                 width=screensize*squaresize)
_canvas.pack()


snake = []  # list of [x,y] for snake body parts
moveQueue = []  # so when multiple inputs are pressed quickly, they can queue up


class Globe():
    def __init__(self):
        self.death = False
        self.frozen = True
        self.snakeLength = 1
        self.screenUpdateDelay = 400
        self.apple = []  # x, y for the apple
        self.lastmove = [0, 0]



globe = Globe()


def popSnake():
    # get of end of snake when moving to the next spot
    snake.pop(0)


def controlSnake(x, y):
    # print(f"input {x}, {y}")
    
    if len(moveQueue) < 3:
        moveQueue.append([x, y])
        print("moveQueue:\n" + str(moveQueue))
        # print(f"Moving {[x, y]}")

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
    # print("snake:\n" + str(snake))
    x = move[0]
    y = move[1]
    # print(f"moving {x}, {y}")
    
    if globe.lastmove[0] + x == 0 and globe.lastmove[1] + y == 0:
        # can't do a 180
        # print("180 turn blocked")
        x = -1
        y = -1

    if [x,y] != [-1,-1]: # new move
        globe.lastmove[0] = x
        # print(f"globe.lastmove x = {x}")
        globe.lastmove[1] = y
        # print(f"globe.lastmove y = {y}")
        x = snake[-1][0] + x
        y = snake[-1][1] + y
    else: # lastmove
        x = snake[-1][0] + globe.lastmove[0]
        # print(f"x = {snake[-1][0]} + {globe.lastmove[0]}")
        y = snake[-1][1] + globe.lastmove[1]
        # print(f"y = {snake[-1][1]} + {globe.lastmove[1]}")

    # print(f"moving {x}, {y}")
    # Check if you hit a wall
    if x > screensize-1 or x < 0 or y > screensize-1 or y < 0:
        killSnake()
    else:
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
        snake.insert(0,snake[0]) 
        newApple()
        globe.snakeLength += 1
        # print(f"snakeLength: {globe.snakeLength}")


def loop():
    if (len(moveQueue) > 0):
        nextSnake(moveQueue[0])
        # Remove that move from the queue
        moveQueue.pop(-1)
    else:
        nextSnake([-1, -1])
    if globe.frozen or globe.death:
        return
    popSnake()
    detectApple()
    draw()
    root.after(globe.screenUpdateDelay, loop)


def killSnake():
    globe.death = True
    draw()
    root.after(3000, resetGame)

def rect(x, y, c):
    _canvas.create_rectangle(
                    50*x, 50*y, 50*(x+1), 50*(y+1), fill=c, outline=c)


def draw():
    # fill squares with red for apple, green for snake, and black for empty
    for x in range(screensize):
        for y in range(screensize):

            if [x, y] in snake:
                rect(x, y, "green")
                if [x, y] == snake[-1]: # head is a different colour
                    rect(x, y, "#00d500")  
                

            elif [x, y] == globe.apple:
                rect(x, y, "red")

            else:
                if globe.death:
                    # Red screen on death
                    rect(x, y, "red")
                    continue
                # _canvas.create_rectangle(
                #     50*x, 50*y, 50*(x+1), 50*(y+1), fill="black")
                rect(x,y,"black")

            


# starting spots
def resetGame():
    globe.death = False

    # Reset positions
    snake.clear()
    snake.append([1, int(screensize/2)])
    globe.apple = [screensize-2, int(screensize/2)]
    globe.lastmove = [0,0]

    globe.death = False
    globe.frozen = True
    draw()


# Set everything up
resetGame()

# Needs to be here for tkinter
root.mainloop()
