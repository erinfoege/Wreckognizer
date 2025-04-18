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
