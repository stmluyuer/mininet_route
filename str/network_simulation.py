from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
import networkx as nx

def create_fat_tree(k):
    net = Mininet(controller=lambda name: RemoteController(name, ip='127.0.0.1', port=6633), link=TCLink)
    num_pods = k
    num_hosts_per_edge = k // 2
    num_agg_switches_per_pod = k // 2
    num_edge_switches_per_pod = k // 2
    num_core_switches = (k // 2) ** 2

    core_switches = [net.addSwitch(f'c{i}') for i in range(1, num_core_switches + 1)]
    agg_switches = [net.addSwitch(f'a{p}{i}') for p in range(1, num_pods + 1) for i in range(1, num_agg_switches_per_pod + 1)]
    edge_switches = [net.addSwitch(f'e{p}{i}') for p in range(1, num_pods + 1) for i in range(1, num_edge_switches_per_pod + 1)]
    hosts = [net.addHost(f'h{p}{e}{i}') for p in range(1, num_pods + 1) for e in range(1, num_edge_switches_per_pod + 1) for i in range(1, num_hosts_per_edge + 1)]

    bandwidth_range = (500, 800)
    delay_range = (0.01, 0.03)

    from link_properties import set_link_properties

    for core_index, core_switch in enumerate(core_switches):
        for pod in range(num_pods):
            agg_switch = agg_switches[core_index // num_agg_switches_per_pod + pod * num_agg_switches_per_pod]
            link = net.addLink(core_switch, agg_switch)
            set_link_properties(link, bandwidth_range, delay_range)

    for pod in range(num_pods):
        for agg_index in range(num_agg_switches_per_pod):
            agg_switch = agg_switches[agg_index + pod * num_agg_switches_per_pod]
            for edge_index in range(num_edge_switches_per_pod):
                edge_switch = edge_switches[edge_index + pod * num_edge_switches_per_pod]
                link = net.addLink(agg_switch, edge_switch)
                set_link_properties(link, bandwidth_range, delay_range)

    for pod in range(num_pods):
        for edge_index in range(num_edge_switches_per_pod):
            edge_switch = edge_switches[edge_index + pod * num_edge_switches_per_pod]
            for host_index in range(num_hosts_per_edge):
                host = hosts[host_index + edge_index * num_hosts_per_edge + pod * num_edge_switches_per_pod * num_hosts_per_edge]
                link = net.addLink(edge_switch, host)
                set_link_properties(link, bandwidth_range, delay_range)

    net.start()

    G = nx.Graph()
    for switch in net.switches:
        G.add_node(switch.name, layer='switch')
    for host in net.hosts:
        G.add_node(host.name, layer='host')
    for link in net.links:
        G.add_edge(link.intf1.node.name, link.intf2.node.name, weight=1)

    print(f"图中共有 {G.number_of_nodes()} 个节点和 {G.number_of_edges()} 条边")

    return net, G
