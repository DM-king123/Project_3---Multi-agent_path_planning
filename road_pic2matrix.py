from PIL import Image
import os
# 设置每个格子的大小
cell_size = 5

# 读取图片
image = Image.open(('C:/Users/DELL/Desktop/data0.png'))

# 将图像转换为 RGB 模式
image = image.convert("RGB")

# 缩放图片使其适合要求的格子大小
width, height = image.size
scaled_width, scaled_height = (width // cell_size, height // cell_size)
image = image.resize((scaled_width, scaled_height))

# 将每个格子的值设为1或0
grid = []
for y in range(scaled_height):
    row = []
    for x in range(scaled_width):
        # 获取像素的RGB值
        r, g, b = image.getpixel((x, y))
        # 判断像素是否为道路（白色）
        if r > 200 and g > 200 and b > 200:
            row.append(0)
        else:
            row.append(1)
    grid.append(row)

# 将矩阵输出到桌面上的txt文件
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_path = os.path.join(desktop_path, "output.txt")
with open(output_path, "w") as f:
    for row in grid:
        f.write("".join(str(cell) for cell in row) + "\n")