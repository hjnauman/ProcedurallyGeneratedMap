from random import randint
from tkinter import *
import random

class Cell():
    def __init__(self, master, x, y, size, color):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.abs = x
        self.ord = y
        self.size= size
        self.color= color


    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            xmin = self.abs * self.size
            xmax = xmin + self.size
            ymin = self.ord * self.size
            ymax = ymin + self.size

            # self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = self.color, outline = 'black')

class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)
        
        self.cellSize = cellSize

        self.grid = []
        for row in range(rowNumber):

            line = []
            for column in range(columnNumber):
                color = self.chooseColor(100)
                line.append(Cell(self, column, row, cellSize, color))

            self.grid.append(line)

        self.draw()


    def chooseColor(self, landPercent):
        """
        Descritpion
        -------------
        Generate a random value between 0 and 99. Then use ranges of these values to determine the color of to return based off
        the percentage of land to water that you would like.

        Params
        --------
        landPercent - An integer value between 0 and 100 that represents the percentage of land you would like on the map
        """
        if randint(0, 99) < landPercent:
            return 'green'
        else:
            return 'blue'


    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()


if __name__ == "__main__" :
    app = Tk()

    grid = CellGrid(app, 50, 50, 10)
    grid.pack()

    app.mainloop()