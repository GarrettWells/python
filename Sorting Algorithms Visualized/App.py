# Garrett Wells
# 9-7-2018
#
# This program visually displays various sorting algorithms
#
# Requires Python 3.6 or higher
# Requires Pygame 1.9.4 or higher

from typing import Tuple
import sys

import pygame

from config import *
from sortingalgs import *
from SortingList import SortingList


class App:
    BUBBLE_SORT = BubbleSort(SortingList(NUM_BLOCKS))
    SELECTION_SORT = SelectionSort(SortingList(NUM_BLOCKS))

    def __init__(self):
        pygame.init()
        self.sorting_alg = self.BUBBLE_SORT  # selects the sorting algorithm
        self._running = True
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        for block in self.sorting_alg.initialize_display():  # wipe the screen
            self.draw_block(block)
        self.refresh()
        self._run()

    def _run(self):
        to_draw = []  # the blocks in the image that must be drawn
        while self._running:
            for event in pygame.event.get():
                self._on_event(event)
            for index, height, color in to_draw:  # these are the blocks that were carried over from the last iteration
                if color != SortingAlgorithm.COMPLETED_BLOCK:  # any completed block shouldn't be draw over
                    self.draw_block((index, height, SortingAlgorithm.BLOCK))

            to_draw = self.sorting_alg.single_compare()

            for block in to_draw:  # new blocks that should be drawn
                self.draw_block(block)
            App.refresh()
            if len(to_draw) == 0:  # if we did nothing this iteration then we are done
                self._running = False
        while True:
            for event in pygame.event.get():  # wait for the user to exit
                self._on_event(event)

    @staticmethod
    def _on_event(event):
        if event.type == pygame.QUIT:  # press the X in the top right
            App._cleanup()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # press ESC
                App._cleanup()

    @staticmethod
    def _cleanup():
        """Quit the program"""
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    @staticmethod
    def refresh():
        """Refesh the screen"""
        pygame.event.pump()
        pygame.display.update()

    def draw_block(self, to_draw: Tuple[int, int, str]):
        """draws a single block. Should be called after single compare

        :param: 3-tuple where
                    the first element is the index
                    the second element is the height
                    the third element is the type of block to draw represented in RGB
        """
        index, height, color = to_draw
        x = index * BLOCK_WIDTH
        y = (height+1) * BLOCK_HEIGHT_UNIT  # a block with a height of 0 should be 1 BLOCK_HEIGHT_UNIT high
        surface = pygame.Surface((BLOCK_WIDTH, y))
        surface.fill(self.get_color(color))
        reset_surface = pygame.Surface((BLOCK_WIDTH, SCREEN_HEIGHT))
        reset_surface.fill(self.get_color(SortingAlgorithm.RESET_BLOCK))
        self.screen.blit(reset_surface, (x, 0))  # clear the old surface before adding the new
        self.screen.blit(surface, (x, SCREEN_HEIGHT-y))

    @staticmethod
    def get_color(color: str) -> Tuple[int, int, int]:
        """Converts a predefined string into a RGB color

        @:param: predefined string
        @:returns: 3-tuple that represents a RGB color"""
        if color == SortingAlgorithm.RESET_BLOCK: return (0, 0, 0)
        elif color == SortingAlgorithm.BLOCK: return (255, 255, 255)
        elif color == SortingAlgorithm.CURRENT_BLOCK: return (128, 128, 255)
        elif color == SortingAlgorithm.COMPLETED_BLOCK: return (255, 255, 0)
        elif color == SortingAlgorithm.PROPOSED_NEXT_BLOCK: return (128, 0, 0)
        else:
            raise Exception("unknown color")
App()
