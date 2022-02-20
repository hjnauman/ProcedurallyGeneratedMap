from cell_types import CellTypes


class Cell():
    def __init__(self, master, x, y, size, cell_type):
        self.master = master
        self.x = x
        self.y = y
        self.size = size
        self.cell_type = cell_type

    def getCellColor(self):
        """
        Description
        -----------
        Get cell color from CellTypes
        """
        # Default color
        color = 'white'

        if self.cell_type == CellTypes.land.value.LAND_0:
            color = 'green'

        elif self.cell_type == CellTypes.water.value.WATER_0:
            color = '#0074D3'

        elif self.cell_type == CellTypes.water_generation.value.WATER_START:
            color = 'black'

        elif self.cell_type == CellTypes.water.value.DEEP_WATER_0:
            color = '#0B62E6'

        elif self.cell_type == CellTypes.water.value.DEEP_WATER_1:
            color = '#2059DA'

        elif self.cell_type == CellTypes.water.value.DEEP_WATER_2:
            color = '#2855B7'

        elif self.cell_type == CellTypes.water.value.DEEP_WATER_3:
            color = '#2E519B'

        elif self.cell_type == CellTypes.land.value.SAND_0:
            color = 'tan'

        elif self.cell_type == CellTypes.water_generation.value.RIVER_HEAD:
            color = 'DodgerBlue4'

        elif self.cell_type == CellTypes.water.value.RIVER_WATER_0:
            color = '#0074D3'  # '#0074D3' 'red' '#0074D3'

        elif self.cell_type == CellTypes.water.value.RIVER_WATER_1:
            color = '#0077E2'  # '#0077E2' 'salmon' '#0074D3'

        elif self.cell_type == CellTypes.water.value.RIVER_WATER_2:
            color = '#027EDE'  # '#027EDE' 'light pink' '#0074D3'

        elif self.cell_type == CellTypes.land.value.LAND_1:
            color = 'forest green'

        elif self.cell_type == CellTypes.land.value.LAND_2:
            color = 'olive drab'

        elif self.cell_type == CellTypes.land.value.LAND_3:
            color = 'burlywood4'

        elif self.cell_type == CellTypes.land.value.LAND_4:
            color = '#9E805B'

        elif self.cell_type == CellTypes.land.value.LAND_5:
            color = '#AD9270'

        elif self.cell_type == CellTypes.land.value.RIVER_BANK:
            color = '#346B23'  # 'chartreuse4'

        elif self.cell_type == CellTypes.plant.value.TREE_0:
            color = 'dark green'

        elif self.cell_type == CellTypes.town.value.TOWN:
            color = 'black'

        elif self.cell_type == CellTypes.road.value.ROAD_DIRT:
            color = 'saddle brown'

        elif self.cell_type == CellTypes.road.value.BRIDGE_WOOD:
            color = 'dark goldenrod'

        return color

    def draw(self):
        """
        Description
        -----------
        Draw current cell to the window
        """
        if self.master is not None:
            x_min = self.x * self.size
            x_max = x_min + self.size
            y_min = self.y * self.size
            y_max = y_min + self.size

            color = self.getCellColor()

            # self.master.create_rectangle(x_min, y_min, x_max, y_max, fill = fill, outline = outline)
            # if self.x % 2 == 0:
            self.master.create_rectangle(x_min, y_min, x_max, y_max, fill=color, width=0)
            # else:
            #    self.master.create_rectangle(x_min, y_min + self.size/2, x_max, y_max + self.size/2, fill=color, width=0)
            # if self.x % 2 == 0:
            #     self.master.create_oval(x_min - 20, y_min - 20, x_max + 20, y_max + 20, fill=color, width=0)
            # else:
            #     self.master.create_oval(x_min - 20, y_min - 30, x_max + 20, y_max - 10, fill=color, width=0)
