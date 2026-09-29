"""
CSC 645 - Assignment 3
Riley Elliott

This program compares uniform-cost, greedy best-first, and A* search.
It builds a visibility graph where the states are the start point, goal
point, and polygon vertices. Two states are connected when the straight
line between them does not pass through an obstacle.
"""

import heapq
import math


# ------------------------------------------------------------
# Problem data: change these values to test a different problem.
# Each point is written as (x, y). Polygon vertices should be listed
# in order around the outside of the polygon.
# ------------------------------------------------------------
START = (0.56, 1.10)
GOAL = (10.52, 6.10)

POLYGONS = [
    [(1.12, 5.54), (1.68, 4.98), (1.12, 3.32), (0.56, 4.98)],
    [(3.32, 6.42), (4.44, 4.44), (2.22, 3.34)],
    [(4.98, 6.42), (6.10, 6.10), (5.56, 5.52)],
    [(7.20, 6.10), (7.76, 5.54), (6.64, 4.44), (6.08, 4.98)],
    [(9.42, 6.42), (9.98, 5.54), (8.86, 4.98), (8.32, 6.08)],
    [(6.10, 4.66), (5.56, 2.88), (4.44, 3.60)],
    [(6.64, 3.32), (7.22, 2.78), (6.10, 2.22), (5.56, 2.76)],
    [(1.68, 2.78), (2.68, 1.68), (1.12, 1.12)],
    [(3.88, 3.32), (4.44, 1.12), (3.32, 0.56), (2.78, 1.68)],
    [(5.56, 2.76), (6.10, 1.10), (5.00, 0.56), (4.44, 1.68)],
    [(8.32, 4.44), (8.86, 2.22), (7.76, 1.10), (7.20, 3.32)],
    [(8.86, 4.44), (10.54, 3.32), (9.42, 2.78)],
    [(8.86, 2.78), (10.54, 2.22), (9.42, 0.56)],
]

SMALL_NUMBER = 1e-9


def straight_distance(point1, point2):
    # Distance formula between two points
    return math.hypot(point2[0] - point1[0], point2[1] - point1[1])


def turn_direction(a, b, c):
    # Tells which way three points turn
    value = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if abs(value) < SMALL_NUMBER:
        return 0
    return 1 if value > 0 else -1


def segments_cross(a, b, c, d):
    # Checks if two line segments cross
    return turn_direction(a, b, c) * turn_direction(a, b, d) < 0 and \
        turn_direction(c, d, a) * turn_direction(c, d, b) < 0


def point_on_segment(point, a, b):
    if turn_direction(a, b, point) != 0:
        return False
    return (
        min(a[0], b[0]) - SMALL_NUMBER <= point[0] <= max(a[0], b[0]) + SMALL_NUMBER
        and min(a[1], b[1]) - SMALL_NUMBER <= point[1] <= max(a[1], b[1]) + SMALL_NUMBER
    )


def inside_obstacle(point, polygon):
    # Uses a ray test to see if a point is inside a polygon
    for index in range(len(polygon)):
        a = polygon[index]
        b = polygon[(index + 1) % len(polygon)]
        if point_on_segment(point, a, b):
            return False

    inside = False
    x, y = point
    previous = len(polygon) - 1

    for current in range(len(polygon)):
        x1, y1 = polygon[current]
        x2, y2 = polygon[previous]
        crosses_ray = (y1 > y) != (y2 > y)
        if crosses_ray:
            crossing_x = (x2 - x1) * (y - y1) / (y2 - y1) + x1
            if x < crossing_x:
                inside = not inside
        previous = current

    return inside


def edge_touch_positions(a, b, c, d):
    # Finds where one line touches another line
    ab_x = b[0] - a[0]
    ab_y = b[1] - a[1]
    cd_x = d[0] - c[0]
    cd_y = d[1] - c[1]
    denominator = ab_x * cd_y - ab_y * cd_x

    if abs(denominator) > SMALL_NUMBER:
        ac_x = c[0] - a[0]
        ac_y = c[1] - a[1]
        t = (ac_x * cd_y - ac_y * cd_x) / denominator
        u = (ac_x * ab_y - ac_y * ab_x) / denominator
        if -SMALL_NUMBER <= t <= 1.0 + SMALL_NUMBER and -SMALL_NUMBER <= u <= 1.0 + SMALL_NUMBER:
            return [max(0.0, min(1.0, t))]
        return []

    # Parallel edges only matter here if they are on the same line.
    if turn_direction(a, b, c) != 0:
        return []

    length_squared = ab_x * ab_x + ab_y * ab_y
    if length_squared < SMALL_NUMBER:
        return []

    values = []
    for point in (c, d):
        t = ((point[0] - a[0]) * ab_x + (point[1] - a[1]) * ab_y) / length_squared
        if -SMALL_NUMBER <= t <= 1.0 + SMALL_NUMBER:
            values.append(max(0.0, min(1.0, t)))
    return values


def clear_line(a, b, polygons):
    # True means the robot can move straight from a to b
    if a == b:
        return False

    for polygon in polygons:
        # A segment cannot cross an obstacle edge.
        for index in range(len(polygon)):
            c = polygon[index]
            d = polygon[(index + 1) % len(polygon)]
            if segments_cross(a, b, c, d):
                return False

        # Split the route at every obstacle-boundary contact. Checking the
        # middle of each part reliably catches any part inside the polygon.
        amounts = [0.0, 1.0]
        for index in range(len(polygon)):
            c = polygon[index]
            d = polygon[(index + 1) % len(polygon)]
            amounts.extend(edge_touch_positions(a, b, c, d))

        amounts = sorted(set(round(value, 12) for value in amounts))
        for index in range(len(amounts) - 1):
            amount = (amounts[index] + amounts[index + 1]) / 2.0
            sample = (
                a[0] + amount * (b[0] - a[0]),
                a[1] + amount * (b[1] - a[1]),
            )
            if inside_obstacle(sample, polygon):
                return False

    return True


def make_search_map(start, goal, polygons):
    # Make a graph containing all points that can see each other
    points = [start, goal]
    point_names = {start: "S", goal: "G"}

    vertex_number = 1
    for polygon in polygons:
        for vertex in polygon:
            if vertex not in point_names:
                points.append(vertex)
                point_names[vertex] = "V" + str(vertex_number)
                vertex_number += 1

    search_map = {point: [] for point in points}

    for first in range(len(points)):
        for second in range(first + 1, len(points)):
            a = points[first]
            b = points[second]
            if clear_line(a, b, polygons):
                cost = straight_distance(a, b)
                search_map[a].append((b, cost))
                search_map[b].append((a, cost))

    return search_map, point_names


def queue_score(method, route_cost, point, goal):
    # Each search method puts a different score in the priority queue
    estimated_distance = straight_distance(point, goal)

    if method == "uniform-cost":
        return route_cost
    if method == "greedy":
        return estimated_distance
    if method == "astar":
        return route_cost + estimated_distance
    raise ValueError("Unknown search method: " + method)


def find_route(search_map, start, goal, method):
    open_list = []
    tie_number = 0
    heapq.heappush(open_list, (queue_score(method, 0.0, start, goal), tie_number, start))

    came_from = {start: None}
    lowest_cost = {start: 0.0}
    visited = set()

    while open_list:
        unused_score, unused_number, current_point = heapq.heappop(open_list)

        if current_point in visited:
            continue

        visited.add(current_point)

        if current_point == goal:
            route = []
            while current_point is not None:
                route.append(current_point)
                current_point = came_from[current_point]
            route.reverse()
            return route, lowest_cost[goal], len(visited)

        for next_point, step_cost in search_map[current_point]:
            new_cost = lowest_cost[current_point] + step_cost

            if next_point not in lowest_cost or new_cost < lowest_cost[next_point]:
                lowest_cost[next_point] = new_cost
                came_from[next_point] = current_point
                tie_number += 1
                score = queue_score(method, new_cost, next_point, goal)
                heapq.heappush(open_list, (score, tie_number, next_point))

    return None, math.inf, len(visited)


def show_result(title, result, point_names):
    route, cost, expanded_nodes = result
    print(title)

    if route is None:
        print("  No collision-free path was found.")
    else:
        named_path = " -> ".join(point_names[point] for point in route)
        coordinate_path = " -> ".join(str(point) for point in route)
        print("  Path:", named_path)
        print("  Coordinates:", coordinate_path)
        print("  Total cost:", round(cost, 3))

    print("  Expanded nodes:", expanded_nodes)
    print()


def main():
    search_map, point_names = make_search_map(START, GOAL, POLYGONS)

    results = {
        "Uniform-cost search": find_route(search_map, START, GOAL, "uniform-cost"),
        "Greedy best-first search": find_route(search_map, START, GOAL, "greedy"),
        "A* search": find_route(search_map, START, GOAL, "astar"),
    }

    print("ROUTE-FINDING SEARCH COMPARISON")
    print("Start:", START)
    print("Goal:", GOAL)
    print()

    for title, result in results.items():
        show_result(title, result, point_names)

    print("Brief comparison:")
    print("- Uniform-cost search uses only the path cost already traveled.")
    print("- Greedy search uses only estimated distance to the goal. It may be fast,")
    print("  but it is not guaranteed to find the lowest-cost path.")
    print("- A* uses both path cost and estimated distance. With straight-line")
    print("  distance as the heuristic, A* finds an optimal path and usually")
    print("  expands fewer nodes than uniform-cost search.")
    print()
    print("Success! All three search algorithms finished.")


if __name__ == "__main__":
    main()
