# Garrett Wells
#
# This program creates a maze, then solves it and displays the solution
#
# Must use python 3.6 or higher
# Must use pygame 1.9.4 or higher
#
# Edit config.py to tweak the settings

import sys

import pygame

from MazeRunner import *
from config import *


class App(object):
    open_block_img = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
    open_block_img.fill((255, 255, 255))  # white
    vertical_bar_img = pygame.Surface((1, BLOCK_HEIGHT))
    vertical_bar_img.fill((0, 0, 0))  # black
    horizontal_bar_img = pygame.Surface((BLOCK_WIDTH, 1))
    horizontal_bar_img.fill((0, 0, 0))  # black
    player_img = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
    player_img.fill((128, 128, 255))  # light blue
    solved_path_img = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
    solved_path_img.fill((255, 128, 128))  # light red

    def __init__(self):
        self._running = True  # flag for if the program is running
        self._screen = None  # screen's canvas
        self._search_mode = 'DFS'
        self._robot = None

    def on_init(self):
        pygame.init()
        self._screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE)
        self._running = True

    def run(self):
        self._robot = MazeCreatingAlg_SinglePathSolution1()  # initialize the robot to a maze generating algorithm
        self.on_init()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            prev_pos = self._robot.get_xy()
            self._running = self._robot.process_movement()
            self.add_empty_space(prev_pos)
            self.add_player_space()
            self.refresh()
        maze = self._robot.get_maze().convert_to_SolvableMaze()
        maze.reset_visited_all()
        self._robot = MazeSolvingAlg(self._search_mode, maze)  # initialize the robot to a maze solving algorithm
        self._running = True
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            prev_path = self._robot.get_escape_path()  # gets the path from the robot's pre-movement position to the start
            self._robot.process_movement()
            new_path = self._robot.get_escape_path()  # gets the path from the robot's post-movement position to the start
            while prev_path.size() > 0:  # change all cells back to open to avoid random player cells throughout the maze
                self.add_empty_space(prev_path.remove().get_xy())
            while new_path.size() > 0:  # change the cells in new_path to player cells
                self.add_player_space(new_path.remove().get_xy())
            if self._robot.get_xy() == (N_COLS-1, N_ROWS-1):  # if the player found the exit
                self._running = False
            self.refresh()

        self.make_solved_path(self._robot.get_escape_path())  # indicate the found path out of the maze

        while True:  # wait for the user to exit the app
            for event in pygame.event.get():
                self.on_event(event)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._search_mode = 'DFS'
                print('using a Depth First Search algorithm')
            elif event.button == 3:
                self._search_mode = 'BFS'
                print('using a Breadth First Search algorithm')
            else:
                print('unknown search mode')
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_cleanup()
        elif event.type == pygame.QUIT:
            self.on_cleanup()

    @staticmethod
    def on_cleanup():  # called before exiting the app
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    @staticmethod
    def refresh():  # refesh the screen
        pygame.event.pump()
        pygame.display.update()

    def add_player_space(self, pos=None):
        if pos is None:
            x, y = self._robot.get_xy()
        else:
            x, y = pos
        self._screen.blit(App.player_img, (x * BLOCK_WIDTH, y * BLOCK_HEIGHT))
        self._add_borders((x, y))

    def add_solved_space(self, pos=None, include_borders=True):
        if pos is None:
            x, y = self._robot.get_xy()
        else:
            x, y = pos
        self._screen.blit(self.solved_path_img, (x * BLOCK_WIDTH, y * BLOCK_HEIGHT))
        if include_borders:
            self._add_borders((x, y))

    def add_empty_space(self, pos=None):
        if pos is None:
            x, y = self._robot.get_xy()
        else:
            x, y = pos
        self._screen.blit(self.open_block_img, (x * BLOCK_WIDTH, y * BLOCK_HEIGHT))
        self._add_borders((x, y))

    def _add_borders(self, pos):  # add the black boundaries that show the walls of the maze around a cell
        x, y = pos
        cell = self._robot.get_maze().get_cell(pos)
        if cell.has_right_wall():
            self._screen.blit(App.vertical_bar_img, ((x + 1) * BLOCK_WIDTH - 1, y * BLOCK_HEIGHT))  # right wall
        if cell.has_bottom_wall():
            self._screen.blit(App.horizontal_bar_img, (x * BLOCK_WIDTH, (y + 1) * BLOCK_HEIGHT - 1))  # bottom wall

        if x == 0:
            self._screen.blit(App.vertical_bar_img, (0, y * BLOCK_HEIGHT))  # left wall
        if y == 0:
            self._screen.blit(App.horizontal_bar_img, (x * BLOCK_WIDTH, 0))  # top wall

    def make_solved_path(self, queue, include_borders=True):
        """Displays the solution to the maze"""
        while queue.size() > 0:
            cell: SolvableCell = queue.remove()
            x, y = cell.get_xy()
            self.add_solved_space((x, y), include_borders)
            App.refresh()


if __name__ == '__main__':
    myApp = App()
    myApp.run()
