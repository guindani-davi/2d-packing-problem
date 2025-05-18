from abc import ABC, abstractmethod

from models.bin import Bin

class Solution(ABC):
    def __init__(self, default_bin: Bin):
        self.bins: list[Bin] = []
        self.default_bin = default_bin

    def calculate_sum_of_squared_rectangules(self):
        return sum(len(bin.rectangles) ** 2 for bin in self.bins)
    
    @abstractmethod
    def __str__(self):
        pass