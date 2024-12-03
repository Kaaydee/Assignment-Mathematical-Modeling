from collections import deque
import sys
import matplotlib.pyplot as plt
import networkx as nx

INF = sys.maxsize


class Edge:
    def __init__(self, from_node, to, capacity, cost):
        self.from_node = from_node
        self.to = to
        self.capacity = capacity
        self.cost = cost


def shortest_paths(n, v0, d, p, adj, capacity, cost):
    d = [INF]*n
    d[v0] = 0
    inq = [False]*n
    q = deque([v0])
    p = [-1]*n

    while q:
        u = q.popleft()
        inq[u] = False
        for v in adj[u]:
            if capacity[u][v] > 0 and d[v] > d[u] + cost[u][v]:
                d[v] = d[u] + cost[u][v]
                p[v] = u
                if not inq[v]:
                    inq[v] = True
                    q.append(v)

    return d, p


def min_cost_flow(N, edges, K, s, t):
    adj = [[] for _ in range(N)]
    cost = [[0]*N for _ in range(N)]
    capacity = [[0]*N for _ in range(N)]
    flow = [[0]*N for _ in range(N)]
    for e in edges:
        adj[e.from_node].append(e.to)
        adj[e.to].append(e.from_node)
        cost[e.from_node][e.to] = e.cost
        cost[e.to][e.from_node] = -e.cost
        capacity[e.from_node][e.to] = e.capacity

    flow_total = 0
    cost_total = 0
    while flow_total < K:
        d, p = shortest_paths(N, s, [], [], adj, capacity, cost)
        if d[t] == INF:
            break

        f = K - flow_total
        cur = t
        while cur != s:
            f = min(f, capacity[p[cur]][cur])
            cur = p[cur]

        # apply flow
        flow_total += f
        cost_total += f * d[t]
        cur = t
        while cur != s:
            capacity[p[cur]][cur] -= f
            capacity[cur][p[cur]] += f
            flow[p[cur]][cur] += f
            cur = p[cur]

    # # Draw the graph
    # G = nx.DiGraph()
    # for e in edges:
    #     G.add_edge(e.from_node, e.to, capacity=e.capacity,
    #                flow=flow[e.from_node][e.to])

    # pos = nx.circular_layout(G)
    # nx.draw(G, pos, with_labels=True)
    # edge_labels = nx.get_edge_attributes(G, 'flow')
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    # plt.show()

    if flow_total < K:
        return -1
    else:
        return cost_total


edges = [
    Edge(0, 1, 6, 5),
    Edge(0, 2, 5, 6),
    Edge(1, 2, 4, 7),
    Edge(1, 3, 8, 4),
    Edge(1, 4, 3, 8),
    Edge(2, 3, 3, 9),
    Edge(2, 4, 8, 2),
    Edge(3, 4, 7, 3),
    Edge(3, 5, 5, 5),
    Edge(3, 6, 3, 6),
    Edge(4, 5, 7, 4),
    Edge(4, 6, 2, 8),
    Edge(5, 6, 1, 9),
    Edge(5, 7, 7, 2),
    Edge(6, 7, 2, 8)
]

N = 8
K = 8
s = 0
t = 7

result = min_cost_flow(N, edges, K, s, t)

print(f"The minimum cost maximum flow is {result}")
