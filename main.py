import random

class Rectangle:
    def __init__(self, width, height, id=None):
        self.width = width # Comprimento do retângulo
        self.height = height # Altura do retângulo
        self.id = id
        self.x = 0 # Posição x do retângulo
        self.y = 0 # Posição y do retângulo
        self.rotated = False
        self.area = width*height
    
    def rotate(self): # Rotaciona o retângulo (troca altura por comprimento)
        self.width, self.height = self.height, self.width
        self.rotated = not self.rotated
    
    def __repr__(self):
        return f"Rectangle(id={self.id}, w={self.width}, h={self.height}, x={self.x}, y={self.y}, rotated={self.rotated})"
    
    def copy(self):
        new_rect = Rectangle(self.width, self.height, self.id)
        new_rect.x = self.x
        new_rect.y = self.y
        new_rect.rotated = self.rotated
        return new_rect

class Bin:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rectangles = []
        self.used_area = 0
        self.area = width*height
        self.occupancy_map = [[False for _ in range(width)] for _ in range(height)] # Map com as posições do recipiente e qual o estado (ocupado ou não) atual
    
    def can_place(self, rect, x, y):
        if x + rect.width > self.width or y + rect.height > self.height:
            return False
        for i in range(x, x + rect.width):
            for j in range(y, y + rect.height):
                if self.occupancy_map[i][j]:
                    return False
        return True

    
    def place_rectangle(self, rect, x, y):
        # Coloca o retângulo na posição (x,y)
        if not self.can_place(rect, x, y):
            return False
        rect.x = x
        rect.y = y
        self.rectangles.append(rect)
        self.used_area += rect.area
        for i in range(x, x + rect.width):
            for j in range(y, y + rect.height):
                self.occupancy_map[i][j] = True
        return True
    
    def find_first_fit_position(self, rect):
        # Testa o retângulo sem alterar o original
        for rotated in [False, True]:
            test_rect = Rectangle(rect.width, rect.height)
            if rotated:
                test_rect.rotate()
            for y in range(self.height - test_rect.height + 1):
                for x in range(self.width - test_rect.width + 1):
                    if self.can_place(test_rect, x, y):
                        return (x, y), rotated
        return None, False

    
    def occupancy(self):
        return self.used_area / (self.width * self.height)
    
    def __repr__(self):
        return f"Bin(w={self.width}, h={self.height}, occupancy={self.occupancy():.2f}, rects={len(self.rectangles)})"

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

        nome_arquivo = f"arquivo_numero{number}.txt"
        with open(nome_arquivo, 'w') as f:
            for i, bin in enumerate(solution, 1):
                f.write(f"Bin {i} (Ocupação: {bin.occupancy():.2%}):\n")
                for rect in bin.rectangles:
                    f.write(f"  Retângulo {rect.id}: ({rect.width}x{rect.height}) {'(rotated)' if rect.rotated else ''}\n")

if __name__ == "__main__":
    main()