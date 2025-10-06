import heapq

def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def heuristic(i, j, len_s1, len_s2):
    return abs(len_s1 - i) + abs(len_s2 - j)

def a_star_text_alignment(S1, S2):
    len_s1, len_s2 = len(S1), len(S2)
    OpenSet = [(0 + heuristic(0, 0, len_s1, len_s2), 0, 0, 0)]
    gScore = {(0, 0): 0}
    CameFrom = {}

    while OpenSet:
        f, cost, i, j = heapq.heappop(OpenSet)
        if i == len_s1 and j == len_s2:
            break
        for i_next, j_next in [(i + 1, j), (i, j + 1), (i + 1, j + 1)]:
            if i_next <= len_s1 and j_next <= len_s2:
                s1_word = S1[i] if i < len_s1 else ""
                s2_word = S2[j] if j < len_s2 else ""
                extraCost = levenshtein_distance(s1_word, s2_word)
                newCost = cost + extraCost
                if (i_next, j_next) not in gScore or newCost < gScore[(i_next, j_next)]:
                    gScore[(i_next, j_next)] = newCost
                    fScore = newCost + heuristic(i_next, j_next, len_s1, len_s2)
                    heapq.heappush(OpenSet, (fScore, newCost, i_next, j_next))
                    CameFrom[(i_next, j_next)] = (i, j)

    alignment_path = []
    current = (len_s1, len_s2)
    while current in CameFrom:
        alignment_path.append(current)
        current = CameFrom[current]
    alignment_path.append((0, 0))
    alignment_path.reverse()
    return alignment_path

if __name__ == "__main__":
    S1 = ["I", "like", "apples"]
    S2 = ["I", "love", "apple"]
    result = a_star_text_alignment(S1, S2)
    print("Alignment Path:", result)
