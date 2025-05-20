from models.solution import Solution
from models.bin import Bin
from PIL import Image, ImageDraw

class GraspSolution(Solution):
    def __init__(self, default_bin: Bin, alpha: int,number: int):
        super().__init__(default_bin)
        self.bin = default_bin
        self.number = number
        self.alpha = alpha

    def __str__(self):
        size = 1000
        img = Image.new("RGB",(size, size), "white")
        draw = ImageDraw.Draw(img)
        x = 10
        y = 10
        output = []
        for i, bin in enumerate(self.bins):
            if x + bin.width > size:
                x = 10
                y += bin.height + 10
            draw.rectangle([x-1, y-1, x + bin.width, y + bin.height], outline="black", fill="white")
            output.append(f"Bin {i + 1}:")
            for rectangle in bin.rectangles:
                output.append(f"  {rectangle}")
                start, end = x + rectangle.x, y + rectangle.y
                draw.rectangle([start, end, start + rectangle.width - 1, end + rectangle.height -1 ], fill=rectangle.color, outline="black")
            x += bin.width + 10
        img.save(f"app/logs/bin_packing_{self.number}.png")
        output.append(f"Sum of squared rectangles: {self.calculate_sum_of_squared_rectangules()}")
        return "\n".join(output)