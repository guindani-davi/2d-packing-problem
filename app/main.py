import random


from app.models.solution import Solution
from models.rectangle import Rectangle
from models.bin import Bin
from helpers import read_input_file

def first_fit_decreasing(solution: Solution, rectangles: list[Rectangle]) -> Solution:
    # Algoritmo que tenta alocar o máximo de retângulos em cada bin, 
    # Usando o mínimo de bins possível 
    # Ordenando os retângulos por área em ordem decrescente

    sorted_rects = sorted(rectangles, key = lambda r: r.area, reverse=True) # Ordena os retângulos por área em ordem decrescente
    remaining_rects = sorted_rects.copy()
    
    while remaining_rects and len(solution.bins) < solution.max_bins:
        temp_remaining: list[Rectangle] = []
        
        for rect in remaining_rects:
            placed = False
            for current_bin in solution.bins:
                position, rotated = current_bin.find_first_fit_position(rect)
                if position is not None:
                    x, y = position
                    if rotated:
                        rect.rotate()
                    current_bin.place_rectangle(rect, x, y)
                    placed = True
                    break
            
            if not placed:
                new_bin = Bin(solution.default_bin.width, solution.default_bin.height)
                position, rotated = new_bin.find_first_fit_position(rect)
                if position is not None:
                    x, y = position
                    if rotated:
                        rect.rotate()
                    new_bin.place_rectangle(rect, x, y)
                    solution.bins.append(new_bin)
        
        remaining_rects = temp_remaining

    return solution

def grasp_construction(bin_width, bin_height, rectangles, alpha, max_bins=100):
    best_solution = None
    best_num_bins = float('inf')
    
    for _ in range(10):  # Número de iterações GRASP
        # Aleatorizar a lista de retângulos com componente GRASP
        sorted_rects = sorted(rectangles, key=lambda r: r.area, reverse=True)
        
        # Criar LCR (Lista de Candidatos Restrita)
        if len(sorted_rects) > 1:
            areas = [r.area for r in sorted_rects]
            Cmax = max(areas)
            Cmin = min(areas)
            threshold = Cmax - alpha * (Cmax - Cmin)
            
            # Dividir em LCR e outros
            LCR = [r for r in sorted_rects if r.area >= threshold]
            other = [r for r in sorted_rects if r.area < threshold]
            
            # Embaralhar LCR e manter a ordem decrescente dentro de cada grupo
            random.shuffle(LCR)
            LCR_sorted = sorted(LCR, key=lambda r: r.area, reverse=True)
            other_sorted = sorted(other, key=lambda r: r.area, reverse=True)
            
            # Juntar novamente mantendo alguns dos maiores primeiro, mas com aleatoriedade
            randomized_rects = LCR_sorted + other_sorted
        else:
            randomized_rects = sorted_rects
        
        # Aplicar First Fit Decreasing na lista (parcialmente) randomizada
        solution = first_fit_decreasing(bin_width, bin_height, randomized_rects, max_bins)
        
        if len(solution) < best_num_bins:
            best_num_bins = len(solution)
            best_solution = solution
    
    return best_solution

def main():
    input_file = "empacotamentos/empacotamento_simples.txt"
    alpha = 0.5
    numbers = [1,2,3,4,5]

    bin_width, bin_height, rectangles = read_input_file(input_file)

    print(f"Executando GRASP com First Fit Decreasing e alpha={alpha}")
    for number in numbers:
        solution = grasp_construction(bin_width, bin_height, rectangles, alpha)

        print(f"\nSolução encontrada com {len(solution)} bins:")
        total_occupancy = sum(bin.occupancy() for bin in solution) / len(solution)
        print(f"Ocupação média: {total_occupancy:.2%}")

        for i, bin in enumerate(solution, 1):
            print(f"Bin {i}: {bin}")

        nome_arquivo = f"./logs/arquivo_numero{number}.txt"
        with open(nome_arquivo, 'w') as f:
            for i, bin in enumerate(solution, 1):
                f.write(f"Bin {i} (Ocupação: {bin.occupancy():.2%}):\n")
                for rect in bin.rectangles:
                    f.write(f"  Retângulo {rect.id}: ({rect.width}x{rect.height}) {'(rotated)' if rect.rotated else ''}\n")

if __name__ == "__main__":
    main()