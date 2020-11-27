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
    RIVER_WATER1 = 9
    LAND1 = 10
    LAND2 = 11
    LAND3 = 12
    LAND4 = 13
    LAND5 = 14
    RIVER_BANK = 15
    RIVER_WATER2 = 16
    RIVER_WATER3 = 17
    TREE0 = 18
    TOWN = 19
    ROAD_DIRT = 20
    BRIDGE_WOOD = 21
    CONNECTED_TOWN = 22

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
        elif self.cellType == cellType.RIVER_WATER1:
            color = '#0074D3' #'red' #'#0074D3'
            # color = 'RoyalBlue4'
        elif self.cellType == cellType.RIVER_WATER2:
            color = '#0077E2'#'salmon' #'#0074D3'
        elif self.cellType == cellType.RIVER_WATER3:
            color = '#027EDE'#'light pink' #'#0074D3'
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
            color = '#346B23'#'chartreuse4'
        elif self.cellType == cellType.TREE0:
            color = 'dark green'
        elif self.cellType == cellType.TOWN:
            color = 'black'#'white'
        elif self.cellType == cellType.ROAD_DIRT:
            color = 'saddle brown'
        elif self.cellType == cellType.BRIDGE_WOOD:
            color = 'dark goldenrod'

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
            #self.master.create_oval(xmin-10, ymin-10, xmax+10, ymax+10, fill = color, width = 0)

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
        self.createLandDiversity(infectionRate)

        self.closestTownList = []

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

        # Expand sand areas
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.SAND:
                    if randint(0, 100) > 50:
                        self.infectCells(10, cell.x, cell.y, cellType.SAND, (cellType.LAND,))
                #    if randint(0, 10000) > 9900:
                #        self.infectCells(30, cell.x, cell.y, cellType.SAND, (cellType.LAND,cellType.SAND))

        # Generate rivers
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
                    if sandCount < 4 and waterCount > 0 and randint(0,10000) > 9900:
                    #if randint(0,10000) > 9950:
                        cell.cellType = cellType.RIVER_HEAD
                        surroundingCells = self.getSurroundingCellsInfo(cell.x, cell.y, 1)
                        direction = self.getDirection(surroundingCells, cell.x, cell.y)
                        distance = randint(2,3)
                        maxRiverLen = randint(20,40)
                        self.createRiver(cell.x, cell.y, direction, distance, maxRiverLen,maxRiverLen,0)

        # Make rivers thick again
    #    for column in self.grid:
    #        for cell in column:
    #            if cell.cellType == cellType.RIVER_WATER1:
    #                self.infectCells(10,cell.x,cell.y,cellType.RIVER_WATER1,(cellType.LAND,))

        # Generate thicker rivers
        self.generateCells(1, 0, '>', (cellType.LAND,), (cellType.RIVER_WATER1,cellType.RIVER_HEAD,), cellType.RIVER_BANK)

        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.RIVER_BANK:
                    cell.cellType = cellType.RIVER_WATER2

        self.generateCells(1, 0, '>', (cellType.LAND,), (cellType.RIVER_WATER2,), cellType.RIVER_BANK)

        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.RIVER_BANK:
                    cell.cellType = cellType.RIVER_WATER3

        # Generate banks around rivers
        self.generateCells(1, 0, '>', (cellType.LAND,), (cellType.RIVER_WATER1,cellType.RIVER_WATER2,cellType.RIVER_WATER3,cellType.RIVER_HEAD,), cellType.RIVER_BANK)

        #turn sand connected to river water into river water
        self.generateCells(1, 0, '>', (cellType.SAND,), (cellType.RIVER_WATER1,cellType.RIVER_WATER2,cellType.RIVER_WATER3,cellType.RIVER_HEAD,), cellType.LAND1)
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND1:
                    cell.cellType = cellType.RIVER_WATER3

    def createLandDiversity(self, infectionRate):
        # Generate areas of differently-colored land 
        #LAND1
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND:
                    if randint(0, 10000) > 9950:
                        cell.cellType = cellType.LAND1
                        self.infectCells(40, cell.x, cell.y, cellType.LAND1, (cellType.LAND,))

        #LAND2
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND or cell.cellType == cellType.LAND1:
                    if randint(0, 10000) > 9950:
                        cell.cellType = cellType.LAND2
                        self.infectCells(30, cell.x, cell.y, cellType.LAND2, (cellType.LAND,cellType.LAND1))

        #TREE0
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND or cell.cellType == cellType.LAND1 or cell.cellType == cellType.LAND2:
                    if randint(0, 10000) > 9995:
                        cell.cellType = cellType.TREE0
                        self.infectCells(50, cell.x, cell.y, cellType.TREE0, (cellType.LAND,cellType.LAND1,cellType.LAND2,))

        # --------------------------------------------------------------------

        #LAND3 (cliffs) (low spawn rate, but high infection rate)
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND or cell.cellType == cellType.LAND1 or cell.cellType == cellType.LAND2:
                    if randint(0, 10000) > 9995:
                        cell.cellType = cellType.LAND3
                        self.infectCells(50, cell.x, cell.y, cellType.LAND3, (cellType.LAND,cellType.LAND1,cellType.LAND2))

        # Generate specific land around cliffs
        self.generateCells(1, 0, '>', (cellType.LAND,cellType.LAND1,cellType.LAND2,), (cellType.LAND3,), cellType.LAND)

        # Create cliff peaks
        rad0 = 3
        self.generateCells(rad0, rad0*8, '=', (cellType.LAND3,), (cellType.LAND3,), cellType.LAND5)

        # Generate small areas around peaks of LAND5
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
                        cell.cellType = cellType.LAND5
                        self.infectCells(40, cell.x, cell.y, cellType.LAND4, (cellType.LAND3,))
#
    #    #LAND5 (cliffs, different color) (low spawn rate, but high infection rate)
        for column in self.grid:
            for cell in column:
                if cell.cellType == cellType.LAND4:
                    if randint(0, 10000) > 9800:
                        cell.cellType = cellType.LAND5
                        self.infectCells(40, cell.x, cell.y, cellType.LAND5, (cellType.LAND4,))

        #Choose Town locations
        maxTowns = 10
        townList = []
        while(maxTowns > 0):
            #choose random cell
            cell = self.grid[randint(0, len(self.grid)-1)][randint(0, len(self.grid[0])-1)]
            if cell.cellType in [cellType.LAND,cellType.LAND1,cellType.LAND2]:
                    surroundingCells = self.getSurroundingCellsInfo(cell.x,cell.y,4)
                    badCellCount = 0
                    waterCount = 0
                    for i in surroundingCells:
                        if self.checkIfWater(i):
                            waterCount += 1
                        elif i.cellType in [cellType.LAND3,cellType.LAND4,cellType.LAND5,cellType.TOWN]:
                            badCellCount += 1
                    if waterCount > 1 and waterCount < 15 and badCellCount == 0: #and randint(0,10000) > 9980:
                    #if randint(0,10000) > 9950:
                        #surroundingCells = self.getSurroundingCellsInfo(cell.x, cell.y, 1)
                        #direction = randint(0,7)
                        #distance = randint(2,3)
                        #maxRoadLen = randint(10,20)
                        #self.createRoad(cell.x, cell.y, direction, distance, maxRoadLen,maxRoadLen,0) # Make road
                        #self.createRoad(cell.x, cell.y, (direction+4)%8, distance, maxRoadLen,maxRoadLen,0) # Make another road in opposite direction
                        cell.cellType = cellType.TOWN
                        townList.append(cell)
                        maxTowns -= 1

        # Connect towns

        self.closestTownList = self.connectTowns(townList)

         # Create "border" cells around towns

        for column in self.grid:
            for cell in column:
                if cell.cellType in [cellType.TOWN,cellType.CONNECTED_TOWN]:
                    for adjacentCell in self.getSurroundingCellsInfo(cell.x,cell.y,1):
                        adjacentCell.cellType = cellType.ROAD_DIRT

         # Generate land bits around roads
        self.generateCells(1, 0, '>', (cellType.LAND,cellType.LAND1,cellType.LAND2,cellType.LAND3,cellType.LAND4,cellType.LAND5,cellType.TREE0), (cellType.ROAD_DIRT,), cellType.LAND1)

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
                cell.cellType = cellType.RIVER_WATER1
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
        if (
            cell.cellType == cellType.WATER or cell.cellType == cellType.DEEP_WATER0
        or cell.cellType == cellType.DEEP_WATER1 or cell.cellType == cellType.DEEP_WATER2
        or cell.cellType == cellType.DEEP_WATER3 or cell.cellType == cellType.RIVER_WATER1
        or cell.cellType == cellType.RIVER_WATER2 or cell.cellType == cellType.RIVER_WATER3
        ):
            return TRUE
        else:
            return FALSE

    def createRiver(self, x , y, direction, distance, counter, counterStart, lastDirChoice):
        
        if counter <= 0:
            return

        # New coords for next line

        offsets = self.getDirectionCoordinates(direction)

        xNew = x+offsets[0]*distance
        yNew = y+offsets[1]*distance

        for i in range(distance):
            if (
                (x+i*offsets[0]) in range(0, len(self.grid))  #checks to ensure x location writing to is within grid
                and (y+i*offsets[1]) in range(0, len(self.grid[0]))  #checks to ensure y location writing to is within grid
            ):
                if not self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
                    if counter > counterStart * (5/6):
                        self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER1
                    elif counter > counterStart * (2/6):
                        self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER2
                    else:
                        self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.RIVER_WATER3

        # Repeat with new line

        if not ((xNew) in range(0, len(self.grid)) and (yNew) in range(0, len(self.grid[0]))):
            return

        surroundingEndList = self.getSurroundingCellsInfo(xNew,yNew,1)
        for cell in surroundingEndList:
            if cell.cellType == cellType.WATER:
                return

        #if randint(0,100) > 1:
        distanceNew = randint(2,3)
        dirChooser = randint(0,5)

        if dirChooser not in [1,2]:
            dirChooser = 0

        directionNew = direction

        if dirChooser == 1:
            directionNew = (direction-1) % 8
        elif dirChooser == 2:
            directionNew = (direction+1) % 8

        if (dirChooser == lastDirChoice):
            if randint(0, 100) < randint(50, 80):
                directionNew = direction


        self.createRiver(xNew , yNew, directionNew, distanceNew, counter-1, counterStart, dirChooser)
        
        forkPercent = 0 # default

        if counter > counterStart * (5/6):
            forkPercent = randint(0, 8)
        elif counter > counterStart * (2/6):
            forkPercent = randint(0, 15)
        else:
            forkPercent = randint(0, 30)
        
        if randint(0,100) < forkPercent:  #fork
            distanceNew2 = randint(2,5)
            self.createRiver(xNew , yNew, directionNew, distanceNew2, counter-1, counterStart, dirChooser)

    def connectTowns(self, townList):
        closestTowns = self.findClosestTowns(townList, townList)
        print('finished finding closest towns!')
        return closestTowns

    def findClosestTowns(self, townList, originalTownList):
        #finalList = []
        shortestDistanceList = []
        connectedTown = []
        for Town in townList:
            lastDifference = 0
            firstRound = True
            closestTownIndex = -1
            for secondTown in originalTownList:
                if Town == secondTown:
                    pass
                else:
                    difference = math.sqrt((Town.x-secondTown.x)**2 + (Town.y-secondTown.y)**2)
                    if firstRound:
                        firstRound = False
                        lastDifference = difference
                    elif difference < lastDifference:
                        closestTownIndex = originalTownList.index(secondTown)
                        lastDifference = difference
            connectedTown = [Town, originalTownList[closestTownIndex]]
            shortestDistanceList.append(connectedTown)

        shortestDistanceListNoDuples = []
        for i in shortestDistanceList:
            if i not in shortestDistanceListNoDuples and [i[1],i[0]] not in shortestDistanceListNoDuples:
                shortestDistanceListNoDuples.append(i)
        
        for i in shortestDistanceListNoDuples:
            i[0].cellType = cellType.CONNECTED_TOWN
        
        unconnectedTowns = []
        for town in originalTownList:
            if town.cellType == cellType.TOWN:
                unconnectedTowns.append(town)

        #TODO FIX THIS SHIT SO ITS RECURSEIVE AND RETURNS A LIST OF ALL THE TOWNS WITH THEIR CLOSEST TOWN CONNECTION
        if len(shortestDistanceListNoDuples) < len(townList):
            for combo in self.findClosestTowns(unconnectedTowns, townList):
                shortestDistanceListNoDuples.append(combo)

        return shortestDistanceListNoDuples
    
    def createRoad(self, x , y, direction, distance, counter, counterStart, lastDirChoice):
        
        if counter <= 0 and not self.checkIfWater(self.grid[x][y]):

            if randint(0,100) < 50 and int(counterStart/2) > 5:
                directionNew = randint(0,7)
                distanceNew = randint(2,3)
                self.createRoad(x, y, directionNew, distanceNew, int(counterStart/2),int(counterStart/2),0) # Make roads
                self.createRoad(x, y, (directionNew+2)%8, distanceNew, int(counterStart/2),int(counterStart/2),0) # Make roads

            self.grid[x][y].cellType = cellType.TOWN

            return

        # New coords for next line
        offsets = self.getDirectionCoordinates(direction)

        xNew = x+offsets[0]*distance
        yNew = y+offsets[1]*distance

        for i in range(distance):
            if (
                (x+i*offsets[0]) in range(0, len(self.grid))  #checks to ensure x location writing to is within grid
                and (y+i*offsets[1]) in range(0, len(self.grid[0]))  #checks to ensure y location writing to is within grid
            ):
                if self.checkIfWater(self.grid[x+i*offsets[0]][y+i*offsets[1]]):
                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.BRIDGE_WOOD # Bridge over water
                else:
                    self.grid[x+i*offsets[0]][y+i*offsets[1]].cellType = cellType.ROAD_DIRT # Land-based dirt road

        # Repeat with new line

        if not ((xNew) in range(0, len(self.grid)) and (yNew) in range(0, len(self.grid[0]))):
            return

        surroundingEndList = self.getSurroundingCellsInfo(xNew,yNew,1)
        for cell in surroundingEndList:
            if cell.cellType == cellType.WATER:
                return

        #if randint(0,100) > 1:
        distanceNew = randint(2,3)
        dirChooser = randint(0,5)

        if dirChooser not in [1,2]:
            dirChooser = 0

        directionNew = direction

        if dirChooser == 1:
            directionNew = (direction-1) % 8
        elif dirChooser == 2:
            directionNew = (direction+1) % 8

        if (dirChooser == lastDirChoice):
            if randint(0, 100) < randint(10, 20):
                directionNew = direction

        self.createRoad(xNew , yNew, directionNew, distanceNew, counter-1, counterStart, dirChooser)
        
        forkPercent = 4 #0 # default

    #    if counter > counterStart * (5/6):
    #        forkPercent = randint(0, 8)
    #    elif counter > counterStart * (2/6):
    #        forkPercent = randint(0, 15)
    #    else:
    #        forkPercent = randint(0, 30)
        
        if randint(0,100) < forkPercent:  #fork
            distanceNew2 = randint(2,5)
            self.createRoad(xNew , yNew, directionNew, distanceNew2, counter-1, counterStart, dirChooser)


    def draw(self):
        for column in self.grid:
            for cell in column:
                cell.draw()
        for townCombo in self.closestTownList:
            print(townCombo[0].x,townCombo[0].y,townCombo[1].x,townCombo[1].y,)
            self.master.create_line(townCombo[0].x,townCombo[0].y,townCombo[1].x,townCombo[1].y,)
            



pixelsPerCell = 6
numColumns = int(1400/pixelsPerCell) #Number of Columns directly coorelates to the x position of the grid
numRows = int(750/pixelsPerCell) #Number of Columns directly coorelates to the y position of the grid
infectionRate = randint(90, 100)

#def key(event):
#    if event.char in ['r','R']:
#        print('Generating new map')
#        grid = CellGrid(app, numRows, numColumns, pixelsPerCell, infectionRate, Biomes.PLAINS)




if __name__ == "__main__" :
    app = Tk()

    #app.bind_all('<Key>', key)

    grid = CellGrid(app, numRows, numColumns, pixelsPerCell, infectionRate, Biomes.PLAINS)
    grid.pack()

    app.mainloop()