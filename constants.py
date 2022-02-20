from cell_types import CellTypes

size_horizontal = 1500
size_vertical = 950

pixels_per_cell = 4

# Number of columns directly coorelates to the x position of the grid
num_cols = int(size_horizontal / pixels_per_cell)

# Number of rows directly coorelates to the y position of the grid
num_rows = int(size_vertical / pixels_per_cell)

max_towns = 5  # 10
town_min_distance = 20

water_cells = [
    CellTypes.WATER,
    CellTypes.DEEP_WATER0,
    CellTypes.DEEP_WATER1,
    CellTypes.DEEP_WATER2,
    CellTypes.DEEP_WATER3,
    CellTypes.RIVER_WATER1,
    CellTypes.RIVER_WATER2,
    CellTypes.RIVER_WATER3
]
