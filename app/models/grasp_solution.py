from solution import Solution
from app.models.bin import Bin


class GraspSolution(Solution):
    def __init__(self, default_bin: Bin, max_bins: int, alpha: int):
        super().__init__(default_bin, max_bins)
        self.alpha = alpha