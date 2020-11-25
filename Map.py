from random import randint
from tkinter import *
import math
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
    RIVER_WATER = 9
    LAND1 = 10
    LAND2 = 11
    LAND3 = 12
    LAND4 = 13
    LAND5 = 14
    RIVER_BANK = 15

class Biomes(Enum):
    PLAINS = 0
    DESERT = 1
    FOREST = 2
    JUNGLE = 3
    MOUNTAINS = 4
    TAIGA = 5
    TUNDRA = 6
    SWAMP = 7
    OCEAN = 8

class Directions(Enum):
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    DOWN_RIGHT = 3
    DOWN = 4
    DOWN_LEFT = 5
    LEFT = 6
    UP_LEFT = 7
    
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
        elif self.cellType == cellType.RIVER_HEAD:
            color = 'DodgerBlue4'
        elif self.cellType == cellType.RIVER_WATER:
            color = 'RoyalBlue4'
        elif self.cellType == cellType.LAND1:
            color = 'forest green'
        elif self.cellType == cellType.LAND2:
            color = 'olive drab'
        elif self.cellType == cellType.LAND3:
            color = 'burlywood4'
        elif self.cellType == cellType.LAND4:
            color = '#9E805B'
        elif self.cellType == cellType.LAND5:
            color = '#AD9270'
        elif self.cellType == cellType.RIVER_BANK:
            color = 'chartreuse4'

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
    def __init__(self,master, rowNumber, columnNumber, cellSize, infectionRate, Biome, *args, **kwargs):
        Canvas.__init__(self, master, width = cellSize * columnNumber , height = cellSize * rowNumber, *args, **kwargs)
        
        self.cellSize = cellSize
        self.Biome = Biome
        self.grid = []
        for column in range(columnNumber):

            line = []
            for row in range(rowNumber):
                cellType = self.chooseBaseCellTypes(Biome)
                line.append(Cell(self, column, row, cellSize, cellType))
            self.grid.append(line)

        self.createWater(infectionRate)

        self.draw()


    def chooseBaseCellTypes(self, Biome):
        """
        Description
        -------------
        Generate a random value between 0 and 999. Then use ranges of these values to determine the color of to return based off
        the percentage of land to water that you would like.

        Params
        --------
        landPercent - A float value between 0.00 and 100.00 that represents the percentage of land you would like on the map
        """
        numCells = numColumns * numRows
        if Biome == Biomes.PLAINS:
            landPercent = 1000 * 99.98 #99.984
            randomValue = randint(0, 99999)
            if randomValue < landPercent:
                return cellType.LAND
            else:
                return cellType.WATER_START


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
                    self.infectCells(infectionRate, cell.x, cell.y, cellType.WATER, (cellType.LAND,))

        # Fill in single-cells of land
        self.generateCells(1, 4, '>', (cellType.LAND,), (cellType.WATER,), cellType.WATER)

        # Fill in single-cells of water
        self.generateCells(1, 2, '<', (cellType.WATER,), (cellType.WATER,), cellType.LAND)

        # Generate deep water 0
        rad0 = 2
        self.generateCells(rad0, rad0*8, '=', (cellType.WATER,), (cellType.WATER,cellType.DEEP_WATER0), cellType.DEEP_WATER0)

        # Generate deep water 1
        rad0 = 2
        self.generateCells(rad0, rad0*8, '=', (cellType.DEEP_WATER0,), (cellType.DEEP_WATER0,cellType.DEEP_WATER1), cellType.DEEP_WATER1)

        # Generate deep water 2
        rad0 = 3
        self.generateCells(rad0, rad0*8, '=', (cellType.DEEP_WATER1,), (cellType.DEEP_WATER1,cellType.DEEP_WATER2), cellType.DEEP_WATER2)

        # Generate deep water 3 
        rad0 = 3
        self.generateCells(rad0, rad0*8, '=', (cellType.DEEP_WATER2,), (cellType.DEEP_WATER2,cellType.DEEP_WATER3), cellType.DEEP_WATER3)

        # TEST round off corners of deep water 3
        self.generateCells(1, 4, '>', (cellType.DEEP_WATER3,), (cellType.DEEP_WATER2,), cellType.DEEP_WATER2)

        # Generate sand on land that touches water
        self.generateCells(1, 0, '>', (cellType.LAND,), (cellType.WATER,), cellType.SAND)

        # Generate rivers

        # amountOfSand = 0
        # for column in self.grid:
        #     for cell in column:
        #         if cell.cellType == cellType.SAND:
        #             amountOfSand += 1
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.SAND:
                    surroundingCells = self.getSurroundingCellsInfo(cell.x,cell.y,1)
                    sandCount = 0
                    waterCount = 0
                    for i in surroundingCells:
                        if i.cellType == cellType.SAND:
                            sandCount += 1
                        elif i.cellType == cellType.WATER:
                            waterCount += 1
                    if sandCount < 4 and waterCount > 0 and randint(0,10000) > 9950:
                    #if randint(0,10000) > 9950:
                        cell.cellType = cellType.RIVER_HEAD
                        surroundingCells = self.getSurroundingCellsInfo(cell.x, cell.y, 1)
                        direction = self.getDirection(surroundingCells, cell.x, cell.y)
                        distance = randint(5,10)
                        maxRiverLen = randint(5,10)
                        self.createRiver(cell.x, cell.y, direction, distance, maxRiverLen)

        # Make rivers thick again
    #    for column in self.grid:
    #        for cell in column:
    #            if cell.cellType == cellType.RIVER_WATER:
    #                self.infectCells(10,cell.x,cell.y,cellType.RIVER_WATER,(cellType.LAND,))

        # Generate banks around rivers
        self.generateCells(1, 0, '>', (cellType.LAND,), (cellType.RIVER_WATER,cellType.RIVER_HEAD,), cellType.RIVER_BANK)

        # Generate areas of differently-colored land -------------------------

        #LAND1
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND:
                    if randint(0, 10000) > 9950:
                        self.cellType = cellType.LAND1
                        self.infectCells(40, cell.x, cell.y, cellType.LAND1, (cellType.LAND,))

        #LAND2
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND or cell.cellType == cellType.LAND1:
                    if randint(0, 10000) > 9950:
                        self.cellType = cellType.LAND2
                        self.infectCells(30, cell.x, cell.y, cellType.LAND2, (cellType.LAND,cellType.LAND1))

        #LAND3 (cliffs) (low spawn rate, but high infection rate)
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND or cell.cellType == cellType.LAND1 or cell.cellType == cellType.LAND2:
                    if randint(0, 10000) > 9995:
                        self.cellType = cellType.LAND3
                        self.infectCells(50, cell.x, cell.y, cellType.LAND3, (cellType.LAND,cellType.LAND1,cellType.LAND2))

        # Generate specific land around cliffs
        self.generateCells(1, 0, '>', (cellType.LAND,cellType.LAND1,cellType.LAND2,), (cellType.LAND3,), cellType.LAND)

        # Create cliff peaks
        rad0 = 3
        self.generateCells(rad0, rad0*8, '=', (cellType.LAND3,), (cellType.LAND3,), cellType.LAND5)

        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND5:
                    #if randint(0, 10000) > 9500:
                    self.infectCells(10, cell.x, cell.y, cellType.LAND5, (cellType.LAND3,))

        #LAND4 (cliffs, higher elevation)
    #    rad0 = 1
    #    self.generateCells(rad0, rad0*8, '=', (cellType.LAND3,), (cellType.LAND3,cellType.LAND4,), cellType.LAND4)

        #LAND5 (cliffs, even higher elevation)
    #    rad0 = 2
    #    self.generateCells(rad0, rad0*8, '=', (cellType.LAND4,), (cellType.LAND4,cellType.LAND5), cellType.LAND5)

        # Fill in single-cells of land between cliffs
        self.generateCells(1, 4, '>', (cellType.LAND,cellType.LAND1,cellType.LAND2,), (cellType.LAND3,), cellType.LAND3)
#
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND3:
                    if randint(0, 10000) > 9800:
                        self.cellType = cellType.LAND5
                        self.infectCells(40, cell.x, cell.y, cellType.LAND4, (cellType.LAND3,))
#
    #    #LAND5 (cliffs, different color) (low spawn rate, but high infection rate)
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND4:
                    if randint(0, 10000) > 9800:
                        self.cellType = cellType.LAND5
                        self.infectCells(40, cell.x, cell.y, cellType.LAND5, (cellType.LAND4,))


        # --------------------------------------------------------------------


    def generateCells(self, rad, threshold, thresholdOperator, currentCellTypes, cellTypeConditional, newCellType):
        for column in self.grid:
            for cell in column:
                if cell.cellType in currentCellTypes:
                    surroundingTypeCount = 0
                    surroundingCells = self.getSurroundingCellsInfo(cell.x, cell.y, rad)
                    for i in surroundingCells:
                        if i.cellType in cellTypeConditional:
                            surroundingTypeCount += 1

                    # Check threshold operator and check if threshold met, then apply newCellType if it is
                    if thresholdOperator == '=' and surroundingTypeCount == threshold:
                        cell.cellType = newCellType
                    elif thresholdOperator == '>' and surroundingTypeCount > threshold:
                        cell.cellType = newCellType
                    elif thresholdOperator == '<' and surroundingTypeCount < threshold:
                        cell.cellType = newCellType

    def infectCells(self, infectionRate, x, y, cellTypeIn, cellTypeToReplace):
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
        self.infectCell(infectionRate, x, y-1,cellTypeIn,cellTypeToReplace) # UP
        self.infectCell(infectionRate, x-1, y-1,cellTypeIn,cellTypeToReplace) # UP LEFT
        self.infectCell(infectionRate, x+1, y-1,cellTypeIn,cellTypeToReplace) # UP RIGHT
        self.infectCell(infectionRate, x, y+1,cellTypeIn,cellTypeToReplace) # DOWN
        self.infectCell(infectionRate, x-1, y+1,cellTypeIn,cellTypeToReplace) # DOWN LEFT
        self.infectCell(infectionRate, x+1, y+1,cellTypeIn,cellTypeToReplace) # DOWN RIGHT
        self.infectCell(infectionRate, x-1, y,cellTypeIn,cellTypeToReplace) # LEFT
        self.infectCell(infectionRate, x+1, y,cellTypeIn,cellTypeToReplace) # RIGHT
    
    def infectCell(self, infectionRate, x, y, cellTypeIn, cellTypeToReplace):
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
            if self.grid[x][y].cellType in cellTypeToReplace:
                randValue = randint(0,99)
                if randValue < infectionRate and self.grid[x][y].cellType != cellTypeIn and self.grid[x][y].cellType != cellType.WATER_START:
                    self.grid[x][y].cellType = cellTypeIn
                    self.infectCells(infectionRate - 1, x, y, cellTypeIn, cellTypeToReplace)

    def getSurroundingCellsInfo(self, x, y, radius):
        """
        Description
        -----------
        This function returns a list that contains the cell types and locations of the surrounding cells
        
        Params
        --------
        x - x coordinate of the infecting cell
        y - y coordinate of the infecting cell
        radius - distance (in number of cells from the center cell) to check
        """
        surroundingCellList = []
        for i in range(1 , radius + 1):
            if y-i >= 0:
                surroundingCellList.append(self.grid[x][y-i]) #UP
            if x < numColumns - i and y-i >= 0:
                surroundingCellList.append(self.grid[x+i][y-i]) #UP RIGHT
            if x < numColumns - i:
                surroundingCellList.append(self.grid[x+i][y]) #RIGHT
            if x < numColumns - i and y < numRows - i:
                surroundingCellList.append(self.grid[x+i][y+i]) #DOWN RIGHT
            if y < numRows - i:
                surroundingCellList.append(self.grid[x][y+i]) #DOWN
            if x-i >= 0 and y < numRows - i:
                surroundingCellList.append(self.grid[x-i][y+i]) #DOWN LEFT
            if x-i >= 0:
                surroundingCellList.append(self.grid[x-i][y]) #LEFT
            if x-i >= 0 and y-i >= 0:
                surroundingCellList.append(self.grid[x-i][y-i]) #UP LEFT

        return surroundingCellList # returns a list of the surrounding cells' cellTypes
    
    def getDirection(self, surroundingCellList, x, y):
        waterCount = 0                                  # Find "center" of surrounding water tiles
        for cell in surroundingCellList:
            if cell.cellType == cellType.SAND:
                cell.cellType = cellType.RIVER_WATER
            if cell.cellType == cellType.WATER:
                waterCount +=1
        waterIndex = math.ceil(waterCount/2)
        for cell in surroundingCellList:
            if cell.cellType == cellType.WATER:
                waterIndex -= 1
            if waterIndex == 0:
                direction = surroundingCellList.index(cell)
                direction = (direction + 4) % 8         # Find opposite direction from chosen cell
                return direction

    def getDirectionCoordinates(self, direction):
        xOff = 0
        yOff = 0

        if direction == Directions.UP.value:
            xOff = 0
            yOff = -1
        elif direction == Directions.UP_RIGHT.value:
            xOff = 1
            yOff = -1
        elif direction == Directions.RIGHT.value:
            xOff = 1
            yOff = 0
        elif direction == Directions.DOWN_RIGHT.value:
            xOff = 1
            yOff = 1
        elif direction == Directions.DOWN.value:
            xOff = 0
            yOff = 1
        elif direction == Directions.DOWN_LEFT.value:
            xOff = -1
            yOff = 1
        elif direction == Directions.LEFT.value:
            xOff = -1
            yOff = 0
        elif direction == Directions.UP_LEFT.value:
            xOff = -1
            yOff = -1

        # print(str(xOff)+", "+str(yOff))

        return [xOff,yOff]

    def checkIfWater(self, cell):
        if cell.cellType == cellType.WATER or cell.cellType == cellType.DEEP_WATER0 or cell.cellType == cellType.DEEP_WATER1 or cell.cellType == cellType.DEEP_WATER2 or cell.cellType == cellType.DEEP_WATER3:
            return TRUE
        else:
            return FALSE

    def createRiver(self, x , y, direction, distance, counter):

        if counter <= 0:
            return

        # New coords for next line

        offsets = self.getDirectionCoordinates(direction)

        xNew = x+offsets[0]*distance
        yNew = y+offsets[1]*distance

        for i in range(distance):
            if (
    #            (direction == Directions.UP.value and y > 0)
    #            or (direction == Directions.UP_RIGHT.value and x < numColumns - i and y > 0)
    #            or (direction == Directions.RIGHT.value and x < numColumns - i)
    #            or (direction == Directions.DOWN_RIGHT.value and x < numColumns - i and y < numRows - i)
    #            or (direction == Directions.DOWN.value and y < numRows - i)
    #            or (direction == Directions.DOWN_LEFT.value and x > 0 and y < numRows - i)
    #            or (direction == Directions.LEFT.value and x > 0)
    #            or (direction == Directions.UP_LEFT.value and x > 0 and y > 0)

                (x+i*offsets[0]) in range(0, len(self.grid))
                and (y+i*offsets[1]) in range(0, len(self.grid[0]))
            ):
                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
                        self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER

    #    if direction == Directions.UP.value:
    #        for i in range(distance):
    #            if y > 0:
    #                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
    #                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER
    ##        xNew = x
    # #       yNew = y-distance
#
    #    elif direction == Directions.UP_RIGHT.value:
    #        for i in range(distance):
    #            if x < numColumns - i and y > 0:
    #                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
    #                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER
    #  #      xNew = x+distance
    #   #     yNew = y-distance
#
    #    elif direction == Directions.RIGHT.value:
    #        for i in range(distance):
    #            if x < numColumns - i:
    #                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
    #                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER
    ##        xNew = x+distance
    # #       yNew = y
#
    #    elif direction == Directions.DOWN_RIGHT.value:
    #        for i in range(distance):
    #            if x < numColumns - i and y < numRows - i:
    #                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
    #                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER
    #  #      xNew = x+distance
    #   #     yNew = y+distance
#
    #    elif direction == Directions.DOWN.value:
    #        for i in range(distance):
    #            if y < numRows - i:
    #                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
    #                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER
    ##        xNew = x
    # #       yNew = y+distance
#
    #    elif direction == Directions.DOWN_LEFT.value:
    #        for i in range(distance):
    #            if x > 0 and y < numRows - i:
    #                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
    #                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER
    #  #      xNew = x-distance
    #   #     yNew = y+distance
#
    #    elif direction == Directions.LEFT.value:
    #        for i in range(distance):
    #            if x > 0:
    #                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
    #                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER
    ##        xNew = x-distance
    # #       yNew = y
#
    #    elif direction == Directions.UP_LEFT.value:
    #        for i in range(distance):
    #            if x > 0 and y > 0:
    #                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
    #                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER
      #      xNew = x-distance
       #     yNew = y-distance

        # Repeat with new line

        if not ((xNew) in range(0, len(self.grid)) and (yNew) in range(0, len(self.grid[0]))):
            return

        surroundingEndList = self.getSurroundingCellsInfo(xNew,yNew,1)
        for cell in surroundingEndList:
            if cell.cellType == cellType.WATER:
                return

        if randint(0,100) > 10:
            distanceNew = randint(2,5)
            dirChooser = randint(0,2)

            directionNew = (direction+1) % 8

            if dirChooser == 1:
                directionNew = (direction-1) % 8

            self.createRiver(xNew , yNew, directionNew, distanceNew,counter-1)

            if randint(0,100) > 70:  #fork
                self.createRiver(xNew , yNew, directionNew, distanceNew,counter-1)

    def draw(self):
        for column in self.grid:
            for cell in column:
                cell.draw()


pixelsPerCell = 5
numColumns = int(1280/pixelsPerCell) #Number of Columns directly coorelates to the x position of the grid
numRows = int(720/pixelsPerCell) #Number of Columns directly coorelates to the y position of the grid
infectionRate = randint(90, 100)

if __name__ == "__main__" :
    app = Tk()

    grid = CellGrid(app, numRows, numColumns, pixelsPerCell, infectionRate, Biomes.PLAINS)
    grid.pack()

    app.mainloop()