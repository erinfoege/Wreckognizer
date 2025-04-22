from kdTree import haversine_dist, time

class QuadNode:
    def __init__(self, point, data, bounds):
        self.point = point
        self.data = data
        self.bounds = bounds  # (min_lat, max_lat, min_long, max_lng)
        self.NE = None
        self.NW = None
        self.SE = None
        self.SW = None

def insert_quad(node, point, data):
    if node is None:
        # bounds of the USA (approx, no Alaska/Hawaii)
        bounds = (24.30, 49.24, -124.37, -66.58)
        return QuadNode(point, data, bounds)

    min_lat, max_lat, min_lng, max_lng = node.bounds
    mid_lat = (min_lat + max_lat) / 2
    mid_lng = (min_lng + max_lng) / 2

    if point[0] >= mid_lat:
        if point[1] >= mid_lng:
            if node.NE is None:
                node.NE = QuadNode(point, data, (mid_lat, max_lat, mid_lng, max_lng))
            else:
                node.NE = insert_quad(node.NE, point, data)
        else:
            if node.NW is None:
                node.NW = QuadNode(point, data, (mid_lat, max_lat, min_lng, mid_lng))
            else:
                node.NW = insert_quad(node.NW, point, data)
    else:
        if point[1] >= mid_lng:
            if node.SE is None:
                node.SE = QuadNode(point, data, (min_lat, mid_lat, mid_lng, max_lng))
            else:
                node.SE = insert_quad(node.SE, point, data)
        else:
            if node.SW is None:
                node.SW = QuadNode(point, data, (min_lat, mid_lat, min_lng, mid_lng))
            else:
                node.SW = insert_quad(node.SW, point, data)

    return node

# dfs structured search
def radius_search_quad(node, center, radius, results=None):
    if node is None:
        return results if results else []

    if results is None:
        results = []

    if haversine_dist(center, node.point) <= radius: #using haversine for distance on Earth
        results.append(node.data)

    def region_might_intersect(bounds, center, radius):
        min_lat, max_lat, min_long, max_long = bounds
        lat, lng = center


        #clamp center to bounds to get closest point
        clamped_lat = max(min_lat, min(lat, max_lat))
        clamped_lng = max(min_long, min(lng, max_long))

        # distance from center to closest point ≤ radius = intersection
        distance = haversine_dist(center, (clamped_lat, clamped_lng))
        return distance <= radius

    for child in [node.NE, node.NW, node.SE, node.SW]:
        if child and region_might_intersect(child.bounds, center, radius):
            radius_search_quad(child, center, radius, results)

    return results

def quad_search(root, search_location, radius):
    start = time.perf_counter()
    resultsQuad = radius_search_quad(root, search_location, radius)
    end = time.perf_counter()
    quadTime = end - start

    print(f"QuadTree Accidents within {radius} miles of {search_location}:")
    print("Quad Total:", len(resultsQuad), f" in {quadTime} seconds\n")
    return resultsQuad

