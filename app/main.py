from models.grasp_builder import GraspBuilder
from models.grasp_solution import GraspSolution
from models.objective_function import objective_function
from models.bin import Bin
from helpers import read_input_file

def main():
    numbers = [1]
    for number in numbers:
        input_file = f"./app/inputs/packing_{number}.txt"
        alpha = 0.5
        bin_width, bin_height, rectangles = read_input_file(input_file)
        
        solution = GraspSolution(Bin(bin_width, bin_height), alpha, number)
        solution = GraspBuilder.build(solution, rectangles)

        print("Initial solution:")
        print(solution)
        print("Objective function value:", objective_function(solution))

        solution, rectangules = GraspBuilder.local_search(solution, rectangles)
        print("After local search:")
        print(solution)
        print("Objective function value:", objective_function(solution))
        print("Rectangles: ")
        print(rectangules)

if __name__ == "__main__":
    main()