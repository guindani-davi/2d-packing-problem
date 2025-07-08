import random, copy
from abc import ABC

from models.grasp_solution import GraspSolution
from models.solution import Solution
from models.bin import Bin
from models.rectangle import Rectangle
from models.objective_function import objective_function
import time
import shutil

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
    def build(solution: GraspSolution, rec: list[Rectangle]) -> GraspSolution:
        while len(rec) > 0:
            # Criar LCR (Lista de Candidatos Restrita)
            areas = [rectangle.area for rectangle in rec]
            Cmax = max(areas)
            Cmin = min(areas)
            threshold = Cmax - solution.alpha * (Cmax - Cmin)
            
            lcr = [rectangle for rectangle in rec if rectangle.area >= threshold]
            
            chosen_rectangle = random.choice(lcr)
            rec.remove(chosen_rectangle)
            solution = GraspBuilder.first_fit(solution, chosen_rectangle)
        
        return solution
    
    @staticmethod
    def local_search(solution: GraspSolution, rectangles: list[Rectangle]) -> tuple[GraspSolution, float, list[Rectangle]]:
        best_solution = copy.deepcopy(solution)
        best_value = objective_function(best_solution)
        best_solution_rectangles = copy.deepcopy(rectangles)
        local_peek = False
        while(not local_peek):
            reset = False
            for i in range(0, len(best_solution_rectangles)):
                for j in range(i+1, len(best_solution_rectangles)):
                    current_rectangles = copy.deepcopy(best_solution_rectangles)
                    current_rectangles[j], current_rectangles[i] = current_rectangles[i], current_rectangles[j]
                    current_solution = GraspSolution(best_solution.default_bin, best_solution.alpha, best_solution.number)
                    current_solution = GraspBuilder.build(current_solution, list(current_rectangles))
                    current_value = objective_function(current_solution)
                    if current_value < best_value:
                        print("Local search found a better solution")
                        best_value = current_value
                        best_solution = copy.deepcopy(current_solution)
                        best_solution_rectangles = copy.deepcopy(current_rectangles)
                        print("Best solution:", best_solution)
                        print("Objective function value:", best_value)
                        reset = True
                    if reset:
                        break
                if reset:
                    break
            if not reset:
                local_peek = True

        return best_solution,best_solution_rectangles
    
    @staticmethod
    def addTabu(pair: tuple[int, int],tabu_list: list,maxTabuSize: int) -> None:
        if pair in tabu_list:
            tabu_list.remove(pair)
        tabu_list.append(pair)
        if len(tabu_list) >= maxTabuSize:
            tabu_list.pop(0)
    
    @staticmethod
    def tabuSearch(solution: GraspSolution, rectangles: list[Rectangle],maxTabuSize: int) -> list[GraspSolution]:
        with open("app/logs/tabu_search.log", "a") as log_file:
            tabu_list = []
            current_solution = GraspBuilder.build(copy.deepcopy(solution), copy.deepcopy(rectangles))
            current_value_s = objective_function(current_solution)
            best_solution = copy.deepcopy(solution)
            best_value_ = current_value_s
            print("Starting tabu search with initial solution:", current_solution)
            print("Initial objective function value:", current_value_s)
            shutil.move("app/logs/bin_packing_3.png", "app/logs/bin_packing_3_inicial.png")
            log_file.write(f"Starting tabu search with initial solution: {current_solution}\n")
            log_file.write(f"Initial objective function value: {current_value_s}\n")
            log_file.write("---------------------------\n")
            best_neighbor_value = float('inf')
            best_neighbor_solution = None
            best_neighbor_move = (0, 0)
            tempoExecucao = time.time() + 60 * 120  # 120 minutos
            while True:
                reset = False
                for i in range(len(rectangles)-1):
                    for j in range(i + 1, len(rectangles)):
                        if time.time() > tempoExecucao:
                            print("Tempo de execução excedido. Encerrando busca tabu.")
                            return best_solution, best_value_
                        current_rectangles = copy.deepcopy(rectangles)
                        current_rectangles[j], current_rectangles[i] = current_rectangles[i], current_rectangles[j]
                        new_solution = GraspBuilder.build(copy.deepcopy(solution), list(current_rectangles))
                        new_value = objective_function(new_solution) #avalia nova solução
                        print(f"Evaluating swap ({i}, {j}): New value = {new_value}, Current best value = {best_value_}")
                        print(f"Current solution: {new_solution}")
                        if (i,j) in tabu_list: # se a troca já está na tabu
                            if new_value < best_value_: # verifica critério de aspiração (nova solução é melhor que a melhor solução encontrada até agora)
                                best_value_ = new_value # atualiza melhor valor
                                best_solution = copy.deepcopy(new_solution) # atualiza melhor solução
                                current_value_s = new_value # atualiza valor da solução atual
                                current_solution = copy.deepcopy(new_solution) # atualiza solução atual
                                GraspBuilder.addTabu((i,j), tabu_list,maxTabuSize) # passa a troca para o final da tabu list
                                reset = True # flag para reiniciar a busca
                                break
                        else: # se a troca não está na tabu
                            if new_value < current_value_s: #se a nova solução é melhor que a solução atual
                                current_value_s = new_value # atualiza valor da solução atual
                                current_solution = copy.deepcopy(new_solution) # atualiza solução atual
                                if new_value < best_value_: # se a nova solução é melhor que a melhor solução
                                    best_value_ = new_value # atualiza melhor valor
                                    best_solution = copy.deepcopy(new_solution) # atualiza melhor solução
                                    GraspBuilder.addTabu((i,j), tabu_list, maxTabuSize) # passa a troca para o final da tabu list
                                    print("Found a better solution:", best_solution)
                                    print("Objective function value:", best_value_)
                                    log_file.write(f"Found a better solution: {best_solution}\n")
                                    log_file.write(f"Objective function value: {best_value_}\n")
                                    log_file.write("---------------------------\n")
                                reset = True
                                break
                            else:
                                if new_value < best_neighbor_value:
                                    best_neighbor_value = new_value
                                    best_neighbor_solution = copy.deepcopy(new_solution)
                                    best_neighbor_move = (i, j)
                    if reset:
                        break
                if not reset:
                    current_solution = best_neighbor_solution
                    current_value_s = best_neighbor_value
                    GraspBuilder.addTabu(best_neighbor_move, tabu_list, maxTabuSize)
                    log_file.write(f"No better solution found. Best neighbor: {best_neighbor_solution} with value {best_neighbor_value}\n")
                    log_file.write("---------------------------\n")
