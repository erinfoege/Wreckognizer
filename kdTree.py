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

    # Alternate between latitude (0) and longitude (1)
    cd = depth % 2

    if point[cd] < root.point[cd]:
        root.left = insert_rec(root.left, point, data, depth + 1)
    else:
        root.right = insert_rec(root.right, point, data, depth + 1)

    return root

def print_tree(root, depth=0):
    if not root:
        return

    # Print current node with its depth
    print(f"{'  ' * depth}Node at depth {depth}: (Lat: {root.point[0]}, Long: {root.point[1]})")
    print(f"{'  ' * depth}Data: {root.data}")

    # Recursively print left and right subtrees
    print_tree(root.left, depth + 1)
    print_tree(root.right, depth + 1)

def haversine_dist(point1, point2):
    lat1 = radians(point1[0])
    lat2 = radians(point2[0])
    long1 = radians(point1[1])
    long2 = radians(point2[1])

    # Haversine formula (from web, how to calc distance on Earth)
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlong / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in miles
    r = 3956

    # calculate the result
    return (c * r)