from tkinter import *
import random
# Initialize window
root = Tk()

WINRES = [1440, 900]
winwidth = WINRES[0]
winheight = WINRES[1]

squarecountx = 17 # odd number works nicely, >= 5
squarecounty = 15 # odd number works nicely, >= 5
squarewidth = winwidth/squarecountx # pixel size of each square
squareheight = winheight/squarecounty

root.geometry(f"{winwidth}x{winheight}")
root.title("Snake")
# Create canvas
_canvas = Canvas(root, height=squarecounty*squareheight,
                 width=squarecountx*squarewidth)
_canvas.pack()




class Globe():
    def __init__(self):
        self.snake = []  # list of [x,y] for snake body parts
        self.moveQueue = []  # so when multiple inputs are pressed quickly, they can queue up
        self.death = False
        self.frozen = True
        self.snakeLength = 1
        self.screenUpdateDelay = 300
        self.moveQueueLength = 2
        self.apple = []  # x, y for the apple
        self.lastmove = [0, 0]


globe = Globe()


def popSnake():
    # get of end of globe.snake when moving to the next spot
    globe.snake.pop(0)


def controlSnake(x, y):
    # print(f"input {x}, {y}")
    
    if len(globe.moveQueue) < globe.moveQueueLength:
        globe.moveQueue.append([x, y])
        # print("moveQueue:\n" + str(moveQueue))
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

def checkImpact(x, y):
    # Check if you hit a wall
    if x > squarecountx-1 or x < 0 or y > squarecounty-1 or y < 0:
        return True
    elif [x,y] in globe.snake:
        return True
    else: return False



def nextSnake(move):
    print(f"snake:\n{globe.snake}")
    x = move[0]
    y = move[1]
    print(f"moving {x}, {y}")
    
    if globe.lastmove[0] + x == 0 and globe.lastmove[1] + y == 0:
        # can't do a 180
        # print("180 turn blocked")
        # if globe.moveQueue[0]
            x = -1
            y = -1


    if [x,y] != [-1,-1]: # new move
        globe.lastmove[0] = x
        # print(f"globe.lastmove x = {x}")
        globe.lastmove[1] = y
        # print(f"globe.lastmove y = {y}")
        x = globe.snake[-1][0] + x
        y = globe.snake[-1][1] + y
    else: # lastmove
        x = globe.snake[-1][0] + globe.lastmove[0]
        # print(f"x = {snake[-1][0]} + {globe.lastmove[0]}")
        y = globe.snake[-1][1] + globe.lastmove[1]
        # print(f"y = {snake[-1][1]} + {globe.lastmove[1]}")

    # print(f"moving {x}, {y}")
    
    if checkImpact(x, y):
        # dead 💀
        # print(f"impact: movex:{x} movey:{y}")
        killSnake()
    else:
        # make next body part of snake
        globe.snake.append([x, y])



def newApple():
    # get a new  spot for the apple
    x = random.randrange(0, 8)
    y = random.randrange(0, 8)
    if [x, y] in globe.snake:
        newApple()
    else:
        globe.apple = [x, y]


def detectApple():
    if globe.apple == globe.snake[-1]:
        globe.snake.insert(0, globe.snake[0]) 
        newApple()
        globe.snakeLength += 1
        # print(f"snakeLength: {globe.snakeLength}")


def loop():
    print(f"moveQueue:\n{str(globe.moveQueue)}")

    if (len(globe.moveQueue) > 0):
        nextSnake(globe.moveQueue[0])
        # Remove that move from the queue
        globe.moveQueue.pop(0)
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
                    squarewidth*x, squareheight*y, squarewidth*(x+1), squareheight*(y+1), fill=c, outline=c)


def draw():
    # if globe.death:

    # fill squares with red for apple, green for snake, and black for empty
    for x in range(squarecountx):
        for y in range(squarecounty):

            if [x, y] in globe.snake:
                rect(x, y, "green")
                if [x, y] == globe.snake[-1]: # head is a different colour
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
    globe.snake.clear()
    globe.moveQueue.clear()
    globe.snake.append([1, int(squarecounty/2)])
    globe.apple = [squarecountx-2, int(squarecounty/2)]
    globe.lastmove = [0,0]

    globe.death = False
    globe.frozen = True
    draw()


# Set everything up
resetGame()

# Needs to be here for tkinter
root.mainloop()
