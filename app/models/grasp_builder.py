import random, copy
from abc import ABC

from models.grasp_solution import GraspSolution
from models.solution import Solution
from models.bin import Bin
from models.rectangle import Rectangle
from models.objective_function import objective_function

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
    def local_search(solution: GraspSolution, rectangles: list[Rectangle]) -> tuple[GraspSolution, float, list[Rectangle]]:
        best_solution = copy.deepcopy(solution)
        best_value = objective_function(best_solution)
        best_solution_rectangles = copy.deepcopy(rectangles)

        local_peek = False
        while(not local_peek):
            for i in range(1, len(best_solution_rectangles)):
                current_rectangles = copy.deepcopy(best_solution_rectangles)
                current_rectangles[0], current_rectangles[i] = current_rectangles[i], current_rectangles[0]
                current_solution = GraspSolution(best_solution.default_bin, best_solution.alpha, best_solution.number)
                current_solution = GraspBuilder.build(current_solution, current_rectangles)

                if objective_function(current_solution) < best_value:
                    print("Local search found a better solution")
                    best_value = objective_function(current_solution)
                    best_solution = copy.deepcopy(current_solution)
                    best_solution_rectangles = copy.deepcopy(current_rectangles)
                    print("Best solution:", best_solution)
                    print("Objective function value:", best_value)
                    break

            local_peek = True

        return best_solution, best_solution_rectangles