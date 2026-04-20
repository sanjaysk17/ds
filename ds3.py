class DisjointSet:
    def __init__(self, vertices):
        # Each node is its own parent initially
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, vertex):
        # Find root with path compression
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            # Union by rank
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1


def kruskal(vertices, edges):
    mst = []
    ds = DisjointSet(vertices)

    # Sort edges based on weight
    edges.sort(key=lambda x: x[2])

    for u, v, w in edges:
        if ds.find(u) != ds.find(v):
            ds.union(u, v)
            mst.append((u, v, w))

    return mst


# 🔹 Main Function (User Input)
def main():
    # Input vertices
    vertices = input("Enter cities (space-separated): ").split()

    # Input edges
    n = int(input("Enter number of connections: "))
    edges = []

    print("Enter connections (city1 city2 cost):")
    for _ in range(n):
        u, v, w = input().split()
        edges.append((u, v, int(w)))

    # Run Kruskal
    mst = kruskal(vertices, edges)

    # Output
    print("\nMinimum Spanning Tree:")
    total_cost = 0

    for u, v, w in mst:
        print(f"{u} - {v} : {w}")
        total_cost += w

    print("Total Cost:", total_cost)


# Run program
if __name__ == "__main__":
    main()