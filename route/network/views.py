from django.shortcuts import render
from django.http import JsonResponse
from .models import LinkData
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
import networkx as nx

# 最短路径
def convert_to_float(value):
    try:
        if isinstance(value, str):
            value = value.replace('ms', '').replace('s', '').replace('kbps', '').replace('mbps', '')
        return float(value)
    except ValueError:
        return 0.0
def dynamic_routing_decision(request):
    if request.method == 'GET':
        src_node = request.GET.get('src')
        dst_node = request.GET.get('dst')

        if src_node and dst_node:
            print(f"Received src: {src_node}, dst: {dst_node}")
            link_data_list = LinkData.objects.all()
            G = nx.DiGraph()

            for link_data in link_data_list:
                node1, node2 = link_data.link.split('<->')
                bw = convert_to_float(link_data.bw)
                delay = convert_to_float(link_data.delay)
                loss = convert_to_float(link_data.loss)
                jitter = convert_to_float(link_data.jitter)
                error = convert_to_float(link_data.error)
                weight = (1 / bw) + (delay / 10) + (loss / 100) + (jitter / 10) + (error / 100)
                
                G.add_edge(node1, node2, weight=weight)
                G.add_edge(node2, node1, weight=weight)

            print("Graph nodes:", G.nodes())
            print("Graph edges:", G.edges(data=True))

            try:
                path = nx.dijkstra_path(G, src_node, dst_node)
                print(f"Found path: {path}")
                return JsonResponse({'path': path})
            except nx.NetworkXNoPath:
                print("No path found")
                return JsonResponse({'status': 'error', 'message': 'No path found'}, status=400)
        else:
            print("Source and destination nodes are required")
            return JsonResponse({'status': 'error', 'message': 'Source and destination nodes are required'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def reachable_nodes(request):
    if request.method == 'GET':
        src_node = request.GET.get('src')
        
        if src_node:
            link_data_list = LinkData.objects.all()
            G = nx.DiGraph()

            for link_data in link_data_list:
                node1, node2 = link_data.link.split('<->')
                bw = convert_to_float(link_data.bw)
                delay = convert_to_float(link_data.delay)
                loss = convert_to_float(link_data.loss)
                jitter = convert_to_float(link_data.jitter)
                error = convert_to_float(link_data.error)
                weight = (1 / bw) + (delay / 10) + (loss / 100) + (jitter / 10) + (error / 100)
                G.add_edge(node1, node2, weight=weight)

            try:
                reachable = nx.single_source_dijkstra_path_length(G, src_node)
                reachable_nodes = list(reachable.keys())
                return JsonResponse({'nodes': reachable_nodes})
            except nx.NetworkXNoPath:
                return JsonResponse({'status': 'error', 'message': 'No reachable nodes found'}, status=400)
        
        return JsonResponse({'status': 'error', 'message': 'Source node is required'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def home(request):
    return render(request, 'network/home.html')

def topology_view(request):
    return render(request, 'network/topology.html')

@csrf_exempt
def receive_link_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for link in data:
                link_str = link['link']
                LinkData.objects.update_or_create(
                    link=link_str,
                    defaults={
                        'bw': link['bw'],
                        'delay': link['delay'],
                        'loss': link['loss'],
                        'jitter': link['jitter'],
                        'error': link['error'],
                        'max_queue_size': link['max_queue_size'],
                        'rate': link['rate'],
                        'mtu': link['mtu'],
                        'timestamp': timezone.now()
                    }
                )
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'failed', 'reason': str(e)}, status=400)
    return JsonResponse({'status': 'invalid request'}, status=400)

def generate_topology(request):
    link_data_list = LinkData.objects.all()
    
    elements = []
    nodes = set()

    for link_data in link_data_list:
        node1, node2 = link_data.link.split('<->')
        nodes.add(node1)
        nodes.add(node2)
        elements.append({
            'data': {
                'id': f'{node1}-{node2}',
                'source': node1,
                'target': node2,
                'bw': link_data.bw,
                'delay': link_data.delay,
                'loss': link_data.loss,
                'jitter': link_data.jitter,
                'error': link_data.error,
                'max_queue_size': link_data.max_queue_size,
                'rate': link_data.rate,
                'mtu': link_data.mtu
            }
        })

    def get_node_type(node):
        if 'c' in node:
            return 'core'
        elif 'a' in node:
            return 'aggregation'
        elif 'e' in node:
            return 'edge'
        elif 'h' in node:
            return 'host'
        else:
            return 'unknown'

    for node in nodes:
        node_type = get_node_type(node)
        elements.append({'data': {'id': node, 'type': node_type}})

    return JsonResponse(elements, safe=False)

def get_link_data(request):
    link_data_list = LinkData.objects.all()
    
    elements = []

    for link_data in link_data_list:
        node1, node2 = link_data.link.split('<->')
        elements.append({
            'data': {
                'id': f'{node1}-{node2}',
                'source': node1,
                'target': node2,
                'bw': link_data.bw,
                'delay': link_data.delay,
                'loss': link_data.loss,
                'jitter': link_data.jitter,
                'error': link_data.error,
                'max_queue_size': link_data.max_queue_size,
                'rate': link_data.rate,
                'mtu': link_data.mtu,
                'timestamp': link_data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    return JsonResponse(elements, safe=False)

def link_data_table(request):
    link_data_list = LinkData.objects.all()
    return render(request, 'network/link_data_table.html', {'link_data_list': link_data_list})
