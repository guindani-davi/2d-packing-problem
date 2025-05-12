from abc import ABC


from models.bin import Bin


class Solution(ABC):
    def __init__(self, default_bin: Bin, max_bins: int):
        self.bins: list[Bin] = []
        self.default_bin = default_bin
        self.max_bins = max_bins

    def calculate_squared_occupancy_mean(self):
        return sum(bin.calculate_occupancy() ** 2 for bin in self.bins)