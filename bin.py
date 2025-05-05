from rectangule import Rectangle

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