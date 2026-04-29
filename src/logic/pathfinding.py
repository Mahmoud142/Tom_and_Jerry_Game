import heapq

def heuristic(a, b):
    # Manhattan distance: optimal for grid movement without diagonal shortcuts
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path_a_star(start, end, state):
    # A* Algorithm: uses a heuristic to guide the search towards the target,
    # making it much faster than Dijkstra for finding paths in large open maps.
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        # 8-direction movement for A* (including diagonals)
        for di, dj in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            neighbor = (current[0] + di, current[1] + dj)
            if state.is_valid(neighbor):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score, neighbor))
                    came_from[neighbor] = current
    return []

def find_path_dijkstra(start, end, state):
    # Dijkstra's Algorithm: explores uniformly in all directions.
    # Guarantees the shortest path but checks more nodes since there is no heuristic.
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_list:
        current_g, current = heapq.heappop(open_list)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (current[0] + di, current[1] + dj)
            if state.is_valid(neighbor):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    # Dijkstra does not use a heuristic, so priority is just g_score
                    heapq.heappush(open_list, (tentative_g, neighbor))
                    came_from[neighbor] = current
    return []
