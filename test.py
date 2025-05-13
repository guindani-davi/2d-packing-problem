from PIL import Image, ImageDraw

# Tamanho da imagem e dos bins
img_size = 400
bin_size = 40
spacing = 15

# Cria a imagem branca
img = Image.new("RGB", (img_size, img_size), "white")
draw = ImageDraw.Draw(img)

# Calcula os limites máximos para que os bins não ultrapassem a borda
x = 15
y = 15

while y + bin_size <= img_size:
    x = 15
    while x + bin_size <= img_size:
        # Desenha a borda do bin
        draw.rectangle(
            [x, y, x + bin_size - 1, y + bin_size - 1],
            outline="black"
        )
        x += bin_size + spacing
    y += bin_size + spacing

# Salva e exibe
img.save("bins_distribuidos.png")
