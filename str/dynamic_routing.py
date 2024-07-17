import networkx as nx
import time
import json
import requests

def collect_link_info(net):
    link_info = {}
    for link in net.links:
        bw1 = link.intf1.params.get('bw', None)
        bw2 = link.intf2.params.get('bw', None)
        delay1 = link.intf1.params.get('delay', None)
        delay2 = link.intf2.params.get('delay', None)
        if bw1 is not None and bw2 is not None and delay1 is not None and delay2 is not None:
            link_info[(link.intf1.node.name, link.intf2.node.name)] = {
                'bw': (bw1 + bw2) / 2,
                'delay': (float(delay1[:-2]) + float(delay2[:-2])) / 2,
            }
    return link_info

def apply_routing_rules(src, dst, path):
    #print(f"下发新的路由规则：从 {src} 到 {dst}，路径: {' -> '.join(path)}")
    pass

def dynamic_routing_decision(net, G, lock):
    while True:
        with lock:
            link_info = collect_link_info(net)
            for (src, dst), info in link_info.items():
                bw = info['bw']
                delay = info['delay']
                loss = info.get('loss', 0)
                jitter = info.get('jitter', 0)
                error = info.get('error', 0)
                weight = (1 / bw) + (delay / 10) + (loss / 100) + (jitter / 10) + (error / 100)
                G[src][dst]['weight'] = weight

            for src in G.nodes():
                for dst in G.nodes():
                    if src != dst and 'host' in G.nodes[src]['layer'] and 'host' in G.nodes[dst]['layer']:
                        try:
                            path = nx.dijkstra_path(G, src, dst)
                            apply_routing_rules(src, dst, path)
                            print(f"{src} 到 {dst} 的最短路径: {' -> '.join(path)}")
                        except nx.NetworkXNoPath:
                            print(f"{src} 和 {dst} 之间没有路径")


            # # 将计算结果发送到Django后端
            # url = 'http://127.0.0.1:8001/dynamic-routing/'  # 替换为实际Django后端URL
            # data = json.dumps(paths)
            # response = requests.post(url, data=data)
            # print(data)
            # if response.status_code == 200:
            #     print("路径信息成功发送到Django后端")
            # else:
            #     print(f"发送失败，状态码: {response.status_code}")

        time.sleep(5)

