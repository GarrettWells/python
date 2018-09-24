import random

from RunnerType import *
from Maze import *
from Data_Structures import *

from config import N_COLS, N_ROWS


class MazeRunner(ABC):

    def __init__(self):
        self._runner = None
        self._maze = None

    @abstractmethod
    def get_maze(self):
        """Returns the maze

        return type varies by subclass"""
        return self._maze

    def get_xy(self) -> tuple:
        """Returns the (x, y) coordinate of the maze runner."""
        return self._runner.get_xy()

    @abstractmethod
    def process_movement(self):
        """Moves the player 1 Cell"""
        pass

    @abstractmethod
    def get_valid_movement(self) -> set:
        """Returns a list of the valid directions"""
        pass


class MazeCreatingAlgs_SinglePathSolution(MazeRunner):
    """Maze creating algorithms used to create a maze with a single solution"""
    def __init__(self):
        super().__init__()
        self._runner = MazeCreatingBot()
        self._maze = IncompleteMaze()
        self._traveled_directions = Stack()

    def get_valid_movement(self) -> set:
        valid_directions = set()
        x, y = self.get_xy()
        if x != N_COLS-1 and not self._maze.get_cell(self.get_xy(), x_adjust=1).is_visited():  # check right
            valid_directions.add('right')
        if y != N_ROWS-1 and not self._maze.get_cell(self.get_xy(), y_adjust=1).is_visited():  # check below
            valid_directions.add('down')
        if x != 0 and not self._maze.get_cell(self.get_xy(), x_adjust=-1).is_visited():  # check left
            valid_directions.add('left')
        if y != 0 and not self._maze.get_cell(self.get_xy(), y_adjust=-1).is_visited():  # check above
            valid_directions.add('up')
        return valid_directions

    def get_maze(self) -> IncompleteMaze:
        return super().get_maze()

    @abstractmethod
    def process_movement(self):
        """Move the player one Cell"""
        pass


class MazeCreatingAlg_SinglePathSolution1(MazeCreatingAlgs_SinglePathSolution):
    """Single path maze creating algorithm 1"""
    def __init__(self):
        super().__init__()

    def process_movement(self) -> bool:
        self._maze.get_cell(self.get_xy()).set_visited()
        valid_directions = self.get_valid_movement()  # get which directions are valid
        if len(valid_directions) > 0:  # if there is a valid direction
            choice = random.sample(valid_directions, 1)[0]  # choose a random valid direction to move
            valid_directions.remove(choice)
            self._traveled_directions.add(choice)
            if choice == 'right':
                self._maze.destroy_right_wall(self.get_xy())
                self._runner.move_right()
            elif choice == 'down':
                self._maze.destroy_bottom_wall(self.get_xy())
                self._runner.move_down()
            elif choice == 'left':
                self._maze.destroy_left_wall(self.get_xy())
                self._runner.move_left()
            elif choice == 'up':
                self._maze.destroy_top_wall(self.get_xy())
                self._runner.move_up()
            else:
                raise Exception('no _maze_runner movement was chosen')
            return True

        else:  # if there were no valid directions
            if self._traveled_directions.size() == 0:  # if we are back at the start
                return False  # we are finished
            else:
                movement = self._traveled_directions.remove()  # go back the way you came
                if movement == 'left':
                    self._runner.move_right()
                elif movement == 'up':
                    self._runner.move_down()
                elif movement == 'right':
                    self._runner.move_left()
                elif movement == 'down':
                    self._runner.move_up()
            return True


class MazeSolvingAlg(MazeRunner):
    """Maze solving algorithm"""
    def __init__(self, search_mode, maze):
        super().__init__()
        self._maze = maze
        self._runner = MazeSolvingBot()

        if search_mode == 'BFS':  # Bredth-First Search
            self._need_to_visit_cells = Queue()
        elif search_mode == 'DFS':  # Depth-First Search
            self._need_to_visit_cells = Stack()
        else:
            raise Exception('unknown search pattern')

    def get_valid_movement(self) -> set:
        coordinates = set()
        x, y = self.get_xy()
        curr_cell = self.get_maze().get_cell((x, y))

        # Checks if the Current cell has a wall in the corresponding spot, then checks
        # if the Cell on the other side of the wall has been visited.
        right_coord = (x + 1, y)
        lower_coord = (x, y + 1)
        left_coord = (x - 1, y)
        upper_coord = (x, y - 1)

        # if there is no wall to the (direction) and Cell to the (direction) is not visited
        if not curr_cell.has_right_wall() and not self.get_maze().get_cell(right_coord).is_visited():
            self.get_maze().get_cell(right_coord).set_previous_cell(curr_cell)  # set the correct previous cell
            coordinates.add(right_coord)
        if not curr_cell.has_bottom_wall() and not self.get_maze().get_cell(lower_coord).is_visited():
            self.get_maze().get_cell(lower_coord).set_previous_cell(curr_cell)  # set the correct previous cell
            coordinates.add(lower_coord)
        if not curr_cell.has_left_wall() and not self.get_maze().get_cell(left_coord).is_visited():
            self.get_maze().get_cell(left_coord).set_previous_cell(curr_cell)  # set the correct previous cell
            coordinates.add(left_coord)
        if not curr_cell.has_top_wall() and not self.get_maze().get_cell(upper_coord).is_visited():
            self.get_maze().get_cell(upper_coord).set_previous_cell(curr_cell)  # set the correct previous cell
            coordinates.add(upper_coord)
        return coordinates

    def process_movement(self):
        self._maze.get_cell(self.get_xy()).set_visited()
        valid_directions = self.get_valid_movement()
        for direction in valid_directions:
            self._need_to_visit_cells.add(direction)
        next_coords = self._need_to_visit_cells.remove()
        self.move_to(self.get_maze().get_cell(next_coords))

    def get_escape_path(self) -> Stack:
        """returns the escape path from start to finish"""
        path = Stack()
        curr_cell = self.get_maze().get_cell(self.get_xy())
        while curr_cell.get_xy() != (0, 0):
            path.add(curr_cell)
            curr_cell = curr_cell.get_previous_cell()
        path.add(self.get_maze().get_cell((0, 0)))
        return path

    def get_maze(self) -> SolvableMaze:
        return super().get_maze()

    def move_to(self, cell: SolvableCell):
        """move to the indicated cell"""
        self._runner.move_to(cell.get_xy())
