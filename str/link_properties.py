import random

def random_value_in_range(min_val, max_val):
    if isinstance(min_val, float) or isinstance(max_val, float):
        return random.uniform(min_val, max_val)
    else:
        return random.randint(min_val, max_val)

def set_link_properties(link, bandwidth_range, delay_range, loss_range=(0, 5), jitter_range=(0, 10), error_range=(0, 1), max_queue_size_range=(100, 1000), rate_range=(10, 1000), mtu_range=(1500, 9000), r2q=3, quantum=12000):
    min_bandwidth, max_bandwidth = bandwidth_range
    min_delay, max_delay = delay_range
    min_loss, max_loss = loss_range
    min_jitter, max_jitter = jitter_range
    min_error, max_error = error_range
    min_max_queue_size, max_max_queue_size = max_queue_size_range
    min_rate, max_rate = rate_range
    min_mtu, max_mtu = mtu_range

    bandwidth = random.uniform(min_bandwidth, max_bandwidth)
    delay = f"{random.uniform(min_delay, max_delay)}ms"
    loss = random_value_in_range(min_loss, max_loss)
    jitter = f"{random_value_in_range(min_jitter, max_jitter)}ms"
    error = random_value_in_range(min_error, max_error)
    max_queue_size = random_value_in_range(min_max_queue_size, max_max_queue_size)
    rate = random_value_in_range(min_rate, max_rate)
    mtu = random_value_in_range(min_mtu, max_mtu)

    link.intf1.params['bw'] = bandwidth
    link.intf1.params['delay'] = delay
    link.intf1.params['loss'] = loss
    link.intf1.params['jitter'] = jitter
    link.intf1.params['error'] = error
    link.intf1.params['max_queue_size'] = max_queue_size
    link.intf1.params['rate'] = rate
    link.intf1.params['mtu'] = mtu

    link.intf2.params['bw'] = bandwidth
    link.intf2.params['delay'] = delay
    link.intf2.params['loss'] = loss
    link.intf2.params['jitter'] = jitter
    link.intf2.params['error'] = error
    link.intf2.params['max_queue_size'] = max_queue_size
    link.intf2.params['rate'] = rate
    link.intf2.params['mtu'] = mtu

    link.intf1.config(r2q=5, quantum=30000)
    link.intf2.config(r2q=5, quantum=30000)
