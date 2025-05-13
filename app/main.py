from models.grasp_builder import GraspBuilder
from models.grasp_solution import GraspSolution
from models.bin import Bin
from helpers import read_input_file


def main():
    input_file = "empacotamentos/empacotamento_simples.txt"
    alpha = 0.3
    bin_width, bin_height, rectangles = read_input_file(input_file)
    
    solution = GraspSolution(Bin(bin_width, bin_height), 10, alpha)
    solution = GraspBuilder.build(solution, rectangles)

    print("Best solution found:")
    for i, bin in enumerate(solution.bins):
        print(f"Bin {i + 1}:")
        for rectangle in bin.rectangles:
            print(f"  {rectangle}")
        print(f"  Area: {bin.area}")
        print(f"  Occupancy: {bin.calculate_occupancy()}%")

if __name__ == "__main__":
    main()