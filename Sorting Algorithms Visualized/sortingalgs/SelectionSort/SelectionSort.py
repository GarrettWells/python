from typing import List, Tuple

from sortingalgs import SortingAlgorithm
from sortingalgs.SelectionSort.SortingAlgListNoDup import SortingAlgListNoDup


class SelectionSort(SortingAlgorithm):

    def __init__(self, list_):
        super().__init__(list_)
        self.index = 0
        self.proposed_next = 0
        self.out_of_place = len(self.list)

    def __sort__(self):
        pass

    def single_pass(self) -> list:
        pass

    def single_compare(self) -> List[Tuple[int, int, str]]:
        if self.out_of_place <= 1:  # only 1 item left to sort
            if self.out_of_place == 0:  # we are done
                return []
            self.out_of_place = 0
            return [(0, self.list.get_height(0), SortingAlgorithm.COMPLETED_BLOCK)]  # change last block
        elif self.index >= self.out_of_place:  # found the next smallest/largest
            self.swap(self.proposed_next, self.out_of_place-1)
            to_return = SortingAlgListNoDup(
                                (self.proposed_next, self.list.get_height(self.proposed_next), SortingAlgorithm.BLOCK)
                              , (self.out_of_place-1, self.list.get_height(self.out_of_place-1), SortingAlgorithm.COMPLETED_BLOCK)
                                )
            self.out_of_place -= 1
            self.proposed_next = 0
            self.reset_index()
            return to_return
        else:  # still trying to find the next smallest/largest
            if self.need_to_swap(self.index, self.proposed_next):  # found a new proposed_next
                self.proposed_next = self.index
                to_return = [(self.proposed_next, self.list.get_height(self.proposed_next), self.CURRENT_BLOCK)
                             , (self.index, self.list.get_height(self.index), self.PROPOSED_NEXT_BLOCK)]
            else:  # didn't find a new proposed_next
                to_return = [(self.index, self.list.get_height(self.index), self.CURRENT_BLOCK),
                             (self.proposed_next, self.list.get_height(self.proposed_next), self.PROPOSED_NEXT_BLOCK)]
            self.index += 1
            return to_return

    def need_to_swap(self, index1, index2) -> bool:
        return self.list.get_height(index1) > self.list.get_height(index2)

    def reset_index(self):
        self.index = 0
