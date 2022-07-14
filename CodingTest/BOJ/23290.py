# BOJ 23290 - 마법사 상어와 복제
from collections import deque

M, S = map(int, input().split(' '))
fish_info = []
for i in range(M):
    fx, fy, d = map(int, input().split(' '))
    fish_info.append([fx-1, fy-1, d])

global shark_info, sx, sy
sx, sy = map(int, input().split(' '))
sx -= 1
sy -=1
shark_info = [sx, sy]

graph = []
for i in range(4):
    sub_graph = []
    for j in range(4):
        sub_graph.append(deque())
    graph.append(sub_graph)

for fish in fish_info:
    fx = fish[0]
    fy = fish[1]
    d = fish[2]
    graph[fx][fy].append(d)

graph[shark_info[0]][shark_info[1]].append(9)     # 상어가 있는 칸은 9

# d에 따라 이동 방향의 dx, dy 값 판단
def find_direction(d):
    if d == 1:
        return 0, -1
    if d == 2:
        return -1, -1
    if d == 3:
        return -1, 0
    if d == 4:
        return -1, 1
    if d == 5:
        return 0, 1
    if d == 6:
        return 1, 1
    if d == 7:
        return 1, 0
    if d == 8:
        return 1, -1

# 모든 물고기 한 칸 이동
def fish_move(graph):
    origin_graph = []
    for ii in range(4):
        sub_graph = []
        for jj in range(4):
            sub_graph.append(deque())
        origin_graph.append(sub_graph)
    for ii in range(4):
        for jj in range(4):
            origin_graph[ii][jj] = graph[ii][jj].copy()

    for i in range(4):
        for j in range(4):
            for k in range(len(origin_graph[i][j])):
                origin_d = origin_graph[i][j][k]
                d = origin_d
                if d == 9 or d < 0:
                    continue
                # 이동 가능한 방향 찾기
                for ii in range(8):
                    dx, dy = find_direction(d)
                    next_x = i + dx
                    next_y = j + dy
                    # 이동하려는 칸이 격자 범위 벗어나는지
                    if next_x < 0 or next_x > 3 or next_y < 0 or next_y > 3:
                        # 이동 방향 45도 반시계 회전
                        d -= 1
                        if d == 0:
                            d = 8
                        continue

                    # 이동하려는 칸에 상어가 있는지, 물고기의 냄새가 있는지 판단
                    will_move = origin_graph[next_x][next_y]
                    check = 0
                    for jj in range(len(will_move)):
                        if will_move[jj] == 9 or will_move[jj] < 0:
                            check = 1

                    # 해당 방향으로 이동 못하면, 이동 방향 45도 반시계 회전
                    if check == 1:
                        d -= 1
                        if d == 0:
                            d = 8
                        continue
                    # 해당 방향으로 이동 가능한 경우
                    else:
                        graph[i][j].remove(origin_d)
                        graph[next_x][next_y].append(d)
                        break

d_sx = [-1, 0, 1, 0]
d_sy = [0, -1, 0, 1]

global max_fish_count
max_fish_count = -1
global path
path = []

# 상어 이동 로직 구현(DFS)
def dfs(x, y, move_count, fish_count, visit):
    global max_fish_count, shark_info, path
    # print("x:", x, ", y:", y, ", cnt:", fish_count, ", path:", visit)
    if move_count == 3:     # 3번 이동한 경우 Stop
        if max_fish_count < fish_count:
            max_fish_count = fish_count
            shark_info = (x, y)
            path = visit[:]
        return

    for k in range(4):
        next_x = x + d_sx[k]
        next_y = y + d_sy[k]
        if next_x >= 0 and next_x < 4 and next_y >= 0 and next_y < 4:
            if (next_x, next_y) not in visit:   # 처음 방문한 경우
                visit.append((next_x, next_y))
                add_cnt = len(graph[next_x][next_y])
                for k in range(len(graph[next_x][next_y])):
                    if graph[next_x][next_y][k] == 9:
                        add_cnt = 0
                dfs(next_x, next_y, move_count+1, fish_count+add_cnt, visit)
                visit.pop()
            else:   # 이미 방문한 경우
                dfs(next_x, next_y, move_count+1, fish_count, visit)

# 상어 연속 3칸 이동 & 물고기 냄새 마킹(-3 값으로)
def shark_move():
    global sx, sy
    graph[sx][sy].remove(9)
    dfs(sx, sy, 0, 0, [])
    for x, y in path:
        if graph[x][y]:
            graph[x][y] = deque()
            graph[x][y].append(-3)
    sx = path[-1][0]
    sy = path[-1][1]
    graph[sx][sy].append(9)

# 물고기 냄새 감소
def reduce_smell(graph):
    for i in range(4):
        for j in range(4):
            for k in range(len(graph[i][j])):
                if graph[i][j][k] < 0:
                    graph[i][j][k] += 1
                if graph[i][j][k] == 0:
                    graph[i][j].remove(0)

# 복제 마법 & fish_info 업데이트
def copy_magic(origin_graph, graph):
    for i in range(4):
        for j in range(4):
            graph[i][j] += origin_graph[i][j]
    return graph

def count_fish(graph):
    result = 0
    for i in range(4):
        for j in range(4):
            for k in range(len(graph[i][j])):
                if graph[i][j][k] == 9 or graph[i][j][k] < 0:
                    continue
                result += 1
    return result

answer = 0
# 연습 횟수 만큼 마법 연습
for i in range(S):
    origin_graph = []
    for ii in range(4):
        sub_graph = []
        for jj in range(4):
            sub_graph.append(deque())
        origin_graph.append(sub_graph)
    for ii in range(4):
        for jj in range(4):
            for kk in range(len(graph[ii][jj])):
                if graph[ii][jj][kk] == 9 or graph[ii][jj][kk] < 0:
                    continue
                origin_graph[ii][jj].append(graph[ii][jj][kk])

    print('======처음=======')
    for j in range(4):
        print(graph[j])
    # 모든 물고기 한 칸 이동
    fish_move(graph)
    print('======물고기 이동 후=======')
    for j in range(4):
        print(graph[j])
    # 상어 연속 3칸 이동 & 물고기 냄새 마킹(-3 값으로)
    shark_move()
    print('======상어 이동 후 & 냄새 마킹=======')
    for j in range(4):
        print(graph[j])

    # 물고기 냄새 감소
    reduce_smell(graph)
    print('======냄새 감소=======')
    for j in range(4):
        print(graph[j])

    # 복제 마법 & fish_info 업데이트
    print('======복제 마법 전 origin_graph=======')
    for j in range(4):
        print(origin_graph[j])
    print('======복제 마법 전 graph=======')
    for j in range(4):
        print(graph[j])
    graph = copy_magic(origin_graph, graph)
    print('======복제 마법 후=======')
    for j in range(4):
        print(graph[j])

    # 물고기 수 count
    answer = count_fish(graph)

print(answer)