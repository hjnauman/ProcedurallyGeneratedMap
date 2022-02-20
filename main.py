from tkinter import *
from cell_grid import CellGrid
from biomes import Biomes
from constants import *
from random import randint

if __name__ == "__main__":
    app = Tk()
    infection_rate = randint(90, 100)

    grid = CellGrid(app, num_rows, num_cols, pixels_per_cell, infection_rate, Biomes.PLAINS)
    grid.pack()

    app.mainloop()
