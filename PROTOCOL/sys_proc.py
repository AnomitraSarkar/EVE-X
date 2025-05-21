import psutil
import time
import os
import threading

processes_info = []

def fetch_process_info(proc):
    try:
        cpu = proc.cpu_percent(interval=None)
        mem = proc.memory_info().rss  # Memory in bytes
        info = {
            'pid': proc.pid,
            'name': proc.name(),
            'cpu': cpu,
            'memory': mem
        }
        processes_info.append(info)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

def get_all_processes_info():
    global processes_info
    processes_info = []
    threads = []
    
    for proc in psutil.process_iter():
        t = threading.Thread(target=fetch_process_info, args=(proc,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def print_sorted_processes():
    get_all_processes_info()

    processes_by_cpu = sorted(processes_info, key=lambda p: p['cpu'], reverse=True)
    processes_by_memory = sorted(processes_info, key=lambda p: p['memory'], reverse=True)

    print("\nTop Processes by CPU Usage:")
    print("{:<8} {:<25} {:>10}%".format("PID", "Name", "CPU"))
    for p in processes_by_cpu[:10]:
        print("{:<8} {:<25} {:>10.1f}".format(p['pid'], p['name'][:24], p['cpu']))

    print("\nTop Processes by Memory Usage:")
    print("{:<8} {:<25} {:>10}".format("PID", "Name", "Memory (MB)"))
    for p in processes_by_memory[:10]:
        print("{:<8} {:<25} {:>10.2f}".format(p['pid'], p['name'][:24], p['memory'] / (1024 * 1024)))

if __name__ == "__main__":
    # Prime the CPU usage counters
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_sorted_processes()
        time.sleep(2)
