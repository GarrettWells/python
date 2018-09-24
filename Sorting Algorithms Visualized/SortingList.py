from random import shuffle


class SortingList(list):

    def __init__(self, size):
        super().__init__()
        for index in range(size):
            super().append(index)
        shuffle(self)

    def get_height(self, index: int) -> int:
        """Gets the height of the block at the desired index"""
        return self[index]