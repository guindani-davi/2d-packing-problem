from models.solution import Solution
from models.bin import Bin


class GraspSolution(Solution):
    def __init__(self, default_bin: Bin, max_bins: int, alpha: int):
        super().__init__(default_bin, max_bins)
        self.alpha = alpha

    def __str__(self):
        output = []
        for i, bin in enumerate(self.bins):
            output.append(f"Bin {i + 1}:")
            for rectangle in bin.rectangles:
                output.append(f"  {rectangle}")
        
        output.append(f"Sum of squared rectangles: {self.calculate_sum_of_squared_rectangules()}")
        return "\n".join(output)