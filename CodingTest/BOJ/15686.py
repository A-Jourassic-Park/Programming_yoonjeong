N, M = map(int, input().split(' '))
arr = [list(map(int, input().split(' '))) for _ in range(N)]

chick_list = []
house_list = []

for i in range(N):
    for j in range(N):
        if arr[i][j] == 1:
            house_list.append([i, j])
        if arr[i][j] == 2:
            chick_list.append([i, j])

comb_result = []
l = len(chick_list)
def combination(idx, r, comb):
    global comb_result, l
    if len(comb) == r:
        comb_result.append(comb[:])
        return
    for i in range(idx, l):
        combination(i + 1, r, comb+[chick_list[i]])

for i in range(M):
    chick_num = i + 1
    comb_result = []
    combination(0, chick_num, [])

    comb_len = len(comb_result)

    min_city_dist = 1000000
    for j in range(comb_len):
        chick_comb = comb_result[j]
        city_dist = 0
        for hx, hy in house_list:
            min_house_dist = 1000000
            for cx, cy in chick_comb:
                house_dist = abs(hx - cx) + abs(hy - cy)
                if house_dist < min_house_dist:
                    min_house_dist = house_dist
            city_dist += min_house_dist
        if city_dist < min_city_dist:
            min_city_dist = city_dist
print(min_city_dist)