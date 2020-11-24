from random import randint
from tkinter import *
import random
from enum import Enum

class cellType(Enum):
    LAND = 0
    WATER_START = 1
    WATER = 2
    DEEP_WATER0 = 3
    DEEP_WATER1 = 4
    DEEP_WATER2 = 5
    DEEP_WATER3 = 6
    SAND = 7
    RIVER_HEAD = 8

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
            color = '#0074D3'
        elif self.cellType == cellType.WATER_START:
            color = 'black'
        elif self.cellType == cellType.DEEP_WATER0:
            color = '#0B62E6'
        elif self.cellType == cellType.DEEP_WATER1:
            color = '#2059DA'
        elif self.cellType == cellType.DEEP_WATER2:
            color = '#2855B7'
        elif self.cellType == cellType.DEEP_WATER3:
            color = '#2E519B'
        elif self.cellType == cellType.SAND:
            color = 'tan'

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
    def __init__(self,master, rowNumber, columnNumber, cellSize, landPercent, infectionRate, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)
        
        self.cellSize = cellSize

        self.grid = []
        for column in range(columnNumber):

            line = []
            for row in range(rowNumber):
                cellType = self.chooseCellType(landPercent)
                line.append(Cell(self, column, row, cellSize, cellType))
            self.grid.append(line)

        self.createWater(infectionRate)

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
        randomValue = randint(0, 9999)
        if randomValue < percent:
            return cellType.LAND
        else:
            if randomValue % 2 == 0:
                return cellType.WATER_START
            else:
                return cellType.RIVER_HEAD

    def createWater(self, infectionRate):
        """
        Description
        -------------
        Create an infection of water cells from water start cells. Fill in small land islands.
        """
        # Create water infection from water start cells
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.WATER_START:
                    cell.cellType = cellType.WATER
                    self.infectCells(infectionRate, cell.x, cell.y, cellType.WATER)
                elif cell.cellType == cellType.RIVER_HEAD:
                    # cell.cellType = cellType.WATER
                    self.createRiver()

        # Fill in single-cells of land
        self.generateCells(1, 4, '>', cellType.LAND, (cellType.WATER,), cellType.WATER)

        # Fill in single-cells of water
        self.generateCells(1, 2, '<', cellType.WATER, (cellType.WATER,), cellType.LAND)

        # Generate deep water 0
        rad0 = 2
        self.generateCells(rad0, rad0*8, '=', cellType.WATER, (cellType.WATER,cellType.DEEP_WATER0), cellType.DEEP_WATER0)

        # Generate deep water 1
        rad0 = 2
        self.generateCells(rad0, rad0*8, '=', cellType.DEEP_WATER0, (cellType.DEEP_WATER0,cellType.DEEP_WATER1), cellType.DEEP_WATER1)

        # Generate deep water 2
        rad0 = 3
        self.generateCells(rad0, rad0*8, '=', cellType.DEEP_WATER1, (cellType.DEEP_WATER1,cellType.DEEP_WATER2), cellType.DEEP_WATER2)

        # Generate deep water 3 
        rad0 = 3
        self.generateCells(rad0, rad0*8, '=', cellType.DEEP_WATER2, (cellType.DEEP_WATER2,cellType.DEEP_WATER3), cellType.DEEP_WATER3)

        # TEST round off corners of deep water 3
        self.generateCells(1, 4, '>', cellType.DEEP_WATER3, (cellType.DEEP_WATER2,), cellType.DEEP_WATER2)

        # Generate sand on land that touches water
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND:
                    rad = 1
                    surroundingCells = self.getSurroundingCells(cell.x, cell.y, rad)
                    for i in surroundingCells:
                        if i == cellType.WATER:
                            cell.cellType = cellType.SAND
                            continue

    def generateCells(self, rad, threshold, thresholdOperator, currentCellType, cellTypeConditional, newCellType):
        for column in self.grid:
            for cell in column:
                if cell.cellType == currentCellType:
                    surroundingTypeCount = 0
                    surroundingCells = self.getSurroundingCells(cell.x, cell.y, rad)
                    for i in surroundingCells:
                        if i in cellTypeConditional:
                            surroundingTypeCount += 1

                    # Check threshold operator and check if threshold met, then apply newCellType if it is
                    if thresholdOperator == '=' and surroundingTypeCount == threshold:
                        cell.cellType = newCellType
                    if thresholdOperator == '>' and surroundingTypeCount > threshold:
                        cell.cellType = newCellType
                    if thresholdOperator == '<' and surroundingTypeCount < threshold:
                        cell.cellType = newCellType

    def infectCells(self, infectionRate, x, y, cellTypeIn):
        """
        Description
        -------------
        Infect surrounding cells (with a percent chance) with a particular cellType.

        Params
        --------
        infectionRate - Int (between 0 and 100?) that defines how likely any given cell is to be infected
        x - x coordinate of the infecting cell
        y - y coordinate of the infecting cell
        cellTypeIn - cellType that infected cells will change to
        """
        self.infectCell(infectionRate, x, y-1,cellTypeIn) # UP
        self.infectCell(infectionRate, x-1, y-1,cellTypeIn) # UP LEFT
        self.infectCell(infectionRate, x+1, y-1,cellTypeIn) # UP RIGHT
        self.infectCell(infectionRate, x, y+1,cellTypeIn) # DOWN
        self.infectCell(infectionRate, x-1, y+1,cellTypeIn) # DOWN LEFT
        self.infectCell(infectionRate, x+1, y+1,cellTypeIn) # DOWN RIGHT
        self.infectCell(infectionRate, x-1, y,cellTypeIn) # LEFT
        self.infectCell(infectionRate, x+1, y,cellTypeIn) # RIGHT
    
    def infectCell(self, infectionRate, x, y, cellTypeIn):
        """
        Description
        -------------
        Infect a single cell with a particular cellType.

        Params
        --------
        infectionRate - Int (between 0 and 100?) that defines how likely any given cell is to be infected
        x - x coordinate of the infecting cell
        y - y coordinate of the infecting cell
        cellTypeIn - cellType that infected cells will change to
        """
        if y < numRows -1 and y > 0 and x < numColumns -1 and x > 0: # Check whether given coordinates work for a cell in the grid
            randValue = randint(0,99)
            if randValue < infectionRate and self.grid[x][y].cellType != cellTypeIn and self.grid[x][y].cellType != cellType.WATER_START:
                self.grid[x][y].cellType = cellTypeIn
                self.infectCells(infectionRate - 1, x, y, cellTypeIn)

    def getSurroundingCells(self, x, y, radius):
        surroundingCellList = []
        for i in range(1 , radius + 1):
            if y > 0:
                surroundingCellList.append(self.grid[x][y-i].cellType) #UP
            if x > 0 and y > 0:
                surroundingCellList.append(self.grid[x-i][y-i].cellType) #UP LEFT
            if x < numColumns - i and y > 0:
                surroundingCellList.append(self.grid[x+i][y-i].cellType) #UP RIGHT
            if y < numRows - i:
                surroundingCellList.append(self.grid[x][y+i].cellType) #DOWN
            if x > 0 and y < numRows - i:
                surroundingCellList.append(self.grid[x-i][y+i].cellType) #DOWN LEFT
            if x < numColumns - i and y < numRows - i:
                surroundingCellList.append(self.grid[x+i][y+i].cellType) #DOWN RIGHT
            if x > 0:
                surroundingCellList.append(self.grid[x-i][y].cellType) #LEFT
            if x < numColumns - i:
                surroundingCellList.append(self.grid[x+i][y].cellType) #RIGHT

        return surroundingCellList # returns a list of the surrounding cells' cellTypes
    
    def createRiver(self, ):
        
        pass

    def draw(self):
        for column in self.grid:
            for cell in column:
                cell.draw()


pixelsPerCell = 2
numColumns = int(1890/pixelsPerCell) #Number of Columns directly coorelates to the x position of the grid
numRows = int(1000/pixelsPerCell) #Number of Columns directly coorelates to the y position of the grid
infectionRate = randint(90, 100)

if __name__ == "__main__" :
    app = Tk()

    grid = CellGrid(app, numRows, numColumns, pixelsPerCell, 99.98, infectionRate)
    grid.pack()

    app.mainloop()