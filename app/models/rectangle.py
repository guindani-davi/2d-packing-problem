class Rectangle:
    def __init__(self, width: int, height: int, id=None):
        self.width = width
        self.height = height
        self.id = id
        self.x = 0
        self.y = 0
        self.rotated = False
        self.area = width*height
    
    def rotate(self):
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