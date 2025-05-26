from models.grasp_builder import GraspBuilder
from models.grasp_solution import GraspSolution
from models.objective_function import objective_function
from models.bin import Bin
from helpers import read_input_file
import time

def main():
    numbers = [1]
    for number in numbers:
        input_file = f"./app/inputs/packing_{number}.txt"
        alpha = 0.5
        bin_width, bin_height, rectangles = read_input_file(input_file)
        rectanglesCopy = rectangles.copy()
        
        solution = GraspSolution(Bin(bin_width, bin_height), alpha, number)
        tempoExecucao = time.time() + 60 * 5  # 5 minutos
        bestSolution = 0
        while time.time() < tempoExecucao:
            solution = GraspBuilder.build(solution, rectangles)
            print("Initial solution:")
            print(solution)
            print("Objective function value:", objective_function(solution))
            solution, rectangules = GraspBuilder.local_search(solution, rectanglesCopy)
            print("After local search:")
            print(solution)
            print("Objective function value:", objective_function(solution))
            print("Rectangles: ")
            print(rectangules)
            if objective_function(solution) > bestSolution:
                bestSolution = objective_function(solution)
                print("New best solution found:", bestSolution)
                print("Solution details:", solution)
        

if __name__ == "__main__":
    main()