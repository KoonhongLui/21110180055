import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

Maze = np.loadtxt('Maze.txt', dtype= np.float64)
Q_table = pd.read_csv('Q_table.csv',index_col = 0)


Path_List = []
print("输入终点的坐标x, y, 例如: 1, 1; 25, 33")
while True:
    try:
        State = eval(input())
        if str(State) in Q_table.index:
            break
        else:
            print("这个终点在墙上, 请重新输入")
    except:
        print("输入的不是合法坐标, 请重新输入")

Path_List.append(State)
Startpoint = (48, 63)

while 1:
    State_List = Q_table.loc[str(State)]
    Action = np.random.choice(State_List[State_List == np.max(State_List)].index) # 随机选择最优的决策
    if Action == 'up':
        State = tuple(sum(i) for i in zip(State, (-1, 0)))
    elif Action == 'down':
        State = tuple(sum(i) for i in zip(State, (1, 0)))
    elif Action == 'left':
        State = tuple(sum(i) for i in zip(State, (0, -1)))
    elif Action == 'right':
        State = tuple(sum(i) for i in zip(State, (0, 1)))
    if State == Startpoint:
        Path_List.append(State)
        break
    elif (str(State) not in Q_table.index) or (State in Path_List):  # 抵达起点
        print("无法抵达此终点")
        exit()
    else:
        Path_List.append(State)

img = np.zeros([49,65,3], dtype=np.uint8)
for i in range(49):
    for j in range(65):
        if Maze[i, j] == 0:
            img[i, j] = [255, 255, 255]
        elif Maze[i, j] == 1:
            img[i, j] = [0, 0, 0]

img[Path_List[0]] = [0,255,0]
fig = plt.figure()
pics = []

for i in Path_List[::-1]:
    img[i] = [255, 0, 0]
    pic = plt.imshow(img, animated=True)

    pics.append([pic])
ani = animation.ArtistAnimation(fig, pics, interval=40,
                                repeat_delay=0)
plt.show()
