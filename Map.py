from random import randint
from tkinter import *
import math
from enum import Enum

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


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
    LAND_DESERT0 = 23
    LAND_DESERT1 = 24
    LAND_DESERT2 = 25
    LAND_SNOW0 = 26
    LAND_SNOW1 = 27
    LAND_SNOW2 = 28


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
        """
        Description
        -----------
        Get cell color from cellType
        """
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
        """
        Description
        -----------
        Draw current cell to the window
        """
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
        self.closestTownList = []
        for column in range(columnNumber):

            line = []
            for row in range(rowNumber):
                cellType = self.chooseBaseCellTypes(Biome)
                line.append(Cell(self, column, row, cellSize, cellType))
            self.grid.append(line)

        self.createWater(infectionRate)
        self.createLandDiversity(infectionRate)

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
        Generate water bodies (lakes, oceans) using infectCells; generate rivers from water bodies

        Params
        --------
        infectionRate - int
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
        """
        Description
        -----------
        Generate areas of different land types, mountains, and towns
        
        Params
        --------
        infectionRate - int
        """
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
        numTowns = 0
        townList = []
        while(numTowns < maxTowns):
            #choose random cell
            cell = self.grid[randint(2, len(self.grid)-3)][randint(2, len(self.grid[0])-3)] # Make towns, not at very edge of map
            if cell.cellType in [cellType.LAND,cellType.LAND1,cellType.LAND2]:
                    surroundingCells = self.getSurroundingCellsInfo(cell.x,cell.y,4)
                    badCellCount = 0
                    waterCount = 0
                    for i in surroundingCells:
                        if self.checkIfWater(i):
                            waterCount += 1
                        elif i.cellType in [cellType.LAND3,cellType.LAND4,cellType.LAND5,cellType.TOWN]:
                            badCellCount += 1

                    if badCellCount != 0:
                        pass
                    
                    # Find distances between towns and make sure they spawn at least "townMinDistance" cells apart
                    lastDifference = 0
                    firstRound = True
                    for existingTown in townList:
                        if cell == existingTown:
                            pass
                        else:
                            difference = math.sqrt((cell.x-existingTown.x)**2 + (cell.y-existingTown.y)**2)
                            if firstRound:
                                firstRound = False
                                lastDifference = difference
                            elif difference < lastDifference:
                                lastDifference = difference

                    # Check if making first town, or if town distance is far enough away from existing towns
                    if (len(townList) == 0) or (lastDifference > townMinDistance):
                        cell.cellType = cellType.TOWN
                        townList.append(cell)
                        numTowns += 1

        # Choose towns to connect

        self.closestTownList = self.connectTowns(townList)

        # Connect towns using roads with A* pathfinding method
        for combo in self.closestTownList:
            pathList = self.pathfinder(combo[0].x, combo[0].y, combo[1].x, combo[1].y)
            x1 = combo[0].x
            y1 = combo[0].y
            for coords in pathList:
                if [coords[0],coords[1]] not in [[combo[0].x, combo[0].y,],[combo[1].x, combo[1].y,]]:
                    if self.checkIfWater(self.grid[coords[0]][coords[1]]):
                        self.grid[coords[0]][coords[1]].cellType = cellType.BRIDGE_WOOD # make bridges over water
                    else:
                        self.grid[coords[0]][coords[1]].cellType = cellType.ROAD_DIRT # make roads over everything else (for now)

         # Create "border" cells around towns

        for column in self.grid:
            for cell in column:
                if cell.cellType in [cellType.TOWN,cellType.CONNECTED_TOWN]:
                    for adjacentCell in self.getSurroundingCellsInfo(cell.x,cell.y,1):
                        adjacentCell.cellType = cellType.ROAD_DIRT

         # Generate land bits around roads
        self.generateCells(1, 0, '>', (cellType.LAND,cellType.LAND1,cellType.LAND2,cellType.LAND3,cellType.LAND4,cellType.LAND5,cellType.TREE0), (cellType.ROAD_DIRT,), cellType.LAND1)

    def generateCells(self, rad, threshold, thresholdOperator, currentCellTypes, cellTypeConditional, newCellType):
        """
        Description
        -------------
        Check for cells within a specific set of cellTypes, and if a specific conditional operator is true, then convert current cell(s) into another specific cellType.

        Params
        --------
        rad - An int, radius to search in for cells of cellTypeConditional
        threshold - An int, number of cells to find for the operator to return true
        thresholdOperator - '>', '<', or '='; operator to check using the threshold value
        currentCellTypes - tuple of cellType(s) to use as center of radius, and which will be converted into newCellType if operator is true
        cellTypeConditional - tuple of cellType(s) to check for in the radius; counted fot the operator check
        newCellType - cellType to convert cells of currentCellType to if they pass the operator check

        """
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
        """
        Description
        -----------
        From an input cell, find nearby water cells and find a direction that faces away from them the most. Returns a direction (enum).
        
        Params
        --------
        surroundingCellList - list of cells; intended to be the list of cells surrounding the current cell as found using getSurroundingCellsInfo
        x - x coordinate of the infecting cell
        y - y coordinate of the infecting cell
        """
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
        """
        Description
        -----------
        From an input direction, find offsets for x and y and return them as a 1D list
        
        Params
        --------
        direction - direction (enum) to check; intended to be between 0 and 7
        """
        xOff = 0
        yOff = 0

        direction2 = direction%8

        if direction2 == Directions.UP.value:
            xOff = 0
            yOff = -1
        elif direction2 == Directions.UP_RIGHT.value:
            xOff = 1
            yOff = -1
        elif direction2 == Directions.RIGHT.value:
            xOff = 1
            yOff = 0
        elif direction2 == Directions.DOWN_RIGHT.value:
            xOff = 1
            yOff = 1
        elif direction2 == Directions.DOWN.value:
            xOff = 0
            yOff = 1
        elif direction2 == Directions.DOWN_LEFT.value:
            xOff = -1
            yOff = 1
        elif direction2 == Directions.LEFT.value:
            xOff = -1
            yOff = 0
        elif direction2 == Directions.UP_LEFT.value:
            xOff = -1
            yOff = -1

        # print(str(xOff)+", "+str(yOff))

        return [xOff,yOff]

    def checkIfWater(self, cell):
        """
        Description
        -----------
        From an input cell, check if it is considered water.
        
        Params
        --------
        cell - input cell
        """
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
        """
        Description
        -----------
        Generate a river line from a given start point; generate different sizes based on current length of river.
        
        Params
        --------
        x - int, starting x coordinate
        y - int, starting y coordinate
        direction - current direction
        distance - distance for this line
        counter - int, counts down with recursive calls to limit river length
        counterStart - int, starting value of counter; set both counter and counterStart to same value when calling in generation
        lastDirChoice - int used to limit direction changes that would cause rivers to loop in on themselves too often; use 0 when calling in generation
        """

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
        """
        Description
        -----------
        Returns a list containing town pairs to connect together.
        
        Params
        --------
        townList - list of cells of cellType cellType.TOWN
        """
        closestTowns = self.findClosestTowns(townList, townList)
        return closestTowns

    def findClosestTowns(self, townList, originalTownList):
        """
        Description
        -----------
        Finds closest towns for each town in townList and returns a list of town combinations without duplicates
        
        Params
        --------
        townList - list of cells of cellType cellType.TOWN (changes during recursive calls)
        originalTownList - list of cells of cellType cellType.TOWN (doesn't change)
        """
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

        #Connect any towns that have no connections to nearest town
        if len(shortestDistanceListNoDuples) < len(townList):
            for combo in self.findClosestTowns(unconnectedTowns, townList):
                shortestDistanceListNoDuples.append(combo)

    #    # TEST: Connect towns that only have one connection
    #    singleConnectionTowns = []
#
    #    if townList == originalTownList: # If first call
    #        for town in townList:
    #            totConnections = 0
    #            for combo in shortestDistanceListNoDuples:
    #                if town in [combo[0], combo[1]]:
    #                    totConnections += 1
    #            if totConnections == 0:
    #                singleConnectionTowns.append(town)
    #                print(town)
    #            
    #    for combo in self.findClosestTowns(singleConnectionTowns, singleConnectionTowns):
    #            shortestDistanceListNoDuples.append(combo)

        return shortestDistanceListNoDuples
    
    def pathfinder(self, x0, y0, x1, y1):
        """
        Description
        -----------
        Finds a path between two points and returns a list of coordinates along the path
        Currently only checks for road-compatible paths by avoiding mountains and going on land when possible
        
        Params
        --------
        x0,y0,x1,y1 - coordinates for two points to connect
        """
        # Generate pathfinding grid

        matrix = [ [0]*len(self.grid) for i in range(len(self.grid))]

        for column in self.grid:
            for cell in column:
                if cell.cellType in [cellType.LAND3,cellType.LAND4,cellType.LAND5,]:
                    matIn = 0 # obstacles
                elif self.checkIfWater(cell) or cell.cellType in [cellType.SAND,cellType.RIVER_BANK,]:
                    matIn = 5 #water, only cross this if necessary
                elif cell.cellType in [cellType.ROAD_DIRT,]:
                    matIn = 1 #use existing roads when possible
                else:
                    matIn = 2 #free spaces
                matrix[cell.y][cell.x] = matIn

        pathGrid = Grid(matrix=matrix)

        # Find a path
        start = pathGrid.node(x0,y0)
        end = pathGrid.node(x1,y1)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, pathGrid)

        # Return the path
        return path

    def createRoad(self, x , y, direction, distance, counter, counterStart, lastDirChoice):
        """
        Description
        -----------
        Generate a road line from a given start point
        
        Params
        --------
        x - int, starting x coordinate
        y - int, starting y coordinate
        direction - current direction
        distance - distance for this line
        counter - int, counts down with recursive calls to limit river length
        counterStart - int, starting value of counter; set both counter and counterStart to same value when calling in generation
        lastDirChoice - int used to limit direction changes that would cause rivers to loop in on themselves too often; use 0 when calling in generation
        """
        
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
        
        if randint(0,100) < forkPercent:  #fork
            distanceNew2 = randint(2,5)
            self.createRoad(xNew , yNew, directionNew, distanceNew2, counter-1, counterStart, dirChooser)


    def draw(self):
        """
        Description
        -----------
        Draw the grid to the window

        """
        for column in self.grid:
            for cell in column:
                cell.draw()
    #    for townCombo in self.closestTownList: # Draw lines between connected towns
    #        self.create_line(townCombo[0].x*pixelsPerCell+int(pixelsPerCell/2),
    #        townCombo[0].y*pixelsPerCell+int(pixelsPerCell/2),
    #        townCombo[1].x*pixelsPerCell+int(pixelsPerCell/2),
    #        townCombo[1].y*pixelsPerCell+int(pixelsPerCell/2),)
            

sizeH = 1000#750 #1400
sizeV = 750

pixelsPerCell = 4
numColumns = int(sizeH/pixelsPerCell) #Number of Columns directly coorelates to the x position of the grid
numRows = int(sizeV/pixelsPerCell) #Number of Columns directly coorelates to the y position of the grid
maxTowns = 10#15
townMinDistance = 20#10
infectionRate = randint(90, 100)
grid = []

# Test to regen map with a button; doesn't work since it doesn't modify the old grid or pass the new grid out, gotta figure it out
#def regenGrid(app, grid):
#    print('Generating new map')
#    app.destroy(grid)
#    grid = CellGrid(app, numRows, numColumns, pixelsPerCell, infectionRate, Biomes.PLAINS)
#    app.pack(grid)

if __name__ == "__main__" :
    app = Tk()

    grid = CellGrid(app, numRows, numColumns, pixelsPerCell, infectionRate, Biomes.PLAINS)
    #b = Button(app, text="Regenerate", command=lambda : regenGrid(app,grid))
    #b.pack()
    grid.pack()

    #app.bind_all('<Key>', key)

    app.mainloop()