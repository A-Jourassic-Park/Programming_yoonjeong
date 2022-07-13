# BOJ 23291 - 어항 정리
from collections import deque

N, K = map(int, input().split(' '))
graph = list()
graph.append(deque(list(map(int, input().split(' ')))))

# 가장 적은 물고기 수의 어항에 한 마리 추가
def push_fish_to_min_bowl(graph):
 min_fish_num = min(graph[0])
 for i in range(len(graph[0])):
  if graph[0][i] == min_fish_num:
   graph[0][i] += 1

# 가장 왼쪽에 있는 어항을 그 어항의 오른쪽에 있는 어항 위에 올려 두기
def popleft_and_stack(graph):
 pop = graph[0].popleft()
 graph.append(deque([pop]))

# 2개 이상 쌓여 있는 어항을 공중 부양 후, 시계방향으로 90도 회전
def fly_blocks_and_rotate_90_clock_wise(graph):
 while True:
  if len(graph) > len(graph[0]) - len(graph[-1]):
   break
  fly_blocks = []
  fly_blocks_row = len(graph)
  fly_blocks_col = len(graph[-1])

  for i in range(fly_blocks_row):
   new_deque = deque()
   for j in range(fly_blocks_col):
    new_deque.append(graph[i].popleft())
   fly_blocks.append(new_deque)
  graph = [graph[0]]

  # 시계방향으로 90도 회전
  rotated_blocks = [[0] * len(fly_blocks) for i in range(len(fly_blocks[0]))]
  for i in range(len(fly_blocks[0])):
   for j in range(len(fly_blocks)):
    rotated_blocks[i][j] = fly_blocks[j][len(fly_blocks[0])-1-i]

  for row in rotated_blocks:
   graph.append(deque(row))

 return graph

# 물고기 수 조절
def fix_fish_num(graph):
 calc_result = []    # 물고기를 얼마나 얻는지/잃는지
 for i in range(len(graph)):
  tmp_calc_result = []
  for j in range(len(graph[i])):
   tmp_calc_result.append(0)
  calc_result.append(tmp_calc_result)

 di = [0, 0, -1, 1]
 dj = [-1, 1, 0, 0]

 for i in range(len(graph)):
  for j in range(len(graph[i])):
   for k in range(4):
    next_i = i + di[k]
    next_j = j + dj[k]

    if next_i >= 0 and next_i < len(graph) and next_j >= 0 and next_j < len(graph[next_i]):
     # 인접 칸과 물고기 수 비교
     sub = graph[i][j] - graph[next_i][next_j]
     d = abs(sub) // 5
     if d > 0:
      if sub > 0:
       calc_result[i][j] -= d
      else:
       calc_result[i][j] += d

 for i in range(len(graph)):
  for j in range(len(graph[i])):
   graph[i][j] += calc_result[i][j]

# 일렬로 놓기
def put_bowl_in_a_row(graph):
 new_graph = deque()

 for i in range(len(graph[-1])):
  for j in range(len(graph)):
   new_graph.append(graph[j][i])

 for i in range(len(graph[-1]), len(graph[0])):
  new_graph.append(graph[0][i])

 aligned_graph = list()
 aligned_graph.append(new_graph)

 graph = aligned_graph

 return graph

# 가운데를 중심으로 왼쪽 N/2개를 공중 부양 후, 시계방향으로 180도 회전
def fly_blocks2_and_rotate_180_clockwise(graph):
 left1 = list()
 left2 = list()
 new_deque1 = deque()

 for i in range(N//2):
  new_deque1.append(graph[0].popleft())
 left1.append(new_deque1)

 # 시계방향으로 180도 회전
 rotated_left1 = []
 for i in reversed(range(len(left1))):
  left1[i].reverse()
  rotated_left1.append(left1[i])
 graph += rotated_left1

 for i in range(2):
  temp_deque = deque()
  for j in range(N//4):
   temp_deque.append(graph[i].popleft())
  left2.append(temp_deque)
 # 시계방향으로 180도 회전
 rotated_left2 = []
 for i in reversed(range(len(left2))):
  left2[i].reverse()
  rotated_left2.append(left2[i])
 graph += rotated_left2

 return graph

# 메인 로직
answer = 0
while True:
 if max(graph[0]) - min(graph[0]) <= K:
  print(answer)
  break
 push_fish_to_min_bowl(graph)
 popleft_and_stack(graph)
 graph = fly_blocks_and_rotate_90_clock_wise(graph)
 fix_fish_num(graph)
 graph = put_bowl_in_a_row(graph)
 graph = fly_blocks2_and_rotate_180_clockwise(graph)
 fix_fish_num(graph)
 graph = put_bowl_in_a_row(graph)
 answer += 1

'''
 References
 https://velog.io/@heyksw/Python-%EB%B0%B1%EC%A4%80-platinum-23291-%EC%96%B4%ED%95%AD-%EC%A0%95%EB%A6%AC
'''