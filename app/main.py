import random


from models.grasp_solution import GraspSolution
from models.solution import Solution
from models.rectangle import Rectangle
from models.bin import Bin
from helpers import read_input_file

def first_fit(solution: Solution, rectangle: Rectangle) -> Solution:

    if len(solution.bins) < solution.max_bins:
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

def grasp_construction(solution: GraspSolution, rectangles: list[Rectangle]):
    best_solution: Solution = solution

    while len(rectangles) > 0 and len(best_solution.bins) < best_solution.max_bins:
        # Criar LCR (Lista de Candidatos Restrita)
        areas = [rectangle.area for rectangle in rectangles]
        Cmax = max(areas)
        Cmin = min(areas)
        threshold = Cmax - solution.alpha * (Cmax - Cmin)
        
        lcr = [rectangle for rectangle in rectangles if rectangle.area >= threshold]
        
        # Aplicar First Fit na LCR
        chosen_rectangle = random.choice(lcr)
        rectangles.remove(chosen_rectangle)
        current_solution = first_fit(solution, chosen_rectangle)
        
        if len(best_solution.bins) == 0:
            best_solution = current_solution
        else:
            if len(current_solution.bins) < len(best_solution.bins):
                best_solution = current_solution
            else:
                if current_solution.calculate_squared_occupancy_mean() < best_solution.calculate_squared_occupancy_mean():
                    best_solution = current_solution
    
    return best_solution

def main():
    input_file = "./app/empacotamentos/empacotamento_simples.txt"
    alpha = 0.3

    bin_width, bin_height, rectangles = read_input_file(input_file)
    solution = GraspSolution(Bin(bin_width, bin_height), max_bins = 10, alpha = alpha)

    solution = grasp_construction(solution, rectangles)
    print(f"Best solution found with {len(solution.bins)} bins.")
    for i, bin in enumerate(solution.bins):
        print(f"Bin {i+1}:")
        for rectangle in bin.rectangles:
            print(f"  Rectangle: {rectangle.width}x{rectangle.height} at ({rectangle.x}, {rectangle.y})")
        print(f"  Occupancy: {bin.calculate_occupancy()}%")

if __name__ == "__main__":
    main()