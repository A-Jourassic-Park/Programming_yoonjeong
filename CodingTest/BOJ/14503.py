N, M = map(int, input().split(' '))
r, c, d = map(int, input().split(' '))
arr = [list(map(int, input().split(' '))) for _ in range(N)]

'''
1. 현재 위치(r,c) 청소
2. 현재 위치에서 현재 방향(d)을 기준으로 왼쪽 방향부터 차례대로 탐색
    1) 왼쪽 방향에 아직 청소하지 않은 공간이 있으면,
       그 방향으로 회전한 다음 한 칸을 전진하고 1번부터 진행
    2) 왼쪽 방향에 청소할 공간이 없다면, 그 방향으로 회전하고 2번으로 돌아감
    3) 네 방향 모두 청소가 이미 되어있거나 벽인 경우에는,
       바라보는 방향을 유지한 채로 한 칸 후진을 하고 2번으로 돌아감
    4) 네 방향 모두 청소가 이미 되어있거나 벽이면서 뒤 쪽 방향이 벽이라 후진도 할 수 없는 경우에는,
       작동을 멈춤
이미 청소된 칸을 또 청소하지 않으며, 벽 통과 불가
d - 0: 북쪽, 1: 동쪽, 2: 남쪽, 3: 서쪽
'''

direction = [(-1, 0), (0, -1), (1, 0), (0, 1)] # 북-서-남-동
visited = [[False] * M for _ in range(N)]

if d == 0:
    d_idx = 0
if d == 1:
    d_idx = 3
if d == 2:
    d_idx = 2
if d == 3:
    d_idx = 1

search_count = 0
clean_count = 0

def out_of_range(r, c):
    if r >= N or r < 0 or c >= M or c < 0:
        return True
    return False

visited[r][c] = True
clean_count += 1

while True:
    # 왼쪽 방향의 칸 확인
    dr, dc = direction[(d_idx+1)%4]
    nr = r + dr
    nc = c + dc

    if not visited[nr][nc] and not out_of_range(nr,nc) and arr[nr][nc] != 1:
        # 청소 가능한 경우
        d_idx += 1      # 회전
        # 전진
        r = nr
        c = nc
        visited[r][c] = True     # 청소
        clean_count += 1
        search_count = 0

    elif visited[nr][nc] or out_of_range(nr,nc) or arr[nr][nc] == 1:
        # 청소할 공간이 없으면
        d_idx += 1      # 회전
        search_count += 1

    if search_count == 4:
        # 후진 방향 파악
        if d_idx % 4 == 0:
            dr, dc = direction[2]
        if d_idx % 4 == 1:
            dr, dc = direction[3]
        if d_idx % 4 == 2:
            dr, dc = direction[0]
        if d_idx % 4 == 3:
            dr, dc = direction[1]
        nr = r + dr
        nc = c + dc
        # 후진 가능 여부 파악
        if out_of_range(nr,nc) or arr[nr][nc] == 1:
            # 후진 불가능
            break
        else:
            # 후진
            r = nr
            c = nc
            search_count = 0

print(clean_count)