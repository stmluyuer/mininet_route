import threading
from mininet.cli import CLI
from network_simulation import create_fat_tree
from dynamic_routing import dynamic_routing_decision
from simulate_changes import simulate_network_changes

def main():
    k = 4  # Fat-tree参数
    net, G = create_fat_tree(k)

    bandwidth_range = (500, 800)
    delay_range = (0.01, 0.03)

    # 创建一个锁对象
    lock = threading.Lock()

    # 创建并启动动态路由决策线程
    dynamic_routing_thread = threading.Thread(target=dynamic_routing_decision, args=(net, G, lock), daemon=True)
    dynamic_routing_thread.start()

    # 创建并启动模拟网络变化线程
    simulate_changes_thread = threading.Thread(target=simulate_network_changes, args=(net, bandwidth_range, delay_range, lock), daemon=True)
    simulate_changes_thread.start()

    CLI(net)
    net.stop()

if __name__ == "__main__":
    main()
