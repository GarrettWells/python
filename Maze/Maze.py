from __future__ import annotations
from abc import ABC

from config import N_ROWS, N_COLS
from Cell import *


class Maze(ABC):

    def __init__(self):
        self.maze = None

    def destroy_right_wall(self, cords):
        if cords[0] == N_COLS - 1:
            raise Exception('cannot destroy right wall')
        else:
            self.maze[cords[0]][cords[1]].destroy_right_wall()
            self.maze[cords[0]+1][cords[1]].destroy_left_wall()

    def destroy_bottom_wall(self, cords):
        if cords[1] == N_ROWS - 1:
            raise Exception('cannot destroy bottom wall')
        else:
            self.maze[cords[0]][cords[1]].destroy_bottom_wall()
            self.maze[cords[0]][cords[1]+1].destroy_top_wall()

    def destroy_left_wall(self, cords):
        if cords[0] == 0:
            raise Exception('cannot destroy left wall')
        else:
            self.maze[cords[0]][cords[1]].destroy_left_wall()
            self.maze[cords[0]-1][cords[1]].destroy_right_wall()

    def destroy_top_wall(self, cords):
        if cords[1] == 0:
            raise Exception('cannot destroy top wall')
        else:
            self.maze[cords[0]][cords[1]].destroy_top_wall()
            self.maze[cords[0]][cords[1]-1].destroy_bottom_wall()

    def reset_visited_all(self):
        """Set all cells of the maze to unvisited"""
        for i in range(N_COLS):
            for j in range(N_ROWS):
                self.maze[i][j].reset_visited()

    def get_cell(self, coords, x_adjust=0, y_adjust=0):
        """Returns the Cell at indicated coordinates

        The return type varies by subclass"""
        x, y = coords
        return self.maze[x + x_adjust][y + y_adjust]


class IncompleteMaze(Maze):
    def __init__(self):
        super().__init__()
        self.maze = [None] * N_COLS
        for i in range(N_COLS):
            self.maze[i] = [None] * N_ROWS
            for j in range(N_ROWS):
                self.maze[i][j] = Cell((i, j))

    def convert_to_SolvableMaze(self) -> SolvableMaze:
        """converts this IncompleteMaze to a SolvableMaze"""
        return SolvableMaze(self.maze)

    def get_cell(self, coords, x_adjust=0, y_adjust=0) -> Cell:
        return super().get_cell(coords, x_adjust, y_adjust)


class SolvableMaze(Maze):
    def __init__(self, maze):
        super().__init__()
        self.maze = maze
        if type(self.maze[0][0]) is Cell:
            for i in range(N_COLS):
                for j in range(N_ROWS):
                    self.maze[i][j] = self.maze[i][j].convert_cell_to_solvable()

    def get_cell(self, coords, x_adjust=0, y_adjust=0) -> SolvableCell:
        return super().get_cell(coords, x_adjust, y_adjust)
