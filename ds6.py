import numpy as np

class QuadTreeNode:
    def __init__(self, boundary):
        self.boundary = boundary   # (x, y, width, height)
        self.cities = []
        self.children = [None, None, None, None]


class QuadTree:
    def __init__(self, boundary, capacity):
        self.root = QuadTreeNode(boundary)
        self.capacity = capacity

    def insert(self, city):
        self._insert_recursive(self.root, city)

    def _insert_recursive(self, node, city):
        if not self._contains(node.boundary, city):
            return

        if len(node.cities) < self.capacity and node.children[0] is None:
            node.cities.append(city)
            return

        if node.children[0] is None:
            self._subdivide(node)

        for i in range(4):
            self._insert_recursive(node.children[i], city)

    def _subdivide(self, node):
        x, y, w, h = node.boundary
        half_w = w / 2
        half_h = h / 2

        node.children[0] = QuadTreeNode((x + half_w, y, half_w, half_h))       # NE
        node.children[1] = QuadTreeNode((x, y, half_w, half_h))               # NW
        node.children[2] = QuadTreeNode((x, y + half_h, half_w, half_h))      # SW
        node.children[3] = QuadTreeNode((x + half_w, y + half_h, half_w, half_h))  # SE

        # Reinsert existing cities
        old_cities = node.cities
        node.cities = []

        for city in old_cities:
            for i in range(4):
                if self._contains(node.children[i].boundary, city):
                    self._insert_recursive(node.children[i], city)

    def _contains(self, boundary, city):
        x, y, w, h = boundary
        return x <= city[0] < x + w and y <= city[1] < y + h

    # Query all cities in region of query point
    def query_location(self, query_point):
        return self._query_location_recursive(self.root, query_point)

    def _query_location_recursive(self, node, query_point):
        if node is None or not self._contains(node.boundary, query_point):
            return []

        if node.children[0] is None:
            return node.cities

        result = []
        for child in node.children:
            result.extend(self._query_location_recursive(child, query_point))
        return result

    # Nearest city search
    def query_nearest_city(self, query_point):
        nearest_city, _ = self._query_nearest(self.root, query_point, float('inf'), None)
        return nearest_city

    def _query_nearest(self, node, query_point, min_dist, nearest_city):
        if node is None:
            return nearest_city, min_dist

        if not self._contains(node.boundary, query_point):
            return nearest_city, min_dist

        for city in node.cities:
            dist = np.linalg.norm(np.array(city) - np.array(query_point))
            if dist < min_dist:
                min_dist = dist
                nearest_city = city

        for child in node.children:
            if child is not None:
                nearest_city, min_dist = self._query_nearest(child, query_point, min_dist, nearest_city)

        return nearest_city, min_dist


# ================= USER INPUT =================

# Boundary input
boundary = tuple(map(int, input("Enter boundary (x y width height): ").split()))
capacity = int(input("Enter node capacity: "))

qt = QuadTree(boundary, capacity)

# Insert cities
n = int(input("Enter number of cities: "))
for _ in range(n):
    city = tuple(map(int, input("Enter city (x y): ").split()))
    qt.insert(city)

# Query point
query_point = tuple(map(int, input("Enter query point (x y): ").split()))

# Results
print("Cities in same region:", qt.query_location(query_point))
print("Nearest city:", qt.query_nearest_city(query_point))