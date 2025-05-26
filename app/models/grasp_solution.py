from models.solution import Solution
from models.bin import Bin
from PIL import Image, ImageDraw

class GraspSolution(Solution):
    def __init__(self, default_bin: Bin, alpha: int, number: int):
        super().__init__(default_bin)
        self.bin = default_bin
        self.number = number
        self.alpha = alpha

    def __str__(self):
        img_height = 600
        img_width = 800
        padding = 20
        img = Image.new("RGB",(img_width, img_height), "white")
        draw = ImageDraw.Draw(img)
        x = 10
        y = 10 
        output = []
        for i, bin_obj in enumerate(self.bins):
            if x + bin_obj.width > img_width - padding:
                x = 10 
                y += bin_obj.height + 10
            draw.rectangle([x - 1, y - 1, x + bin_obj.width, y + bin_obj.height], outline="black", fill="white")
            #output.append(f"Bin {i + 1}:")

            for rectangle in bin_obj.rectangles:
                #output.append(f"  {rectangle}")
               
                start_x = x + rectangle.x
                start_y = y + (bin_obj.height - (rectangle.y + rectangle.height))

                end_x = start_x + rectangle.width - 1
                end_y = start_y + rectangle.height - 1

                draw.rectangle([start_x, start_y, end_x, end_y], fill=rectangle.color, outline="black")

            x += bin_obj.width + 10

        img.save(f"app/logs/bin_packing_{self.number}.png")
        output.append(f"Sum of squared rectangles: {self.calculate_sum_of_squared_rectangules()}")
        return "\n".join(output)

