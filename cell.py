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

        if self.cell_type == CellTypes.LAND:
            color = 'green'

        elif self.cell_type == CellTypes.WATER:
            color = '#0074D3'

        elif self.cell_type == CellTypes.WATER_START:
            color = 'black'

        elif self.cell_type == CellTypes.DEEP_WATER0:
            color = '#0B62E6'

        elif self.cell_type == CellTypes.DEEP_WATER1:
            color = '#2059DA'

        elif self.cell_type == CellTypes.DEEP_WATER2:
            color = '#2855B7'

        elif self.cell_type == CellTypes.DEEP_WATER3:
            color = '#2E519B'

        elif self.cell_type == CellTypes.SAND:
            color = 'tan'

        elif self.cell_type == CellTypes.RIVER_HEAD:
            color = 'DodgerBlue4'

        elif self.cell_type == CellTypes.RIVER_WATER1:
            color = '#0074D3'  # '#0074D3' 'red' '#0074D3'

        elif self.cell_type == CellTypes.RIVER_WATER2:
            color = '#0077E2'  # '#0077E2' 'salmon' '#0074D3'

        elif self.cell_type == CellTypes.RIVER_WATER3:
            color = '#027EDE'  # '#027EDE' 'light pink' '#0074D3'

        elif self.cell_type == CellTypes.LAND1:
            color = 'forest green'

        elif self.cell_type == CellTypes.LAND2:
            color = 'olive drab'

        elif self.cell_type == CellTypes.LAND3:
            color = 'burlywood4'

        elif self.cell_type == CellTypes.LAND4:
            color = '#9E805B'

        elif self.cell_type == CellTypes.LAND5:
            color = '#AD9270'

        elif self.cell_type == CellTypes.RIVER_BANK:
            color = '#346B23'  # 'chartreuse4'

        elif self.cell_type == CellTypes.TREE0:
            color = 'dark green'

        elif self.cell_type == CellTypes.TOWN:
            color = 'black'

        elif self.cell_type == CellTypes.ROAD_DIRT:
            color = 'saddle brown'

        elif self.cell_type == CellTypes.BRIDGE_WOOD:
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
            self.master.create_rectangle(x_min, y_min, x_max, y_max, fill=color, width=0)
            # self.master.create_oval(x_min-10, y_min-10, x_max+10, y_max+10, fill = color, width = 0)
