import numpy as np
import networkx as nx

# Thuật toán Bellman-Ford để tìm đường đi ngắn nhất trong đồ thị có trọng số
def bellman_ford(graph, source, sink):
    # Khởi tạo các khoảng cách từ nguồn tới các đỉnh khác là vô cùng
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0  # Khoảng cách từ nguồn đến chính nó là 0

    # Lặp để cập nhật khoảng cách từ nguồn tới các đỉnh khác
    for _ in range(graph.number_of_nodes() - 1):
        for u, v in graph.edges:
            capacity = graph[u][v].get('capacity', 0)
            cost = graph[u][v]['cost']
            # Nếu khoảng cách mới nhỏ hơn khoảng cách hiện tại và cạnh có dung lượng dương
            if distances[u] + cost < distances[v] and capacity > 0:
                distances[v] = distances[u] + cost

    return distances

# Thuật toán Edmonds-Karp để tìm Tìm luồng có chi phí nhỏ nhất
def edmonds_karp_min_cost(graph, source, sink, demand):
    # Tạo bản sao của đồ thị để thao tác
    residual_graph = graph.copy()
    min_cost = 0  # Khởi tạo chi phí tối thiểu

    while True:
        distances = bellman_ford(residual_graph, source, sink)

        # Nếu không thể đến được đích, thoát khỏi vòng lặp
        if distances[sink] == float('inf'):
            break

        # Tìm đường đi ngắn nhất từ nguồn tới đích
        path = nx.shortest_path(residual_graph, source=source, target=sink, weight='cost')

        # Tìm đoạn có sức chứa nhỏ nhất (sức chứa nhỏ nhất trên đường đi)
        bottleneck_capacity = min(residual_graph[u][v].get('capacity', 0) for u, v in zip(path, path[1:]))
        for u, v in zip(path, path[1:]):
            # Nếu đường đi đã đầy, gán chi phí lớn để loại bỏ đường này
            if residual_graph[u][v].get('capacity', 0) == 0:
                residual_graph[u][v]['cost'] = float('inf')
           
        if bottleneck_capacity != 0:
            for u, v in zip(path, path[1:]):
                if bottleneck_capacity < demand:
                    # Cập nhật dung lượng còn lại của cạnh và chi phí tối thiểu
                    if 'capacity' in residual_graph[u][v]:
                        residual_graph[u][v]['capacity'] -= bottleneck_capacity
                        min_cost += residual_graph[u][v].get('cost', 0) * bottleneck_capacity
                        # print("from", u, "to", v, "with cost", residual_graph[u][v].get('cost', 0), "and capacity", bottleneck_capacity)
                    else:
                        residual_graph[v][u]['capacity'] += bottleneck_capacity
                        
                    # Nếu có cạnh ngược, cập nhật dung lượng của cạnh đó
                    if residual_graph.has_edge(v, u):
                        if 'capacity' in residual_graph[v][u]:
                            residual_graph[v][u]['capacity'] += bottleneck_capacity
                        else:
                            residual_graph[u][v]['capacity'] -= bottleneck_capacity
                else:
                    # Cập nhật dung lượng còn lại của cạnh và chi phí tối thiểu
                    if 'capacity' in residual_graph[u][v]:
                        residual_graph[u][v]['capacity'] -= demand
                        min_cost += residual_graph[u][v].get('cost', 0) * demand
                        # print("from", u, "to", v, "with cost", residual_graph[u][v].get('cost', 0), "and capacity", demand)
                    else:
                        residual_graph[v][u]['capacity'] += demand
                        
                    # Nếu có cạnh ngược, cập nhật dung lượng của cạnh đó
                    if residual_graph.has_edge(v, u):
                        if 'capacity' in residual_graph[v][u]:
                            residual_graph[v][u]['capacity'] += demand
                        else:
                            residual_graph[u][v]['capacity'] -= demand
                            
            # Cập nhật dung lượng còn lại của nhu cầu
            if bottleneck_capacity < demand:
                demand -= bottleneck_capacity 
            else:
                return min_cost


# Dữ liệu cung cấp
start_nodes = np.array([0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6])
end_nodes   = np.array([1, 2, 2, 3, 4, 3, 4, 4, 5, 6, 5, 6, 6, 7, 7])
capacities  = np.array([6, 5, 4, 8, 3, 3, 8, 7, 5, 3, 7, 2, 1, 7, 2])
unit_costs  = np.array([5, 6, 7, 4, 8, 9, 2, 3, 5, 6, 4, 8, 9, 2, 8])
supplies = [8, 0, 0, 0, 0, 0, 0, -8]
demand = 8

graph = nx.DiGraph()

# Thêm cạnh với dung lượng và chi phí đơn vị
for i in range(len(start_nodes)):
    graph.add_edge(start_nodes[i], end_nodes[i], capacity=capacities[i], cost=unit_costs[i])

# Thêm nguồn cung và rò rỉ cho từng đỉnh
for i, supply in enumerate(supplies):
    graph.nodes[i]['supply'] = supply

# Xác định đỉnh nguồn và đỉnh đích
source_node = 0
sink_node = 7

# Tính luồng có chi phí tối thiểu sử dụng Edmonds-Karp và Bellman-Ford
min_cost_flow = edmonds_karp_min_cost(graph, source_node, sink_node, demand)

print("The minimum cost maximum flow is", min_cost_flow)
