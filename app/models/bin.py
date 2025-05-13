from models.rectangle import Rectangle

class Bin:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.rectangles: list[Rectangle] = []
        self.used_area = 0
        self.area = width * height
        self.occupancy_map = [[False for _ in range(width)] for _ in range(height)] # Mapa com as posições do recipiente e qual o estado (ocupado ou não) atual
    
    def can_place(self, rect: Rectangle, x: int, y: int) -> bool:
        if x + rect.width > self.width or y + rect.height > self.height:
            return False
        for i in range(x, x + rect.width):
            for j in range(y, y + rect.height):
                if self.occupancy_map[i][j]:
                    return False
        return True
    
    def place_rectangle(self, rectangle: Rectangle, x: int, y: int) -> bool:
        if not self.can_place(rectangle, x, y):
            return False
        rectangle.x = x
        rectangle.y = y
        self.rectangles.append(rectangle)
        self.used_area += rectangle.area
        for i in range(x, x + rectangle.width):
            for j in range(y, y + rectangle.height):
                self.occupancy_map[i][j] = True
        return True
    
    def find_first_fit_position(self, rect: Rectangle) -> tuple[tuple[int, int], bool]:
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
    
    def __repr__(self):
        return f"Bin(w={self.width}, h={self.height}, occupancy={self.occupancy():.2f}, rects={len(self.rectangles)})"