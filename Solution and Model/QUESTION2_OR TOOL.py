"""From Bradley, Hax and Maganti, 'Applied Mathematical Programming', figure 8.1."""
import numpy as np
import time
from ortools.graph.python import min_cost_flow
start = time.time()

"""MinCostFlow simple interface example."""
# Instantiate a SimpleMinCostFlow solver.
smcf = min_cost_flow.SimpleMinCostFlow()

# Define four parallel arrays: sources, destinations, capacities,
# and unit costs between each pair. For instance, the arc from node 0
# to node 1 has a capacity of 15.
start_nodes = np.array([0, 0, 1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6])
end_nodes   = np.array([1, 2, 2, 3, 4, 3, 4, 4, 5, 6, 5, 6, 6, 7, 7])
capacities  = np.array([6, 5, 4, 8, 3, 3, 8, 7, 5, 3, 7, 2, 1, 7, 2])
unit_costs  = np.array([5, 6, 7, 4, 8, 9, 2, 3, 5, 6, 4, 8, 9, 2, 8])

# Define an array of supplies at each node.
supplies = [8, 0, 0, 0, 0, 0, 0, -8]

# Add arcs, capacities and costs in bulk using numpy.
all_arcs = smcf.add_arcs_with_capacity_and_unit_cost(
    start_nodes, end_nodes, capacities, unit_costs
)

# Add supply for each nodes.
smcf.set_nodes_supplies(np.arange(0, len(supplies)), supplies)

# Find the min cost flow.
status = smcf.solve()

if status != smcf.OPTIMAL:
    print("There was an issue with the min cost flow input.")
    print(f"Status: {status}")
    exit(1)
print(f"Minimum cost: {smcf.optimal_cost()}")
print("")
print(" Arc    Flow / Capacity Cost")
solution_flows = smcf.flows(all_arcs)
costs = solution_flows * unit_costs
for arc, flow, cost in zip(all_arcs, solution_flows, costs):
    print(
        f"{smcf.tail(arc):1} -> {smcf.head(arc)}  {flow:3}  / {smcf.capacity(arc):3}       {cost}"
    )
end = time.time()
# tính thời gian
print(end-start)