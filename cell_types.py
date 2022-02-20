from enum import Enum


class Water(Enum):
    WATER_0 = 0
    DEEP_WATER_0 = 1
    DEEP_WATER_1 = 2
    DEEP_WATER_2 = 3
    DEEP_WATER_3 = 4
    RIVER_WATER_0 = 5
    RIVER_WATER_1 = 6
    RIVER_WATER_2 = 7


class WaterGeneration(Enum):
    WATER_START = 0
    RIVER_HEAD = 1


class Land(Enum):
    LAND_0 = 0
    LAND_1 = 1
    LAND_2 = 2
    LAND_3 = 3
    LAND_4 = 4
    LAND_5 = 5
    SAND_0 = 6
    RIVER_BANK = 7


class Desert(Enum):
    DESERT_0 = 0
    DESERT_1 = 1
    DESERT_2 = 2


class Plant(Enum):
    TREE_0 = 0


class Town(Enum):
    TOWN = 0
    CONNECTED_TOWN = 1


class Road(Enum):
    ROAD_DIRT = 0
    BRIDGE_WOOD = 1


class Snow(Enum):
    LAND_SNOW0 = 0
    LAND_SNOW1 = 1
    LAND_SNOW2 = 2


class CellTypes(Enum):
    '''
    This class represents the types of cells available in the map.
    '''
    water = Water
    water_generation = WaterGeneration
    land = Land
    desert = Desert
    plant = Plant
    town = Town
    road = Road
    snow = Snow
