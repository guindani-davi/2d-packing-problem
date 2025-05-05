import random

from rectangule import Rectangle
from bin import Bin

def read_input_file(filename): #função de leitura de um arquivo com os exemplos
    # Arquivos de exemplo seguem o seguinte padrão: Primeira linha: Dimensão dos recipientes. Demais linhas: Dimensões de cada retângulo
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    bin_width, bin_height = map(int, lines[0].strip().split())
    
    rectangles = []
    for i, line in enumerate(lines[1:]):
        width, height = map(int, line.strip().split())
        rectangles.append(Rectangle(width, height, i+1))
    
    return bin_width, bin_height, rectangles

def first_fit_decreasing_grasp(bin_width, bin_height, rectangles, max_bins=100):
    sorted_rects = sorted(rectangles, key=lambda r: r.area, reverse=True)
    remaining_rects = sorted_rects.copy()
    bins = []
    
    while remaining_rects and len(bins) < max_bins:
        temp_remaining = []
        
        for rect in remaining_rects:
            placed = False
            for current_bin in bins:
                position, rotated = current_bin.find_first_fit_position(rect)
                if position is not None:
                    x, y = position
                    if rotated:
                        rect.rotate()
                    current_bin.place_rectangle(rect, x, y)
                    placed = True
                    break  # Já foi colocado, não precisa testar nos outros bins
            
            if not placed:
                # Se não coube em nenhum bin existente, criar um novo bin
                new_bin = Bin(bin_width, bin_height)
                position, rotated = new_bin.find_first_fit_position(rect) #garantir que ele cabe no novo bin
                if position is not None:
                    x, y = position
                    if rotated:
                        rect.rotate()
                    new_bin.place_rectangle(rect, x, y)
                    bins.append(new_bin)
                else:
                    # Caso absurdo (não deveria acontecer): nem na bin nova coube
                    temp_remaining.append(rect)
        
        remaining_rects = temp_remaining

    return bins


def grasp_construction(bin_width, bin_height, rectangles, alpha, max_bins=100):
    # Fase de construção GRASP com FFD
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
        solution = first_fit_decreasing_grasp(bin_width, bin_height, randomized_rects, max_bins)
        
        if len(solution) < best_num_bins:
            best_num_bins = len(solution)
            best_solution = solution
    
    return best_solution

def main():
    input_file = "empacotamentos/empacotamento_desafiador.txt"
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