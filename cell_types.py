from enum import Enum


class CellTypes(Enum):
    '''
    This class represents the types of cells available in the map.
    '''
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
