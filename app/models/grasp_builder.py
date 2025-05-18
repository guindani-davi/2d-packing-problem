import random
from abc import ABC

from models.grasp_solution import GraspSolution
from models.solution import Solution
from models.bin import Bin
from models.rectangle import Rectangle

class GraspBuilder(ABC):
    @staticmethod
    def first_fit(solution: Solution, rectangle: Rectangle) -> Solution:
        placed = False
        for current_bin in solution.bins:
            position, rotated = current_bin.find_first_fit_position(rectangle)
            if position is not None:
                x, y = position
                if rotated:
                    rectangle.rotate()
                current_bin.place_rectangle(rectangle, x, y)
                placed = True
                break
        
        if not placed:
            new_bin = Bin(solution.default_bin.width, solution.default_bin.height)
            position, rotated = new_bin.find_first_fit_position(rectangle)
            if position is not None:
                x, y = position
                if rotated:
                    rectangle.rotate()
                new_bin.place_rectangle(rectangle, x, y)
                solution.bins.append(new_bin)

        return solution

    @staticmethod
    def build(solution: GraspSolution, rectangles: list[Rectangle]) -> GraspSolution:
        while len(rectangles) > 0:
            # Criar LCR (Lista de Candidatos Restrita)
            areas = [rectangle.area for rectangle in rectangles]
            Cmax = max(areas)
            Cmin = min(areas)
            threshold = Cmax - solution.alpha * (Cmax - Cmin)
            
            lcr = [rectangle for rectangle in rectangles if rectangle.area >= threshold]
            
            chosen_rectangle = random.choice(lcr)
            rectangles.remove(chosen_rectangle)
            solution = GraspBuilder.first_fit(solution, chosen_rectangle)
        
        return solution
    
    @staticmethod
    def objective_function(solution: GraspSolution) -> float:
        return len(solution.bins) * 100000 - solution.calculate_sum_of_squared_rectangules()