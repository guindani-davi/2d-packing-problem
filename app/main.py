from models.grasp_builder import GraspBuilder
from models.grasp_solution import GraspSolution
from models.objective_function import objective_function
from models.bin import Bin
from helpers import read_input_file
import time

def main():
    numbers = [2]
    for number in numbers:
        input_file = f"./app/inputs/packing_{number}.txt"
        alpha = 0.5
        bin_width, bin_height, rectangles = read_input_file(input_file)
        rectanglesCopy = rectangles.copy()
        current_solution = GraspSolution(Bin(bin_width, bin_height), alpha, number)
        tempoExecucao = time.time() + 60 * 5  # 5 minutos
        bestSolution = GraspBuilder.build(current_solution, rectangles)
        bestValue = objective_function(bestSolution)
        tabuList = []
        maxTabuSize = round(len(rectanglesCopy) * 0.3)
        while time.time() < tempoExecucao:
            list = {}
            current_solution = GraspBuilder.build(current_solution, rectangles)
            print("Current solution:")
            print(current_solution)
            print("Objective function value:", objective_function(current_solution))
            neighborhood = GraspBuilder.neighborhood(current_solution, rectanglesCopy)
            for neighborhood_solution in neighborhood: #loop para avaliar todas as solucoes vizinhas e adicionar em uma lista
                list.setdefault(objective_function(neighborhood_solution), neighborhood_solution)
            list = sorted(list.items())
            for key, value in list:
                if key not in tabuList:
                    tabuList.append(key)
                    current_solution = value
                    if key < bestValue:
                        bestSolution = current_solution
                        bestValue = key
                        print("New best solution found:")
                        print(bestSolution)
                        print("Objective function value:", bestValue)
                        #função de aspiração confusa
                    if len(tabuList) >= maxTabuSize:
                        tabuList.pop(0)
                    break
        print("Final best solution:")
        print(bestSolution)
        print("Objective function value:", bestValue)
            
        

if __name__ == "__main__":
    main()