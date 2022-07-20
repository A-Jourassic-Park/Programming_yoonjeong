# BOJ 20057 - 마법사 상어와 토네이도
import sys
sys.setrecursionlimit(10 ** 6)  # 백준 런타임 에러 해결을 위한 재귀함수 호출 횟수 확대

N = int(input())

graph = []
for i in range(N):
    sub_graph = list(map(int, input().split(' ')))
    graph.append(sub_graph)

global visted
visited = [[False] * N for _ in range(N)]

start_i = N // 2
start_j = N // 2

direction = [[0, -1], [1, 0], [0, 1], [-1, 0]]   # 좌 - 하 - 우 - 상
global dir_idx
dir_idx = 0

def rotate_90(p_graph):
    return list(reversed(list(zip(*p_graph))))

global percent_graph
percent_graph = []
percent_graph0 = [
    [0, 0, 0.02, 0, 0],
    [0, 0.1, 0.07, 0.01, 0],
    [0.05, 0, 0, 0, 0],
    [0, 0.1, 0.07, 0.01, 0],
    [0, 0, 0.02, 0, 0]
]
percent_graph.append(percent_graph0)
percent_graph1 = rotate_90(percent_graph0)
percent_graph.append(percent_graph1)
percent_graph2 = rotate_90(percent_graph1)
percent_graph.append(percent_graph2)
percent_graph3 = rotate_90(percent_graph2)
percent_graph.append(percent_graph3)

global alpha_direction
alpha_direction = [[0, -2], [2, 0], [0, 2], [-2, 0]]

global result
result = 0

def func(i, j):
    global dir_idx, visited, result, percent_graph, alpha_direction
    visited[i][j] = True

    if i == 0 and j == 0:
        return

    # 다음 방향 정하기
    next_i = i + direction[dir_idx % 4][0]
    next_j = j + direction[dir_idx % 4][1]

    if visited[next_i][next_j]:
        dir_idx -= 1
        next_i = i + direction[dir_idx % 4][0]
        next_j = j + direction[dir_idx % 4][1]

    # 비율 만큼 모래 이동
    sand_of_y = graph[next_i][next_j]
    left_sand = sand_of_y

    for r in range(5):
        for c in range(5):
            sand_to_move = int(sand_of_y * percent_graph[dir_idx%4][r][c])
            left_sand -= sand_to_move
            if 0 <= next_i + r - 2 < N and 0 <= next_j + c - 2 < N:
                graph[next_i + r - 2][next_j + c - 2] += sand_to_move
            else:
                result += sand_to_move

    # alpha 위치에 남은 모래 이동
    alpha_i = i + alpha_direction[dir_idx%4][0]
    alpha_j = j + alpha_direction[dir_idx%4][1]

    if 0 <= alpha_i < N and 0 <= alpha_j < N:
        graph[alpha_i][alpha_j] += left_sand
    else:
        result += left_sand

    graph[next_i][next_j] = 0

    dir_idx += 1
    func(next_i, next_j)

func(start_i, start_j)
print(result)