from typing import Tuple

from sortingalgs import SortingAlgorithm


class SortingAlgListNoDup(list):
    """This class should be used with the sorting algorithms to avoid passing duplicate entries to App.py. A duplicate
    is any 2 entries that have the same index."""

    def __init__(self, *args):
        super().__init__()
        for arg in args:
            self.append(arg)

    def append(self, entry: Tuple[list, list, Tuple[int, int, int]]):
        index, height, rgb = entry
        for existing_entry in self:
            existing_index, _, existing_rgb = existing_entry
            if existing_index == index:
                if rgb == SortingAlgorithm.COMPLETED_BLOCK:
                    self.remove(existing_entry)
                    super().append(entry)
                break
        super().append(entry)
