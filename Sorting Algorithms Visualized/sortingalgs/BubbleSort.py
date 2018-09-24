from typing import Tuple, List

from SortingList import SortingList
from sortingalgs.SortingAlgorithm import SortingAlgorithm


class BubbleSort(SortingAlgorithm):

    def __init__(self, list_: SortingList):
        super().__init__(list_)
        self.index = 1
        self.out_of_place = len(self.list)

    def __sort__(self):
        pass

    def single_pass(self) -> list:
        pass

    def single_compare(self) -> List[Tuple[int, int, str]]:
        if self.out_of_place <= 1:
            if self.out_of_place == 0:
                return []
            self.out_of_place = 0
            return [(0, self.list.get_height(0), SortingAlgorithm.COMPLETED_BLOCK)]  # we are done
        elif self.index >= self.out_of_place:  # done with a single pass
            self.reset_index()
            self.out_of_place -= 1
            return [(self.out_of_place, self.list.get_height(self.out_of_place), SortingAlgorithm.COMPLETED_BLOCK)]
        else:
            if self.need_to_swap(self.index-1, self.index):
                self.swap(self.index, self.index - 1)
            to_return = [(self.index - 1, self.list.get_height(self.index - 1), SortingAlgorithm.CURRENT_BLOCK),
                         (self.index, self.list.get_height(self.index), SortingAlgorithm.CURRENT_BLOCK)]
            self.index += 1
            return to_return

    def need_to_swap(self, index1, index2) -> bool:
        return self.list.get_height(index1) > self.list.get_height(index2)

    def reset_index(self):  # to avoid accidentally setting index to 0
        self.index = 1
