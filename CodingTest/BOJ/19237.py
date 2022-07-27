# BOJ 19237 - 어른 상어

import copy

N, M, k = map(int, input().split(' '))
graph = [list(map(int, input().split())) for _ in range(N)]
shark_dir = list(map(int, input().split(' ')))
shark_dir_prior = []
for i in range(M):
    shark_dir_prior.append([list(map(int, input().split())) for _ in range(4)])

# 그래프 초기 세팅
'''
상어가 있는 칸은 [상어 번호, 냄새, 이동방향] 형태로 저장
상어는 없는데 냄새가 있는 칸은 [상어 번호, 냄새, -1] 형태로 저장
상어가 없는 칸은 0 저장
'''
for i in range(N):
    for j in range(N):
        if graph[i][j] != 0:
            s_num = graph[i][j]
            s_dir = shark_dir[s_num-1]
            s_lst = [s_num, k, s_dir]
            graph[i][j] = s_lst

dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # 위, 아래, 왼쪽, 오른쪽

def move_shark(graph):       # 상하좌우로 인접한 칸 중 하나로 이동 & 겹치는 상어 있으면 제거
    # 현재 이동방향 확인 후 우선순위 판단
    '''
    1. 인접한 칸 중 아무 냄새가 없는 칸의 방향
    2. 그런 칸이 없으면 자신의 냄새가 있는 칸의 방향
    가능한 칸이 여러 개일 경우, 특정 우선순위를 따름 (shark_dir_prior)
    '''
    next_graph = copy.deepcopy(graph)
    for i in range(N):
        for j in range(N):
            if graph[i][j] != 0:
                if graph[i][j][2] != -1:
                    s_num = graph[i][j][0]
                    s_dir = graph[i][j][2]
                    s_dir_prior = shark_dir_prior[s_num-1][s_dir-1]
                    chk = 0
                    for d in s_dir_prior:
                        next_i = i + dir[d-1][0]
                        next_j = j + dir[d-1][1]

                        # 범위 확인
                        if next_i < 0 or next_i >= N or next_j < 0 or next_j >= N:
                            continue
                        # 인접한 칸 중 아무 냄새 없는 칸
                        if graph[next_i][next_j] == 0:
                            next_graph[i][j][2] = -1
                            if isinstance(next_graph[next_i][next_j], list):
                                if isinstance(next_graph[next_i][next_j][0], list) and len(next_graph[next_i][next_j]) > 1:
                                    next_graph[next_i][next_j].append([s_num, 0, d])
                                else:
                                    lst = next_graph[next_i][next_j]
                                    next_graph[next_i][next_j] = []
                                    next_graph[next_i][next_j].append(lst)
                                    next_graph[next_i][next_j].append([s_num, 0, d])
                            elif next_graph[next_i][next_j] == 0:
                                next_graph[next_i][next_j] = [s_num, 0, d]
                            chk = 1
                            break

                    if chk == 0:
                        for d in s_dir_prior:
                            next_i = i + dir[d - 1][0]
                            next_j = j + dir[d - 1][1]

                            # 범위 확인
                            if next_i < 0 or next_i >= N or next_j < 0 or next_j >= N:
                                continue

                            # 자신의 냄새가 있는 칸 방향
                            if graph[next_i][next_j] != 0:
                                if graph[next_i][next_j][0] == s_num:
                                    next_graph[i][j][2] = -1
                                    next_graph[next_i][next_j][1] = 0
                                    next_graph[next_i][next_j][2] = d
                                    break
    # 중복되는 칸 상어 쫓아 내기
    for i in range(N):
        for j in range(N):
            if isinstance(next_graph[i][j], list):
                if isinstance(next_graph[i][j][0], list) and len(next_graph[i][j]) > 1:
                    # 중복되는 칸이 있는 경우
                    arr_len = len(next_graph[i][j])
                    # 상어 수가 작은 애가 이김
                    s_num = 500
                    for a in range(arr_len):
                        if s_num > next_graph[i][j][a][0]:
                            s_num = next_graph[i][j][a][0]
                            result_shark = next_graph[i][j][a]
                    next_graph[i][j] = result_shark

    return next_graph

def leave_smell(graph, k):      # 자신의 위치에 냄새 뿌리기
    for i in range(N):
        for j in range(N):
            if graph[i][j] != 0:
                if graph[i][j][2] != -1:
                    graph[i][j][1] = k

def reduce_smell(graph):     # 지나온 위치 냄새 -1 감소
    for i in range(N):
        for j in range(N):
            if graph[i][j] != 0:
                if graph[i][j][2] == -1:
                    graph[i][j][1] -= 1
                if graph[i][j][1] == 0:
                    graph[i][j] = 0

def shark_check(graph):          # 1번 상어만 격자에 남았는지 체크
    chk = True
    for i in range(N):
        for j in range(N):
            if graph[i][j] != 0:
                if graph[i][j][0] != 1 and graph[i][j][2] != -1:
                    chk = False
    return chk

sec = 0
while True:
    # 1번 상어만 격자에 남아있을 시
    if shark_check(graph):
        print(sec)
        break

    # 1000초가 지났을 시
    if sec == 1000:
        print(-1)
        break

    # 메인 로직
    # 상하좌우로 인접한 칸 중 하나로 이동
    graph = move_shark(graph)
    # 자신의 위치에 냄새 뿌리기
    leave_smell(graph, k)
    # 냄새 -1 감소
    reduce_smell(graph)

    sec += 1