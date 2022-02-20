from tkinter import *
import math
from random import randint

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from biomes import Biomes
from cell_types import CellTypes
from cell import Cell
from directions import Directions
from constants import *


class CellGrid(Canvas):
    def __init__(self, master, row_num, col_num, cell_size, infection_rate, biome, *args, **kwargs):
        Canvas.__init__(self, master, width=cell_size * col_num, height=cell_size * row_num, *args, **kwargs)

        self.cell_size = cell_size
        self.biome = biome
        self.grid = []
        self.closesttown_list = []

        for column in range(col_num):
            line = []
            for row in range(row_num):
                cell_types = self.choose_base_cell_types(biome)
                line.append(Cell(self, column, row, cell_size, cell_types))
            self.grid.append(line)

        self.create_water(infection_rate)
        self.create_land_diversity(infection_rate)

        self.draw()

    def cell_in_grid(self, x: int, y: int) -> bool:
        '''
        Description
        -----------
        This function returns a boolean value that represents whether or not a cell is contained within the boundaries of the grid.

        Parameters
        ----------
        x : int
            x position of the proposed cell.
        y : int
            y position of the proposed cell.

        Returns
        -------
        bool
            True whenever the cell x and y positions exist within the boundaries of the grid.
        '''
        return ((y < num_rows - 1) and (y > 0) and (x < num_cols - 1) and (x > 0))

    def choose_base_cell_types(self, biome: Biomes, land_percent: float = 99.98):
        """
        Description
        -----------
        This function determines the base cell types of the map and creates water starting point cells.
        This is determined by the passed biome and the land percentage parameter.

        Parameters
        ----------
        biome : Biome
            This is the biome associated with the map.
        land_percent : float
            A float value between 0.00 and 100.00 that represents the percentage of land you would like on the map
        """
        if biome == Biomes.PLAINS:
            rand_val = randint(0, 99999)
            if rand_val < (land_percent * 1000):
                return CellTypes.LAND
            else:
                return CellTypes.WATER_START

    def create_water(self, infection_rate: int):
        """
        Description
        -----------
        Generate water bodies (lakes, oceans) using infect_cells; generate rivers from water bodies

        Parameters
        ----------
        infection_rate : int
            Integer value that determines the percentage chance of infection.
        """
        # Create water infection from water start cells
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.WATER_START:
                    cell.cell_type = CellTypes.WATER
                    self.infect_cells(infection_rate, cell.x, cell.y, CellTypes.WATER, (CellTypes.LAND,))

        # Fill in single-cells of land
        self.generate_cells(1, 4, '>', [CellTypes.LAND], [CellTypes.WATER], CellTypes.WATER)

        # Fill in single-cells of water
        self.generate_cells(1, 2, '<', [CellTypes.WATER], [CellTypes.WATER], CellTypes.LAND)

        # Generate deep water 0
        rad0 = 2
        self.generate_cells(rad0, rad0 * 8, '=', [CellTypes.WATER], [CellTypes.WATER, CellTypes.DEEP_WATER0], CellTypes.DEEP_WATER0)

        # Generate deep water 1
        rad0 = 2
        self.generate_cells(rad0, rad0 * 8, '=', [CellTypes.DEEP_WATER0], [CellTypes.DEEP_WATER0, CellTypes.DEEP_WATER1], CellTypes.DEEP_WATER1)

        # Generate deep water 2
        rad0 = 3
        self.generate_cells(rad0, rad0 * 8, '=', [CellTypes.DEEP_WATER1], [CellTypes.DEEP_WATER1, CellTypes.DEEP_WATER2], CellTypes.DEEP_WATER2)

        # Generate deep water 3
        rad0 = 3
        self.generate_cells(rad0, rad0 * 8, '=', [CellTypes.DEEP_WATER2], [CellTypes.DEEP_WATER2, CellTypes.DEEP_WATER3], CellTypes.DEEP_WATER3)

        # TEST round off corners of deep water 3
        self.generate_cells(1, 4, '>', [CellTypes.DEEP_WATER3], [CellTypes.DEEP_WATER2], CellTypes.DEEP_WATER2)

        # Generate sand on land that touches water
        self.generate_cells(1, 0, '>', [CellTypes.LAND], [CellTypes.WATER], CellTypes.SAND)

        # Expand sand areas
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.SAND:
                    if randint(0, 100) > 50:
                        self.infect_cells(10, cell.x, cell.y, CellTypes.SAND, (CellTypes.LAND,))

        # Generate rivers
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.SAND:
                    surroundingCells = self.get_surrounding_cells_info(cell.x, cell.y, 1)
                    sandCount = 0
                    waterCount = 0
                    for i in surroundingCells:
                        if i.cell_type == CellTypes.SAND:
                            sandCount += 1
                        elif i.cell_type == CellTypes.WATER:
                            waterCount += 1
                    if sandCount < 4 and waterCount > 0 and randint(0, 10000) > 9900:
                        cell.cell_type = CellTypes.RIVER_HEAD
                        direction = self.get_direction(surroundingCells, cell.x, cell.y)
                        distance = randint(2, 3)
                        maxRiverLen = randint(20, 40)
                        self.create_river(cell.x, cell.y, direction, distance, maxRiverLen, maxRiverLen, 0)

        # Generate thicker rivers
        self.generate_cells(1, 0, '>', [CellTypes.LAND], [CellTypes.RIVER_WATER1, CellTypes.RIVER_HEAD], CellTypes.RIVER_BANK)

        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.RIVER_BANK:
                    cell.cell_type = CellTypes.RIVER_WATER2

        self.generate_cells(1, 0, '>', [CellTypes.LAND], [CellTypes.RIVER_WATER2], CellTypes.RIVER_BANK)

        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.RIVER_BANK:
                    cell.cell_type = CellTypes.RIVER_WATER3

        # Generate banks around rivers
        self.generate_cells(1, 0, '>', [CellTypes.LAND], [CellTypes.RIVER_WATER1, CellTypes.RIVER_WATER2, CellTypes.RIVER_WATER3, CellTypes.RIVER_HEAD], CellTypes.RIVER_BANK)

        # Turn sand connected to river water into river water
        self.generate_cells(1, 0, '>', [CellTypes.SAND], [CellTypes.RIVER_WATER1, CellTypes.RIVER_WATER2, CellTypes.RIVER_WATER3, CellTypes.RIVER_HEAD], CellTypes.LAND1)
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.LAND1:
                    cell.cell_type = CellTypes.RIVER_WATER3

    def create_land_diversity(self, infection_rate):
        """
        Description
        -----------
        Generate areas of different land types, mountains, and towns

        Params
        --------
        infection_rate - int
        """
        # Generate areas of differently-colored land
        # LAND1
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.LAND:
                    if randint(0, 10000) > 9950:
                        cell.cell_type = CellTypes.LAND1
                        self.infect_cells(40, cell.x, cell.y, CellTypes.LAND1, (CellTypes.LAND,))

        # LAND2
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.LAND or cell.cell_type == CellTypes.LAND1:
                    if randint(0, 10000) > 9950:
                        cell.cell_type = CellTypes.LAND2
                        self.infect_cells(30, cell.x, cell.y, CellTypes.LAND2, (CellTypes.LAND, CellTypes.LAND1))

        # TREE0
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.LAND or cell.cell_type == CellTypes.LAND1 or cell.cell_type == CellTypes.LAND2:
                    if randint(0, 10000) > 9995:
                        cell.cell_type = CellTypes.TREE0
                        self.infect_cells(50, cell.x, cell.y, CellTypes.TREE0, (CellTypes.LAND, CellTypes.LAND1, CellTypes.LAND2,))

        # --------------------------------------------------------------------

        # LAND3 (cliffs) (low spawn rate, but high infection rate)
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.LAND or cell.cell_type == CellTypes.LAND1 or cell.cell_type == CellTypes.LAND2:
                    if randint(0, 10000) > 9995:
                        cell.cell_type = CellTypes.LAND3
                        self.infect_cells(50, cell.x, cell.y, CellTypes.LAND3, (CellTypes.LAND, CellTypes.LAND1, CellTypes.LAND2))

        # Generate specific land around cliffs
        self.generate_cells(1, 0, '>', [CellTypes.LAND, CellTypes.LAND1, CellTypes.LAND2], [CellTypes.LAND3], CellTypes.LAND)

        # Create cliff peaks
        rad0 = 3
        self.generate_cells(rad0, rad0 * 8, '=', [CellTypes.LAND3], [CellTypes.LAND3], CellTypes.LAND5)

        # Generate small areas around peaks of LAND5
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.LAND5:
                    # if randint(0, 10000) > 9500:
                    self.infect_cells(10, cell.x, cell.y, CellTypes.LAND5, (CellTypes.LAND3,))

        # Fill in single-cells of land between cliffs
        self.generate_cells(1, 4, '>', [CellTypes.LAND, CellTypes.LAND1, CellTypes.LAND2], [CellTypes.LAND3], CellTypes.LAND3)
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.LAND3:
                    if randint(0, 10000) > 9800:
                        cell.cell_type = CellTypes.LAND5
                        self.infect_cells(40, cell.x, cell.y, CellTypes.LAND4, (CellTypes.LAND3,))

        # LAND5 (cliffs, different color) (low spawn rate, but high infection rate)
        for column in self.grid:
            for cell in column:
                if cell.cell_type == CellTypes.LAND4:
                    if randint(0, 10000) > 9800:
                        cell.cell_type = CellTypes.LAND5
                        self.infect_cells(40, cell.x, cell.y, CellTypes.LAND5, (CellTypes.LAND4,))

        # Choose Town locations
        num_towns = 0
        town_list = []
        while(num_towns < max_towns):
            # choose random cell
            cell = self.grid[randint(2, len(self.grid) - 3)][randint(2, len(self.grid[0]) - 3)]  # Make towns, not at very edge of map
            if cell.cell_type in [CellTypes.LAND, CellTypes.LAND1, CellTypes.LAND2]:
                surroundingCells = self.get_surrounding_cells_info(cell.x, cell.y, 4)
                badCellCount = 0
                waterCount = 0
                for i in surroundingCells:
                    if self.check_if_water(i):
                        waterCount += 1
                    elif i.cell_type in [CellTypes.LAND3, CellTypes.LAND4, CellTypes.LAND5, CellTypes.TOWN]:
                        badCellCount += 1

                if badCellCount != 0:
                    pass

                # Find distances between towns and make sure they spawn at least "town_min_distance" cells apart
                lastDifference = 0
                firstRound = True
                for existingTown in town_list:
                    if cell == existingTown:
                        pass
                    else:
                        difference = math.sqrt((cell.x - existingTown.x)**2 + (cell.y - existingTown.y)**2)
                        if firstRound:
                            firstRound = False
                            lastDifference = difference
                        elif difference < lastDifference:
                            lastDifference = difference

                # Check if making first town, or if town distance is far enough away from existing towns
                if (len(town_list) == 0) or (lastDifference > town_min_distance):
                    cell.cell_type = CellTypes.TOWN
                    town_list.append(cell)
                    num_towns += 1

        # Choose towns to connect
        self.closesttown_list = self.connect_towns(town_list)

        # Connect towns using roads with A* pathfinding method
        for combo in self.closesttown_list:
            pathList = self.path_finder(combo[0].x, combo[0].y, combo[1].x, combo[1].y)
            for coords in pathList:
                if [coords[0], coords[1]] not in [[combo[0].x, combo[0].y, ], [combo[1].x, combo[1].y, ]]:
                    if self.check_if_water(self.grid[coords[0]][coords[1]]):
                        self.grid[coords[0]][coords[1]].cell_type = CellTypes.BRIDGE_WOOD  # make bridges over water
                    else:
                        self.grid[coords[0]][coords[1]].cell_type = CellTypes.ROAD_DIRT  # make roads over everything else (for now)

        # Create "border" cells around towns
        for column in self.grid:
            for cell in column:
                if cell.cell_type in [CellTypes.TOWN, CellTypes.CONNECTED_TOWN]:
                    for adjacentCell in self.get_surrounding_cells_info(cell.x, cell.y, 1):
                        adjacentCell.cell_type = CellTypes.ROAD_DIRT

        # Generate land bits around roads
        self.generate_cells(
            1, 0, '>', [CellTypes.LAND, CellTypes.LAND1, CellTypes.LAND2, CellTypes.LAND3, CellTypes.LAND4, CellTypes.LAND5, CellTypes.TREE0],
            [CellTypes.ROAD_DIRT], CellTypes.LAND1
        )

    def generate_cells(self, radius, threshold, threshold_operator, current_cell_types, cell_types_conditional, new_cell_type):
        """
        Description
        -------------
        Check for cells within a specific set of cell types, and if a specific conditional operator is true, then convert current cell(s) into the specified
        cell type.

        Paramaters
        ----------
        radius : int
            An int, radius to search in for cells of cell_types_conditional
        threshold : int
            An int, number of cells to find for the operator to return true
        threshold_operator : str
            '>', '<', or '='; operator to check using the threshold value
        current_cell_types : Tuple
            Tuple of CellTypes(s) to use as center of radius, and which will be converted into new_cell_type if operator is true
        cell_types_conditional : Tuple
            Tuple of CellTypes(s) to check for in the radius; counted fot the operator check
        new_cell_type : CellTypes
            The cell type to convert cells of current_cell_types to if they pass the operator check

        """
        for column in self.grid:
            for cell in column:
                if cell.cell_type in current_cell_types:
                    surrounding_type_count = 0
                    surrounding_cells = self.get_surrounding_cells_info(cell.x, cell.y, radius)

                    for i in surrounding_cells:
                        if i.cell_type in cell_types_conditional:
                            surrounding_type_count += 1

                    # Check threshold operator and check if threshold met, then apply new_cell_type if it is
                    if threshold_operator == '=' and surrounding_type_count == threshold:
                        cell.cell_type = new_cell_type

                    elif threshold_operator == '>' and surrounding_type_count > threshold:
                        cell.cell_type = new_cell_type

                    elif threshold_operator == '<' and surrounding_type_count < threshold:
                        cell.cell_type = new_cell_type

                    else:
                        Exception('The threshold operator passed was not one of the viable options.')

    def infect_cells(self, infection_rate: int, x: int, y: int, cell_type_new: CellTypes, cell_types_to_replace: CellTypes):
        """
        Description
        -------------
        Infect surrounding cells (with a percent chance) with a particular CellTypes.

        Params
        --------
        infection_rate : Int
            Value (between 0 and 100) that defines how likely any given cell is to be infected.
        x : int
            x coordinate of the infecting cell.
        y : int
            y coordinate of the infecting cell.
        cell_type_new : List
            List of possible cell types that infected cells will change to.
        cell_types_to_replace : List
            List of cell types that need to be replaced.
        """
        self.infect_cell(infection_rate, x, y - 1, cell_type_new, cell_types_to_replace)  # UP
        self.infect_cell(infection_rate, x - 1, y - 1, cell_type_new, cell_types_to_replace)  # UP LEFT
        self.infect_cell(infection_rate, x + 1, y - 1, cell_type_new, cell_types_to_replace)  # UP RIGHT
        self.infect_cell(infection_rate, x, y + 1, cell_type_new, cell_types_to_replace)  # DOWN
        self.infect_cell(infection_rate, x - 1, y + 1, cell_type_new, cell_types_to_replace)  # DOWN LEFT
        self.infect_cell(infection_rate, x + 1, y + 1, cell_type_new, cell_types_to_replace)  # DOWN RIGHT
        self.infect_cell(infection_rate, x - 1, y, cell_type_new, cell_types_to_replace)  # LEFT
        self.infect_cell(infection_rate, x + 1, y, cell_type_new, cell_types_to_replace)  # RIGHT

    def infect_cell(self, infection_rate: int, x: int, y: int, cell_type_new: CellTypes, cell_types_to_replace: CellTypes):
        """
        Description
        -----------
        Infect a single cell with a particular cell type.

        Paramaters
        ----------
        infection_rate : int
            Value (between 0 and 100?) that defines how likely any given cell is to be infected.
        x : int
            x coordinate of the infecting cell.
        y : int
            y coordinate of the infecting cell.
        cell_type_new : CellTypes
            Cell types that infected cells will change to.
        cell_types_to_replace : CellTypes
            Cell types that will be replaced by infected cells.
        """
        # Check whether given coordinates work for a cell in the grid
        if self.cell_in_grid(x, y):
            # Check to see if the cell type is one that needs to be replaced
            if self.grid[x][y].cell_type in cell_types_to_replace:
                rand_val = randint(0, 99)

                # If rand_val is less than the infection rate, change it and then infect the cells around it while reducing the infection rate
                if rand_val < infection_rate and self.grid[x][y].cell_type != cell_type_new and self.grid[x][y].cell_type != CellTypes.WATER_START:
                    self.grid[x][y].cell_type = cell_type_new
                    self.infect_cells(infection_rate - 1, x, y, cell_type_new, cell_types_to_replace)

    def get_surrounding_cells_info(self, x, y, radius):
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
        for i in range(1, radius + 1):
            if y - i >= 0:
                surroundingCellList.append(self.grid[x][y - i])  # UP
            if x < num_cols - i and y - i >= 0:
                surroundingCellList.append(self.grid[x + i][y - i])  # UP RIGHT
            if x < num_cols - i:
                surroundingCellList.append(self.grid[x + i][y])  # RIGHT
            if x < num_cols - i and y < num_rows - i:
                surroundingCellList.append(self.grid[x + i][y + i])  # DOWN RIGHT
            if y < num_rows - i:
                surroundingCellList.append(self.grid[x][y + i])  # DOWN
            if x - i >= 0 and y < num_rows - i:
                surroundingCellList.append(self.grid[x - i][y + i])  # DOWN LEFT
            if x - i >= 0:
                surroundingCellList.append(self.grid[x - i][y])  # LEFT
            if x - i >= 0 and y - i >= 0:
                surroundingCellList.append(self.grid[x - i][y - i])  # UP LEFT

        return surroundingCellList  # returns a list of the surrounding cells' CellTypess

    def get_direction(self, surroundingCellList, x, y):
        """
        Description
        -----------
        From an input cell, find nearby water cells and find a direction that faces away from them the most. Returns a direction (enum).

        Params
        --------
        surroundingCellList - list of cells; intended to be the list of cells surrounding the current cell as found using get_surrounding_cells_info
        x - x coordinate of the infecting cell
        y - y coordinate of the infecting cell
        """
        waterCount = 0                                  # Find "center" of surrounding water tiles
        for cell in surroundingCellList:
            if cell.cell_type == CellTypes.SAND:
                cell.cell_type = CellTypes.RIVER_WATER1
            if cell.cell_type == CellTypes.WATER:
                waterCount += 1
        waterIndex = math.ceil(waterCount / 2)
        for cell in surroundingCellList:
            if cell.cell_type == CellTypes.WATER:
                waterIndex -= 1
            if waterIndex == 0:
                direction = surroundingCellList.index(cell)
                direction = (direction + 4) % 8         # Find opposite direction from chosen cell
                return direction

    def get_directionCoordinates(self, direction):
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

        direction2 = direction % 8

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

        return [xOff, yOff]

    def check_if_water(self, cell):
        """
        Description
        -----------
        From an input cell, check if it is considered water.

        Params
        --------
        cell - input cell
        """
        return cell.cell_type in water_cells

    def create_river(self, x, y, direction, distance, counter, counterStart, lastDirChoice):
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

        offsets = self.get_directionCoordinates(direction)

        xNew = x + offsets[0] * distance
        yNew = y + offsets[1] * distance

        for i in range(distance):
            # checks to ensure x location and y location being written to is within the grid
            if (
                (x + i * offsets[0]) in range(0, len(self.grid)) and (y + i * offsets[1]) in range(0, len(self.grid[0]))
            ):
                if not self.check_if_water(self.grid[x + i * offsets[0]][y + i * offsets[1]]):
                    if counter > counterStart * (5 / 6):
                        self.grid[x + i * offsets[0]][y + i * offsets[1]].cell_type = CellTypes.RIVER_WATER1
                    elif counter > counterStart * (2 / 6):
                        self.grid[x + i * offsets[0]][y + i * offsets[1]].cell_type = CellTypes.RIVER_WATER2
                    else:
                        self.grid[x + i * offsets[0]][y + i * offsets[1]].cell_type = CellTypes.RIVER_WATER3

        # Repeat with new line

        if not ((xNew) in range(0, len(self.grid)) and (yNew) in range(0, len(self.grid[0]))):
            return

        surroundingEndList = self.get_surrounding_cells_info(xNew, yNew, 1)
        for cell in surroundingEndList:
            if cell.cell_type == CellTypes.WATER:
                return

        # if randint(0,100) > 1:
        distanceNew = randint(2, 3)
        dirChooser = randint(0, 5)

        if dirChooser not in [1, 2]:
            dirChooser = 0

        directionNew = direction

        if dirChooser == 1:
            directionNew = (direction - 1) % 8
        elif dirChooser == 2:
            directionNew = (direction + 1) % 8

        if (dirChooser == lastDirChoice):
            if randint(0, 100) < randint(50, 80):
                directionNew = direction

        self.create_river(xNew, yNew, directionNew, distanceNew, counter - 1, counterStart, dirChooser)

        forkPercent = 0  # default

        if counter > counterStart * (5 / 6):
            forkPercent = randint(0, 8)
        elif counter > counterStart * (2 / 6):
            forkPercent = randint(0, 15)
        else:
            forkPercent = randint(0, 30)

        if randint(0, 100) < forkPercent:  # fork
            distanceNew2 = randint(2, 5)
            self.create_river(xNew, yNew, directionNew, distanceNew2, counter - 1, counterStart, dirChooser)

    def connect_towns(self, town_list):
        """
        Description
        -----------
        Returns a list containing town pairs to connect together.

        Params
        --------
        town_list - list of cells of CellTypes CellTypes.TOWN
        """
        closestTowns = self.find_closest_towns(town_list, town_list)
        return closestTowns

    def find_closest_towns(self, town_list, originaltown_list):
        """
        Description
        -----------
        Finds closest towns for each town in town_list and returns a list of town combinations without duplicates

        Params
        --------
        town_list - list of cells of CellTypes CellTypes.TOWN (changes during recursive calls)
        originaltown_list - list of cells of CellTypes CellTypes.TOWN (doesn't change)
        """
        shortestDistanceList = []
        connectedTown = []
        for Town in town_list:
            lastDifference = 0
            firstRound = True
            closestTownIndex = -1
            for secondTown in originaltown_list:
                if Town == secondTown:
                    pass
                else:
                    difference = math.sqrt((Town.x - secondTown.x)**2 + (Town.y - secondTown.y)**2)
                    if firstRound:
                        firstRound = False
                        lastDifference = difference
                    elif difference < lastDifference:
                        closestTownIndex = originaltown_list.index(secondTown)
                        lastDifference = difference
            connectedTown = [Town, originaltown_list[closestTownIndex]]
            shortestDistanceList.append(connectedTown)

        shortestDistanceListNoDuples = []
        for i in shortestDistanceList:
            if i not in shortestDistanceListNoDuples and [i[1], i[0]] not in shortestDistanceListNoDuples:
                shortestDistanceListNoDuples.append(i)

        for i in shortestDistanceListNoDuples:
            i[0].cell_type = CellTypes.CONNECTED_TOWN

        unconnectedTowns = []
        for town in originaltown_list:
            if town.cell_type == CellTypes.TOWN:
                unconnectedTowns.append(town)

        # Connect any towns that have no connections to nearest town
        if len(shortestDistanceListNoDuples) < len(town_list):
            for combo in self.find_closest_towns(unconnectedTowns, town_list):
                shortestDistanceListNoDuples.append(combo)

    #    # TEST: Connect towns that only have one connection
    #    singleConnectionTowns = []
#
    #    if town_list == originaltown_list: # If first call
    #        for town in town_list:
    #            totConnections = 0
    #            for combo in shortestDistanceListNoDuples:
    #                if town in [combo[0], combo[1]]:
    #                    totConnections += 1
    #            if totConnections == 0:
    #                singleConnectionTowns.append(town)
    #                print(town)
    #
    #    for combo in self.find_closest_towns(singleConnectionTowns, singleConnectionTowns):
    #            shortestDistanceListNoDuples.append(combo)

        return shortestDistanceListNoDuples

    def path_finder(self, x0, y0, x1, y1):
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

        matrix = [[0] * len(self.grid) for i in range(len(self.grid))]

        for column in self.grid:
            for cell in column:
                if cell.cell_type in [CellTypes.LAND3, CellTypes.LAND4, CellTypes.LAND5, ]:
                    matIn = 0  # obstacles
                elif self.check_if_water(cell) or cell.cell_type in [CellTypes.SAND, CellTypes.RIVER_BANK, ]:
                    matIn = 5  # water, only cross this if necessary
                elif cell.cell_type in [CellTypes.ROAD_DIRT, ]:
                    matIn = 1  # use existing roads when possible
                else:
                    matIn = 2  # free spaces
                matrix[cell.y][cell.x] = matIn

        pathGrid = Grid(matrix=matrix)

        # Find a path
        start = pathGrid.node(x0, y0)
        end = pathGrid.node(x1, y1)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        path, runs = finder.find_path(start, end, pathGrid)

        # Return the path
        return path

    def create_road(self, x, y, direction, distance, counter, counterStart, lastDirChoice):
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

        if counter <= 0 and not self.check_if_water(self.grid[x][y]):

            if randint(0, 100) < 50 and int(counterStart / 2) > 5:
                directionNew = randint(0, 7)
                distanceNew = randint(2, 3)
                self.create_road(x, y, directionNew, distanceNew, int(counterStart / 2), int(counterStart / 2), 0)  # Make roads
                self.create_road(x, y, (directionNew + 2) % 8, distanceNew, int(counterStart / 2), int(counterStart / 2), 0)  # Make roads

            self.grid[x][y].cell_type = CellTypes.TOWN

            return

        # New coords for next line
        offsets = self.get_directionCoordinates(direction)

        xNew = x + offsets[0] * distance
        yNew = y + offsets[1] * distance

        for i in range(distance):
            # Check to ensure x and y location written is within the grid
            if (
                (x + i * offsets[0]) in range(0, len(self.grid)) and (y + i * offsets[1]) in range(0, len(self.grid[0]))
            ):
                if self.check_if_water(self.grid[x + i * offsets[0]][y + i * offsets[1]]):
                    self.grid[x + i * offsets[0]][y + i * offsets[1]].CellTypes = CellTypes.BRIDGE_WOOD  # Bridge over water
                else:
                    self.grid[x + i * offsets[0]][y + i * offsets[1]].CellTypes = CellTypes.ROAD_DIRT   # Land-based dirt road

        # Repeat with new line
        if not ((xNew) in range(0, len(self.grid)) and (yNew) in range(0, len(self.grid[0]))):
            return

        surroundingEndList = self.get_surrounding_cells_info(xNew, yNew, 1)
        for cell in surroundingEndList:
            if cell.cell_type == CellTypes.WATER:
                return

        # if randint(0,100) > 1:
        distanceNew = randint(2, 3)
        dirChooser = randint(0, 5)

        if dirChooser not in [1, 2]:
            dirChooser = 0

        directionNew = direction

        if dirChooser == 1:
            directionNew = (direction - 1) % 8
        elif dirChooser == 2:
            directionNew = (direction + 1) % 8

        if (dirChooser == lastDirChoice):
            if randint(0, 100) < randint(10, 20):
                directionNew = direction

        self.create_road(xNew, yNew, directionNew, distanceNew, counter - 1, counterStart, dirChooser)

        forkPercent = 4  # 0 # default

        if randint(0, 100) < forkPercent:
            distanceNew2 = randint(2, 5)
            self.create_road(xNew, yNew, directionNew, distanceNew2, counter - 1, counterStart, dirChooser)

    def draw(self):
        """
        Description
        -----------
        Draw the grid to the window

        """
        for column in self.grid:
            for cell in column:
                cell.draw()
    #    for townCombo in self.closesttown_list: # Draw lines between connected towns
    #        self.create_line(townCombo[0].x*pixelsPerCell+int(pixelsPerCell/2),
    #        townCombo[0].y*pixelsPerCell+int(pixelsPerCell/2),
    #        townCombo[1].x*pixelsPerCell+int(pixelsPerCell/2),
    #        townCombo[1].y*pixelsPerCell+int(pixelsPerCell/2),)
