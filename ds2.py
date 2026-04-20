import heapq

class Graph:
    def __init__(self):
        self.edges = {}

    def add_edge(self, u, v, w):
        self.edges.setdefault(u, []).append((v, w))
        self.edges.setdefault(v, []).append((u, w))  # undirected


def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph.edges}
    prev = {node: None for node in graph.edges}

    dist[start] = 0
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)

        for v, w in graph.edges[u]:
            new_d = d + w

            if new_d < dist[v]:
                dist[v] = new_d
                prev[v] = u
                heapq.heappush(pq, (new_d, v))

    return dist, prev


def get_path(prev, end):
    path = []
    while end:
        path.append(end)
        end = prev[end]
    return path[::-1]


# Example
g = Graph()
g.add_edge("A", "B", 4)
g.add_edge("A", "C", 2)
g.add_edge("B", "C", 1)
g.add_edge("B", "D", 5)
g.add_edge("C", "D", 8)

start = "A"
end = "D"

dist, prev = dijkstra(g, start)
path = get_path(prev, end)

print("Shortest Route:", " -> ".join(path))
print("Travel Time:", dist[end])