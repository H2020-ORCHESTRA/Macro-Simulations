"""Help functions."""

from AAPI import *
import typing
import csv
import data
import math
import os


def time_sta_from_sec(seconds: int) -> float:
    """Calculate the time of simulation in stationary period based on seconds.

    :example:

    In :py:`AAPIManage()` and :py:`AAPIPostManage()`:

    .. code-block:: python

        if timeSta == time_sta_from_sec(5):
            pass

    :param int seconds: Number of seconds
    :return: Time of simulation in stationary period based on simulation step
    :rtype: float
    """
    return AKIGetIniSimTime() + (seconds * AKIGetSimulationStepTime())


def time_from_sec(seconds: int) -> float:
    """Calculate the time of simulation based on seconds.

    :example:

    In :py:`AAPIManage()` and :py:`AAPIPostManage()`:

    .. code-block:: python

        if time == time_from_sec(5):
            pass

    :param int seconds: Number of seconds
    :return: Time of simulation based on simulation step
    :rtype: float
    """
    return seconds * AKIGetSimulationStepTime()


def print(s: str):
    """Print a string.

    :param str s: String to print
    """
    AKIPrintString(s)


def prints(ls: typing.List[str]):
    """Print a string.

    :param ls: List of strings to print
    :type ls: list[str]
    """
    for s in ls:
        AKIPrintString(s)


def load_csv_file(csv_file_path = f"C:/tmp/{data.setup_name}.csv"):
    # AGENT_ID = 1
    DST_ROW = 2
    CAV_ROW = 3
    ACC_TIME_ROW = 4
    ENTRY_ROW = 8

    init_sim_time = (AKIGetIniSimTime()/60)
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file, delimiter=",")
        for e, row in enumerate(reader):
            if e == 0:
                continue

            time = row[ENTRY_ROW].split(' ')[1]
            h, m, s = map(int, time.split(':'))
            row[ENTRY_ROW] = h*60 + m - init_sim_time

            data.trucks_to_spawn.append([data.depot_to_centroid[int(row[DST_ROW])], int(row[ACC_TIME_ROW])*60, row[ENTRY_ROW], row[CAV_ROW]])
    
    data.trucks_to_spawn = sorted(data.trucks_to_spawn, key=lambda x: x[2])
    print(f"Number of trucks to spawn: {len(data.trucks_to_spawn)}")


def calculate_kpis():
    data.avg_time_inside_park = sum(data.truck_times_inside_park)/len(data.truck_times_inside_park)
    data.avg_waiting_time = sum(data.truck_waiting_times)/len(data.truck_waiting_times)
    truck_waiting_sorted = sorted(data.truck_waiting_times) # Sort in ascending order
    index = math.ceil(95 / 100 * len(truck_waiting_sorted))
    data.waiting_time_95 = truck_waiting_sorted[index]


def save_kpis():
    cwd = os.getcwd()
    print(f"Working dir: {cwd}")
    # f = open("./kpi.txt", "w")
    # f.write(f"Total trucks: {data.tot_trucks_in}\n")
    # f.write(f"Entry times: {data.entry_times}\n")
    # f.write(f"Exit times: {data.exit_times}\n")
    # f.write(f"Time spent inside park: {data.truck_times_inside_park}\n")
    # f.write(f"Average time inside park: {data.avg_time_inside_park}\n")
    # f.write(f"Truck waiting times: {data.truck_waiting_times}\n")
    # f.write(f"Average waiting time: {data.avg_waiting_time}\n")
    # f.write(f"95th percentile waiting time: {data.waiting_time_95}\n")
    # f.close()

    with open(f"kpi/{data.setup_name}.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Total trucks:"] + [data.tot_trucks_in])
        csvwriter.writerow(["Entry times:"] + data.entry_times)
        csvwriter.writerow(["Exit times:"] + data.exit_times)
        csvwriter.writerow(["Time spent inside park:"] + data.truck_times_inside_park)
        csvwriter.writerow(["Average time inside park:"] + [data.avg_time_inside_park])
        csvwriter.writerow(["Truck waiting times:"] + data.truck_waiting_times)
        csvwriter.writerow(["Average waiting time:"] + [data.avg_waiting_time])
        csvwriter.writerow(["95th percentile waiting time:"] + [data.waiting_time_95])