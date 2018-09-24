from abc import ABC


class RunnerType(ABC):
    y: int
    x: int

    def __init__(self):
        self.x = 0
        self.y = 0

    def move_right(self):
        self.x += 1

    def move_left(self):
        self.x -= 1

    def move_up(self):
        self.y -= 1

    def move_down(self):
        self.y += 1

    def get_xy(self) -> (int, int):
        """Returns the (x, y) position of the robot as a tuple"""
        return self.x, self.y

    def move_to(self, xy):
        """Moves the robot to the specified (x, y) position"""
        self.x = xy[0]
        self.y = xy[1]


class MazeCreatingBot(RunnerType):
    def __init__(self):
        super().__init__()


class MazeSolvingBot(RunnerType):
    def __init__(self):
        super().__init__()
