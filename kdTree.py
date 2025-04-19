from math import radians, cos, sin, asin, sqrt

class Accident:
    def __init__(self, point, data):
        self.point = point      # (lat, long)
        self.data = data        # dictionary with ID, Severity, City, State, Zipcode
        self.left = None
        self.right = None


def insert_rec(root, point, data, depth=0):
    if not root:
        return Accident(point, data)

    # alternate between latitude (0) and longitude (1)
    cd = depth % 2

    if point[cd] < root.point[cd]:
        root.left = insert_rec(root.left, point, data, depth + 1)
    else:
        root.right = insert_rec(root.right, point, data, depth + 1)

    return root

def print_tree(root, depth=0):
    if not root:
        return

    print(f"{'  ' * depth}Node at depth {depth}: (Lat: {root.point[0]}, Long: {root.point[1]})")
    print(f"{'  ' * depth}Data: {root.data}")

    print_tree(root.left, depth + 1)
    print_tree(root.right, depth + 1)

def haversine_dist(point1, point2):
    lat1 = radians(point1[0])
    lat2 = radians(point2[0])
    long1 = radians(point1[1])
    long2 = radians(point2[1])

    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlong / 2) ** 2

    c = 2 * asin(sqrt(a))

    # radius of earth in miles
    r = 3956

    return (c * r)


def bfs_with_pruning(root, search_center, radius):
    if not root: #if root doesn't exist
        return []

    results = []
    queue = [(root, 0)]  # item is tuple: (node, depth)

    while queue: # queue is not empty
        current_node, depth = queue.pop(0)

        # distance to search center calculated
        distance = haversine_dist(search_center, current_node.point)

        if distance <= radius: # add to results if within radius
            results.append(current_node.data)

        # k=2, so cuts dimension between 0 for latitude and 1 for longitude
        cd = depth % 2

        # pruning where left and right children are explored only if within current dimension
        if current_node.left and (search_center[cd] - radius) <= current_node.point[cd]:
            queue.append((current_node.left, depth + 1))

        if current_node.right and (search_center[cd] + radius) >= current_node.point[cd]:
            queue.append((current_node.right, depth + 1))

    return results


def dfs_with_pruning(node, search_center, radius, depth=0, results=None):
    if node is None:  #if root doesn't exist
        return

    if results is None:
        results = []

    # distance to search center calculated
    distance = haversine_dist(search_center, node.point)

    if distance <= radius: # add to results if within radius
        results.append(node.data)

    # k=2, so cuts dimension between 0 for latitude and 1 for longitude
    cd = depth % 2

    # pruning where left and right children are explored only if within current dimension
    if node.left and (search_center[cd] - radius) <= node.point[cd]:
        dfs_with_pruning(node.left, search_center, radius, depth + 1, results)

    if node.right and (search_center[cd] + radius) >= node.point[cd]:
        dfs_with_pruning(node.right, search_center, radius, depth + 1, results)

    return results