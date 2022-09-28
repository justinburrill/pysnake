from tkinter import *
import random
# Initialize window
root = Tk()
root.geometry('450x450')
# Create canvas
_canvas = Canvas(root, height=450, width=450)
_canvas.pack()

snake = []
snakeLength = 1
apple = []


def newApple():
    apple = [random.randrange(0, 8), random.randrange(0, 8)]


def updateScreen():
    for x in range(9):
        for y in range(9):
            if [x, y] in snake:
                _canvas.create_rectangle(
                    50*x, 50*y, 50*(x+1), 50*(y+1), fill="green")
            else:
                _canvas.create_rectangle(
                    50*x, 50*y, 50*(x+1), 50*(y+1), fill="black")


snake.append([2, 4])
newApple()
updateScreen()

root.mainloop()
