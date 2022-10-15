'''
N x N 격자
초기 격자의 모든 칸에는 블록이 하나씩 들어 있음
    검은색 블록(-1)
    무지개 블록(0)
    일반 블록(1 <= X <= M)
인접한 칸: |r1-r2| + |c1-c2| = 1을 만족하는 두 칸
블록 그룹: 연결된 블록의 집합
    - 일반 블록이 적어도 하나 있어야 함
    - 일반 블록의 색은 모두 같아야 함
    - 검은색 블록은 포함되면 안 되고, 무지개 블록은 얼마나 있든 상관 X
    - 그룹에 속한 블록의 개수는 2 이상
    - 임의의 한 블록에서 그룹에 속한 인접 칸으로 이동해서 그룹에 속한 다른 모든 칸으로 이동할 수 있어야 함
    - 블록 그룹의 기준 블록
      : 무지개 블록이 아닌 블록 중에서 행의 번호가 가장 작은 블록, 여러 개면 열의 번호가 가장 작은 블록
오토 플레이 (아래 과정이 블록 그룹이 존재하는 동안 계속 반복)
    1. 크기가 가장 큰 블록 그룹을 찾는다.
       그러한 블록 그룹이 여러 개라면,
       포함된 무지개 블록의 수가 가장 많은 -> 기준 블록의 행이 가장 큰 -> 열이 가장 큰
    2. 1에서 찾은 블록 그룹의 모든 블록 제거
       블록 그룹에 포함된 블록의 수를 B라고 했을 때, B^2점 획득
    3. 격자에 중력이 작용
       * 중력 작용: 검은색 블록을 제외한 모든 블록이 행의 번호가 큰 칸으로 이동
                  이동은 다른 블록이나 격자의 경계를 만나기 전까지 계속 됨
    4. 격자가 90도 반시계 방향으로 회전
    5. 다시 격자에 중력 작용

필요한 변수
    - 입력: N, M, arr
    - 출력: score
    - visited[][]: 방문 여부
    - dr, dc: 방향
    -
'''

N, M = map(int, input().split(' '))
arr = [list(map(int, input().split(' '))) for _ in range(N)]

# 방향: 상-좌-하-우
dc = (-1, 0, 1, 0)
dr = (0, -1, 0, 1)

score = 0

def out_of_range(r, c):
    if r >= N or r < 0 or c >= N or c < 0:
        return True
    return False

def dfs(sr, sc, r, c):
    visited[r][c] = True

    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]

        if not out_of_range(nr, nc) and not visited[nr][nc] and arr[nr][nc] > -1:
            if arr[nr][nc] == arr[sr][sc] or arr[nr][nc] == 0:  # 같은 색 블록만
                group.append([nr, nc])
                dfs(sr, sc, nr, nc)

    if len(group) >= 2 and group not in block_group_list:
        block_group_list.append(group)

def gravity_op():
    global arr
    for j in range(N):
        for i in range(N, 0, -1):
            i -= 1
            if arr[i][j] >= 0:
                ci = i
                ni = i
                while True:
                    ni += 1
                    if ni < N and arr[ni][j] == -2:
                        arr[ni][j] = arr[ci][j]
                        arr[ci][j] = -2
                        ci = ni
                    else:
                        break

def rotate_counterclockwise_90():
    new_arr = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            new_arr[i][j] = arr[j][N - 1 - i]
    return new_arr

while True:
    visited = [[False] * N for _ in range(N)]
    group = []
    block_group_list = []

    # 블록 그룹 정보 저장
    for r in range(N):
        for c in range(N):
            if arr[r][c] > 0 and not visited[r][c]:
                group = [[r, c]]
                dfs(r, c, r, c)
                for i in range(N):
                    for j in range(N):
                        if arr[i][j] == 0:
                            visited[i][j] = False

    if len(block_group_list) == 0:
        break
    # 오토플레이
    # 1. 크기가 가장 큰 블록 그룹 찾기
    max_num = 0
    for block_group in block_group_list:
        if len(block_group) > max_num:
            max_num = len(block_group)

    max_group_list = []
    for block_group in block_group_list:
        if max_num == len(block_group):
            max_group_list.append(block_group)

    # 크기가 같은 블록 그룹이 여러 개일 시
    if len(max_group_list) > 1:
        # 무지개 블록이 가장 많은 블록 그룹
        max_rainbow_block = 0
        for group in max_group_list:
            count = 0
            for r, c in group:
                if arr[r][c] == 0:
                    count += 1
            if count > max_rainbow_block:
                max_rainbow_block = count
        max_rainbow_block_list = []
        for group in max_group_list:
            count = 0
            for r, c in group:
                if arr[r][c] == 0:
                    count += 1
            if max_rainbow_block == count:
                max_rainbow_block_list.append(group)
        if len(max_rainbow_block_list) > 1:
            # 기준 블록의 행, 열 값이 제일 큰
            max_group = max_rainbow_block_list[-1]
        elif len(max_rainbow_block_list) == 1:
            max_group = max_rainbow_block_list[0]
    elif len(max_group_list) == 1:
        max_group = max_group_list[0]

    # 2. 가장 큰 블록 그룹 제거
    for r, c in max_group:
        arr[r][c] = -2
    # 제거한 블록 개수의 제곱 수만큼 점수 합산
    score += (len(max_group) * len(max_group))

    # 3. 중력 작용
    gravity_op()

    # 4. 반시계 방향으로 회전
    arr = rotate_counterclockwise_90()

    # 5. 중력 작용
    gravity_op()

print(score)