import random

from models.rectangle import Rectangle
from models.bin import Bin
from helpers import read_input_file

from PIL import Image, ImageDraw

def random_color():
    return tuple(random.randint(0, 255) for _ in range(3))

def first_fit_decreasing_grasp(bin_width: int, bin_height: int, rectangles: list[Rectangle], max_bins=100):
    sorted_rects = sorted(rectangles, key=lambda r: r.area, reverse=True)
    remaining_rects = sorted_rects.copy()
    bins: list[Bin] = []
    
    while remaining_rects and len(bins)< max_bins:
        temp_remaining: list[Rectangle] = []
        
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
        
        
    return solution

def main():
    input_file = "app/empacotamentos/empacotamento_desafiador.txt"
    alpha = 0.5
    numbers = [1]
    size = 250
    bin_width, bin_height, rectangles = read_input_file(input_file)

    print(f"Executando GRASP com First Fit Decreasing e alpha={alpha}")
    for number in numbers:
        solution = grasp_construction(bin_width, bin_height, rectangles, alpha)

        print(f"\nSolução encontrada com {len(solution)} bins:")
        total_occupancy = sum(bin.occupancy() for bin in solution) / len(solution)
        print(f"Ocupação média: {total_occupancy:.2%}")

        for i, bin in enumerate(solution, 1):
            print(f"Bin {i}: {bin}")

        nome_arquivo = f"app/logs/arquivo_numero{number}.txt"
        with open(nome_arquivo, 'w') as f:
            img = Image.new("RGB", (size, size), "white")
            draw = ImageDraw.Draw(img)
            auxX = 10
            auxY = 10
            bin_size = 40
            for i, bin in enumerate(solution, 1):
                if auxX + bin_size > size:
                    auxX = 10
                    auxY += bin_size + 15
                draw.rectangle([auxX-1,auxY-1, auxX + bin_size,auxY + bin_size],fill="white",outline="black")
                f.write(f"Bin {i} (Ocupação: {bin.occupancy():.2%}):\n")
                for rect in bin.rectangles:
                    color = random_color()
                    start,end= auxX + rect.x, auxY + rect.y
                    draw.rectangle([start, end, start + rect.width - 1 , end + rect.height - 1],fill=color)
                    f.write(f"  Retângulo {rect.id}: ({rect.width}x{rect.height}) ({rect.x},{rect.y}) {'(rotated)' if rect.rotated else ''}\n")
                auxX += bin_size + 15
            img.save(f"app/logs/binZAO.png")
if __name__ == "__main__":
    main()