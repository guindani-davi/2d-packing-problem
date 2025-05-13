from models.grasp_builder import GraspBuilder
from models.grasp_solution import GraspSolution
from models.bin import Bin
from helpers import read_input_file

def main():
    numbers = [1, 2, 3, 4, 5]
    for number in numbers:
        input_file = f"./app/inputs/packing_{number}.txt"
        alpha = 0.5
        bin_width, bin_height, rectangles = read_input_file(input_file)
        
        solution = GraspSolution(Bin(bin_width, bin_height), 10, alpha,number)
        solution = GraspBuilder.build(solution, rectangles)

        print(solution)

if __name__ == "__main__":
    main()