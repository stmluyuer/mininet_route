class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.edges = []

class Edge:
    def __init__(self, start, end, delay, bandwidth, loss_rate):
        self.start = start
        self.end = end
        self.delay = delay
        self.bandwidth = bandwidth
        self.loss_rate = loss_rate

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id)

    def add_edge(self, start, end, delay, bandwidth, loss_rate):
        if start not in self.nodes or end not in self.nodes:
            print(f"错误: 节点 {start} 或 {end} 不存在于图中")
            return
        edge = Edge(start, end, delay, bandwidth, loss_rate)
        self.nodes[start].edges.append(edge)
        self.nodes[end].edges.append(edge)
        self.edges.append(edge)

    def get_edge_weight(self, start, end):
        for edge in self.edges:
            if (edge.start == start and edge.end == end) or (edge.start == end and edge.end == start):
                return (1 / edge.bandwidth) + (edge.delay / 10) + (edge.loss_rate / 100)
        return float('inf')  # 无法到达时返回无穷大

    def get_shortest_path(self, src, dst):
        import heapq
        queue = [(0, src, [])]
        seen = set()
        while queue:
            (cost, node, path) = heapq.heappop(queue)
            if node in seen:
                continue
            path = path + [node]
            if node == dst:
                return (cost, path)
            seen.add(node)
            for edge in self.nodes[node].edges:
                next_node = edge.end if edge.start == node else edge.start
                if next_node not in seen:
                    next_cost = cost + self.get_edge_weight(node, next_node)
                    heapq.heappush(queue, (next_cost, next_node, path))
        return (float('inf'), [])  # 无法到达时返回无穷大和空路径