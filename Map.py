from random import randint
from tkinter import *
import random
from enum import Enum

class cellType(Enum):
    LAND = 0
    WATER_START = 1
    WATER = 2

class Cell():
    def __init__(self, master, x, y, size, cellType):
        """ Constructor of the object called by Cell(...) """
        self.master = master
        self.x = x
        self.y = y
        self.size= size
        self.cellType= cellType

    def getCellColor(self):

        color = 'white' # default color

        if self.cellType == cellType.LAND:
            color = 'green'
        elif self.cellType == cellType.WATER:
            color = 'blue'
        elif self.cellType == cellType.WATER_START:
            color = 'blue'

        return color

    def draw(self):
        """ order to the cell to draw its representation on the canvas """
        if self.master != None :
            xmin = self.x * self.size
            xmax = xmin + self.size
            ymin = self.y * self.size
            ymax = ymin + self.size

            color = self.getCellColor()

            # self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = fill, outline = outline)
            self.master.create_rectangle(xmin, ymin, xmax, ymax, fill = color, width = 0)

class CellGrid(Canvas):
    def __init__(self,master, rowNumber, columnNumber, cellSize, landPercent, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)
        
        self.cellSize = cellSize

        self.grid = []
        for column in range(columnNumber):

            line = []
            for row in range(rowNumber):
                cellType = self.chooseCellType(landPercent)
                line.append(Cell(self, column, row, cellSize, cellType))
            self.grid.append(line)

        self.createWater()

        self.draw()


    def chooseCellType(self, landPercent):
        """
        Description
        -------------
        Generate a random value between 0 and 999. Then use ranges of these values to determine the color of to return based off
        the percentage of land to water that you would like.

        Params
        --------
        landPercent - A float value between 0.00 and 100.00 that represents the percentage of land you would like on the map
        """
        percent = landPercent * 10 * 10
        if randint(0, 9999) < percent:
            return cellType.LAND
        else:
            return cellType.WATER_START

    def createWater(self):
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.WATER_START:
                    self.infectCells(54, cell.x, cell.y, cellType.WATER)

    def infectCells(self, infectionRate, x, y, cellTypeIn):
        self.infectCell(infectionRate, x, y-1,cellTypeIn) # UP
        self.infectCell(infectionRate, x, y+1,cellTypeIn) # DOWN
        self.infectCell(infectionRate, x-1, y,cellTypeIn) # LEFT
        self.infectCell(infectionRate, x+1, y,cellTypeIn) # RIGHT
    
    def infectCell(self, infectionRate, x, y, cellTypeIn):
        if y < numRows -1 and y > 0 and x < numColumns -1 and x > 0:
            randValue = randint(0,99)
            if randValue < infectionRate and self.grid[x][y].cellType != cellTypeIn and self.grid[x][y].cellType != cellType.WATER_START:
                self.grid[x][y].cellType = cellTypeIn
                self.infectCells(infectionRate - 1, x, y, cellTypeIn)

    def draw(self):
        for column in self.grid:
            for cell in column:
                cell.draw()


pixelsPerCell = 5
numColumns = int(1890/pixelsPerCell) #Number of Columns directly coorelates to the x position of the grid
numRows = int(1000/pixelsPerCell) #Number of Columns directly coorelates to the y position of the grid


if __name__ == "__main__" :
    app = Tk()

    grid = CellGrid(app, numRows, numColumns, pixelsPerCell, 99.00)
    grid.pack()

    app.mainloop()