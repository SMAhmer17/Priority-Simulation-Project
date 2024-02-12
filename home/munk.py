import numpy as np
from scipy.stats import *
import pandas as pd
import random as rand
import math
import heapq

def munk(arrival_rate, service_rate):      # Generating random number 
    A = 55
    M = 1994
    Zo = 10112166
    C = 9

    prioritie = []

    for i in range(20):
        LCG = ((A * Zo) + C) % M
        X = LCG / M
        Yo = ((3 - 1) * X) + 1
        dec = Yo - int(Yo)
        decf = int(dec * 10)

        if 0 <= decf <= 4:
            result = math.floor(Yo)
        elif 5 <= decf <= 9:
            result = math.ceil(Yo)
        else:
            result = "not"

        prioritie.append(result)
        Zo = LCG

    rand = None
    if rand is None:
        values = []
        i = 0
        while True:
            val = poisson.cdf(k=i, mu=arrival_rate)
            values.append(val)
            if val == 1:
                i += 1
                break
            i += 1
        rand = len(values)

    inter_arrival = [0]
    inter_arvl = np.round(np.random.poisson(arrival_rate, size=rand - 1), 2) # Generating random posson arrival time
    inter_arvl = np.abs(inter_arvl)
    for element in inter_arvl:
        inter_arrival.append(element)

    arrivali = [round(sum(inter_arrival[:i + 1]), 2) for i in range(20)]
    
    service = np.round(np.random.exponential(scale=1 / service_rate, size=20), 2)# Generating random exp Service time
    servicei = np.abs(service)
    

    st = []
    en = []

    class Process:                                       # Generting Start & End time
        def __init__(self, name, arrival_time, service_time, priority):
            self.name = name
            self.arrival_time = arrival_time
            self.service_time = service_time
            self.priority = priority

        def __lt__(self, other):
            return self.priority < other.priority

    def schedule_processes(processes):
        MIN_SERVICE_TIME = 0.001
        current_time = 0
        result = {}
        priority_queue = []

        while processes or priority_queue:
            while processes and processes[0].arrival_time <= current_time:
                process = processes.pop(0)
                heapq.heappush(priority_queue, process)

            if not priority_queue:
                current_time = processes[0].arrival_time
                continue

            current_process = heapq.heappop(priority_queue)
            start_time = current_time

            if current_process.service_time < MIN_SERVICE_TIME:
                end_time = current_time + current_process.service_time
                current_process.service_time = 0
            else:
                end_time = min(current_time + current_process.service_time,
                               processes[0].arrival_time if processes else float('inf'))

            if current_process.name not in result:
                result[current_process.name] = (start_time, end_time)
            else:
                result[current_process.name] = (result[current_process.name][0], end_time)

            current_time = end_time

            if current_process.service_time > (end_time - start_time):
                current_process.service_time -= (end_time - start_time)
                heapq.heappush(priority_queue, current_process)

        return result

    num_processes = len(prioritie)
    processes = []

    names = [f"p{i + 1}" for i in range(num_processes)]
    arrival_times = arrivali
    service_times = servicei
    priorities = prioritie
    
    for i in range(num_processes):
        name = names[i]
        arrival_time = arrival_times[i]
        service_time = service_times[i]
        priority = priorities[i]
        processes.append(Process(name, arrival_time, service_time, priority))

    schedule = schedule_processes(processes)

    sorted_process_names = sorted(schedule.keys(), key=lambda name: int(name[1:]))

    end_times_dict = {}

    for p in sorted_process_names:
        start, end = schedule[p]
        st.append(round(start, 3))
        en.append(round(end, 3))
        end_times_dict[p] = round(end, 3)

    en = [end_times_dict[name] for name in names]
    print(len(en))
    turnaround_times = np.round(np.abs(np.array(en) - np.array(arrivali)), 3)
    waiting_times = np.round(np.abs(np.array(en) - np.array(arrivali) - np.array(servicei)), 3)
    response_times = np.round(np.abs(np.array(st) - np.array(arrivali)), 3)

    return {
        "Arrival Times": arrivali,
        "Service Times": servicei,
        "Start Times": st,
        "End Times": en,
        "Priority": prioritie,
        "Turnaround Times": turnaround_times,
        "Waiting Times": waiting_times,
        "Response Times": response_times
    }


