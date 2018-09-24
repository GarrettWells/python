from abc import ABC, abstractmethod
from typing import Tuple, List

from SortingList import SortingList


class SortingAlgorithm(ABC):
    """Abstract Base Class of sorting algorithms"""

    CURRENT_BLOCK = "current block"
    PROPOSED_NEXT_BLOCK = "proposed_next_block"
    COMPLETED_BLOCK = "completed block"
    BLOCK = "block"
    RESET_BLOCK = "reset_block"

    def __init__(self, list_: SortingList):
        self.list = list_

    @abstractmethod
    def __sort__(self):
        pass

    @abstractmethod
    def single_pass(self) -> list:
        """Run the sort method until a single element is moved to the correct index"""
        pass

    @abstractmethod
    def single_compare(self) -> List[Tuple[list, list, str]]:
        """Process a single comparison of the sort method

        :return: 3-tuple where
                the first element is the index
                the second element is the height
                the third element is the type of block to draw represented by a color in RGB
        """
        pass

    def initialize_display(self) -> List[Tuple[int, int, str]]:
        to_return = []
        for i in range(len(self.list)):
            to_return.append((i, self.list.get_height(i), SortingAlgorithm.BLOCK))
        return to_return

    def swap(self, index1, index2):
        temp = self.list.get_height(index1)
        self.list[index1] = self.list[index2]
        self.list[index2] = temp
