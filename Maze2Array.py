import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

image_path = "CutMaze.png"
image = Image.open(image_path)

input_transform = transforms.Compose([
    transforms.Grayscale(1),
    transforms.ToTensor(),
])
image_tensor = input_transform(image).reshape(392, 520)

Maze = np.zeros([49, 65])
for i in range(49):
    for j in range(65):
        local_image = image_tensor[8 * i:8 * i + 8, 8 * j:8 * j + 8]
        gray_val = float(torch.sum(local_image) / 64)
        if gray_val > 0.1:
            Maze[i, j] = 1
        else:
            Maze[i, j] = 0
Maze[44, 63] = 0  #把图里的黄色小人设为通路
np.savetxt('Maze.txt', Maze, fmt="%d")

