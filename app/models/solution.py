from abc import ABC


from models.bin import Bin


class Solution(ABC):
    def __init__(self, default_bin: Bin, max_bins: int):
        self.bins: list[Bin] = []
        self.default_bin = default_bin
        self.max_bins = max_bins

    def calculate_sum_of_squared_rectangules(self):
        return sum(len(bin.rectangles) ** 2 for bin in self.bins)