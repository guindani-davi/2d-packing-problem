from models.rectangle import Rectangle

def read_input_file(filename: str):
    # Arquivos de exemplo seguem o seguinte padrão: Primeira linha: Dimensão dos recipientes. Demais linhas: Dimensões de cada retângulo
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    bin_width, bin_height = map(int, lines[0].strip().split())
    
    rectangles: list[Rectangle] = []
    for i, line in enumerate(lines[1:]):
        parts = line.strip().split()
        width, height = map(int, parts[:2])
        color = parts[2]
        rgb = tuple(map(int, color.strip("()").split(",")))
        rectangule_id = i + 1
        rectangles.append(Rectangle(width, height, rgb, rectangule_id))
    
    return bin_width, bin_height, rectangles
