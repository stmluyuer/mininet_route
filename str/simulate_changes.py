import requests
import time
from link_properties import set_link_properties

def simulate_network_changes(net, bandwidth_range, delay_range, lock, loss_range=(0, 5), jitter_range=(0, 10), error_range=(0, 1), max_queue_size_range=(100, 1000), rate_range=(10, 1000), mtu_range=(1500, 9000)):
    while True:
        try:
            all_links_data = []
            with lock:
                for link in net.links:
                    set_link_properties(link, bandwidth_range, delay_range, loss_range, jitter_range, error_range, max_queue_size_range, rate_range, mtu_range)
                    bw1 = link.intf1.params.get('bw', None)
                    bw2 = link.intf2.params.get('bw', None)
                    delay1 = link.intf1.params.get('delay', None)
                    delay2 = link.intf2.params.get('delay', None)
                    loss1 = link.intf1.params.get('loss', None)
                    loss2 = link.intf2.params.get('loss', None)
                    jitter1 = link.intf1.params.get('jitter', None)
                    jitter2 = link.intf2.params.get('jitter', None)
                    error1 = link.intf1.params.get('error', None)
                    error2 = link.intf2.params.get('error', None)
                    queue_size1 = link.intf1.params.get('max_queue_size', None)
                    queue_size2 = link.intf2.params.get('max_queue_size', None)
                    rate1 = link.intf1.params.get('rate', None)
                    rate2 = link.intf2.params.get('rate', None)
                    mtu1 = link.intf1.params.get('mtu', None)
                    mtu2 = link.intf2.params.get('mtu', None)

                    link_data = {
                        'link': f"{link.intf1.node.name}<->{link.intf2.node.name}",
                        'bw': round(link.intf1.params.get('bw', 0), 2),
                        'delay': f"{round(float(link.intf1.params.get('delay', '0ms')[:-2]), 2)}ms",
                        'loss': round(link.intf1.params.get('loss', 0), 2),
                        'jitter': f"{round(float(link.intf1.params.get('jitter', '0ms')[:-2]), 2)}ms",
                        'error': round(link.intf1.params.get('error', 0), 2),
                        'max_queue_size': link.intf1.params.get('max_queue_size', 0),
                        'rate': round(link.intf1.params.get('rate', 0), 2),
                        'mtu': link.intf1.params.get('mtu', 0)
                    }
                    all_links_data.append(link_data)

                    # if all(param is not None for param in [bw1, bw2, delay1, delay2, loss1, loss2, jitter1, jitter2, error1, error2, queue_size1, queue_size2, rate1, rate2, mtu1, mtu2]):
                    #     print(f"链路 {link.intf1.node.name}<->{link.intf2.node.name} 更新后: "
                    #           f"带宽 {bw1:.2f} Mbps, 延迟 {delay1}, 丢包率 {loss1}%, 抖动 {jitter1}, 错误率 {error1}%, "
                    #           f"队列长度 {queue_size1}, MTU {mtu1}")

            try:
                response = requests.post('http://127.0.0.1:8001/receive_link_data/', json=all_links_data)
                if response.status_code != 200:
                    print("Failed to send link data")
                else:
                    print("Successful")
            except requests.exceptions.RequestException as e:
                print(f"Error sending link data: {e}")

            time.sleep(1)
        except Exception as e:
            print(f"Error in simulate_network_changes: {e}")
            time.sleep(1)
