from models.grasp_builder import GraspBuilder
from models.grasp_solution import GraspSolution
from models.objective_function import objective_function
from models.bin import Bin
from helpers import read_input_file
import time

def main():
    numbers = [3] # define qual arquivo de entrada será processado (Arquivos da pasta inputs)
    for number in numbers:
        input_file = f"./app/inputs/packing_{number}.txt"
        alpha = 0
        bin_width, bin_height, rectangles = read_input_file(input_file)
        solution = GraspSolution(Bin(bin_width, bin_height), alpha, number)
        maxTabuSize = round(len(rectangles) * 0.3)
        best_solution, best_value_ = GraspBuilder.tabuSearch(solution, rectangles, maxTabuSize)
        print("Best solution found:")
        print(best_solution)
        print("Best objective function value", best_value_)
            
        

if __name__ == "__main__":
    main()