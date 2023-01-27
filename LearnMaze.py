import random
import numpy as np
import pandas as pd

Maze = np.loadtxt('Maze.txt', dtype=int)
Startpoint = (48, 63)

lr = 0.1  # 学习率
reward_decay = 0.9
epsilon = 0.1  # 选择探索策略的概率
episode_num = 2000;
reward_endpoint = 100
reward_repeat = -1000
reward_notwall = -1

Q_table = pd.DataFrame(columns=['up', 'down', 'left', 'right'], dtype=np.float64)
Maze[Startpoint] = 1

for i in range(49):
    for j in range(65):
        if Maze[i, j] == 0:
            Q_table = Q_table.append(pd.Series([0] * 4, index=['up', 'down', 'left', 'right'], name='({x}, {y})' \
                                               .format(x=i, y=j)))
State_Num = Q_table.shape[0];

for State in Q_table.index:
    for Action in Q_table.columns:
        if Action == 'up':
            Next_State = tuple(sum(i) for i in zip(eval(State), (-1, 0)))
        elif Action == 'down':
            Next_State = tuple(sum(i) for i in zip(eval(State), (1, 0)))
        elif Action == 'left':
            Next_State = tuple(sum(i) for i in zip(eval(State), (0, -1)))
        elif Action == 'right':
            Next_State = tuple(sum(i) for i in zip(eval(State), (0, 1)))
        if (Maze[Next_State] == 1) and (Next_State != Startpoint):  # 撞墙
            Q_table.loc[str(State), Action] = -float('inf')  # 排除掉撞墙选项

for t in range(episode_num):
    if np.mod(t, 10) == 0:
        lr = max(lr * 0.9, 0.001)
        epsilon = epsilon * 0.5

    order = list(range(State_Num))
    random.shuffle(order)
    for i in order:
        State = Q_table.index[i]
        Path_List = [State]
        while 1:
            State_List = Q_table.loc[State]
            if np.random.random() > epsilon:
                Action = np.random.choice(State_List[State_List == np.max(State_List)].index)  # 随机选择最优的决策
            else:
                Action = np.random.choice(State_List[State_List != -float('inf')].index)
            if Action == 'up':
                Next_State = tuple(sum(i) for i in zip(eval(State), (-1, 0)))
            elif Action == 'down':
                Next_State = tuple(sum(i) for i in zip(eval(State), (1, 0)))
            elif Action == 'left':
                Next_State = tuple(sum(i) for i in zip(eval(State), (0, -1)))
            elif Action == 'right':
                Next_State = tuple(sum(i) for i in zip(eval(State), (0, 1)))

            Next_State_reward = 0

            if Next_State == Startpoint:  # 抵达起点
                reward = reward_endpoint
            elif str(Next_State) in Path_List:  # 惩罚回头路
                reward = reward_repeat
            else:  # 可走路径
                reward = reward_notwall
                Next_State_List = Q_table.loc[str(Next_State)]
                Next_State_reward = np.max(Next_State_List)

            Q_table.loc[State, Action] += lr * (reward + reward_decay * Next_State_reward)

            if (reward == reward_repeat) or (reward == reward_endpoint):  # 回头或到达终点则终止
                break
            State = str(Next_State)
            Path_List.append(State)
Q_table.to_csv('Q_table.csv')
