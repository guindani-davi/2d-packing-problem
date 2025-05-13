from models.grasp_builder import GraspBuilder
from models.grasp_solution import GraspSolution
from models.bin import Bin
from helpers import read_input_file


def main():
    input_file = "./app/inputs/packing_3.txt"
    alpha = 0.5
    bin_width, bin_height, rectangles = read_input_file(input_file)
    
    solution = GraspSolution(Bin(bin_width, bin_height), 10, alpha)
    solution = GraspBuilder.build(solution, rectangles)

    print(solution)

if __name__ == "__main__":
    main()