# 프로그래머스 카카오 60059 - 자물쇠와 열쇠
def check_open(key, lock):
    chk = True
    for i in range(N-M+1):
        for j in range(N-M+1):
            temp_lock = lock[i:i+M]
            for k in range(N-M+1):
                print(temp_lock[k])
            print(temp_lock)
    return chk

def rotate_90_clockwise(key):
    return

def rotate_90_counterclockwise(key):
    return

def move_right(key):
    return

def move_left(key):
    return

def move_up(key):
    return

def move_down(key):
    return

def check_key(key):
    chk = False
    for i in range(M):
        for j in range(M):
            if key[i][j] == 1:
                chk = True
    return chk

def solution(key, lock):
    while True:
        # key의 돌기와 lock의 홈이 일치하는지 확인
        chk = check_open(key, lock)
        if chk == True:
            print('true')
            break

        if check_key(key):
            continue
        rotate_90_clockwise(key)             # 시계 방향으로 90도 회전
        rotate_90_counterclockwise(key)     # 반시계 방향으로 90도 회전

        move_right(key)     # 오른 쪽으로 한 칸 이동
        move_left(key)      # 왼 쪽으로 한 칸 이동
        move_up(key)        # 위 쪽으로 한 칸 이동
        move_down(key)      # 아래 쪽으로 한 칸 이동

    return True

M = 3
N = 5

key = [
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 1]
]

# lock = [
#     [1, 1, 1],
#     [1, 1, 0],
#     [1, 0, 1]
# ]

lock = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1]
]

check_open(key, lock)
# solution(key, lock)