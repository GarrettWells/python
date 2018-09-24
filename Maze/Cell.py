class Cell(object):
    """A Cell is defined as any space in the maze

    This class makes no distinction between player cells, open cells, or undiscovered cells
    """
    def __init__(self, cords, has_right_wall=True, has_bottom_wall=True, has_left_wall=True, has_top_wall=True):
        self.x = cords[0]
        self.y = cords[1]
        self._has_right_wall = has_right_wall
        self._has_bottom_wall = has_bottom_wall
        self._has_left_wall = has_left_wall
        self._has_top_wall = has_top_wall
        self.visited = False

    def has_right_wall(self) -> bool:
        return self._has_right_wall

    def has_bottom_wall(self) -> bool:
        return self._has_bottom_wall

    def has_left_wall(self) -> bool:
        return self._has_left_wall

    def has_top_wall(self) -> bool:
        return self._has_top_wall

    def destroy_right_wall(self):
        self._has_right_wall = False

    def destroy_bottom_wall(self):
        self._has_bottom_wall = False

    def destroy_left_wall(self):
        self._has_left_wall = False

    def destroy_top_wall(self):
        self._has_top_wall = False

    def is_visited(self) -> bool:
        """Checks if the Cell is visited"""
        return self.visited

    def set_visited(self):
        """Marks the Cell as visited"""
        self.visited = True

    def get_xy(self) -> (int, int):
        """Returns the (x, y) position of the Cell"""
        return self.x, self.y

    def reset_visited(self):
        self.visited = False

    def convert_cell_to_solvable(self) -> 'SolvableCell':
        return SolvableCell((self.x, self.y), self.has_right_wall(), self.has_bottom_wall()
                            , self.has_left_wall(), self.has_top_wall())


class SolvableCell(Cell):
    """A Solvable Cell is the same a a regular Cell but also keeps track of the Cell the player came from to get there"""
    def __init__(self, cords, has_right_wall=True, has_bottom_wall=True, has_left_wall=True, has_top_wall=True):
        super().__init__(cords, has_right_wall, has_bottom_wall, has_left_wall, has_top_wall)
        self.previous_cell = None

    def set_previous_cell(self, cell):
        self.previous_cell = cell

    def get_previous_cell(self):
        return self.previous_cell