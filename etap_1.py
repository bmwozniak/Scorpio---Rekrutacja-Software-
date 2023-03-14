import psutil
import netifaces
import time

# funkcja do odczytywania informacji o interfejsach sieciowych
def get_network_data():
    network_data = []
    for interface in netifaces.interfaces():
        interface_data = {}
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            interface_data['ip_address'] = addrs[netifaces.AF_INET][0]['addr']
        else:
            interface_data['ip_address'] = 'N/A'
        stats = netifaces.if_stats(interface)
        interface_data['status'] = 'UP' if stats.isup else 'DOWN' if stats.isup == False else 'UNKNOWN'
        interface_data['bytes_sent'] = stats.bytes_sent
        interface_data['bytes_recv'] = stats.bytes_recv
        network_data.append(interface_data)
    return network_data

# funkcja do odczytywania informacji o procesorze
def get_cpu_data():
    cpu_data = {}
    cpu_data['load'] = psutil.cpu_percent(percpu=True)
    cpu_data['temp'] = psutil.sensors_temperatures()['coretemp'][0].current
    return cpu_data

# funkcja do odczytywania informacji o pamięci
def get_memory_data():
    memory_data = {}
    memory = psutil.virtual_memory()
    memory_data['total'] = memory.total
    memory_data['available'] = memory.available
    memory_data['used'] = memory.used
    return memory_data

# funkcja do odczytywania informacji o dysku
def get_disk_data():
    disk_data = {}
    disk = psutil.disk_usage('/')
    disk_data['free'] = disk.free
    return disk_data

# zapisanie danych do pliku tekstowego
def save_data_to_file(data):
    with open('~/system_data_readings.txt', 'w') as f:
        for key in data:
            f.write(key + '\n')
            f.write(str(data[key]) + '\n')

# odczyt i zapis danych co 60 sekund
while True:
    data = {}
    data['network'] = get_network_data()
    data['cpu'] = get_cpu_data()
    data['memory'] = get_memory_data()
    data['disk'] = get_disk_data()
    save_data_to_file(data)
    time.sleep(60)
