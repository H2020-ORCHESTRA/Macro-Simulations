from AAPI import *

#list elem: (ped_time_to_spawn, destination_gate, status)
peds_to_spawn_parking = []

#list elem: (ped_time_to_spawn, destination_gate, status)
peds_to_spawn_trains = []

#list elem: (ped_time_to_spawn, destination_gate, status)
peds_to_spawn_bus_taxi = []

#dictionnary storing the timestamp when a passenger entered the simulation
# {passenger_id: start_time}
passenger_start_time = {}

#dictionnary storing the concrete speed of a passenger
# {passenger_id: [concrete_speed, ...]}
passenger_concrete_speed = {}

#dictionnary storing the distribution of passengers travel time inside the airport
# {travel_time: amount of passenger traveling for this time}
travel_time_distribution = {}

#dictionnary passengers travel time inside the airport
travel_time_per_passenger = {}

gate_to_red_centroid = {
    1:  27968,
    2:  28026,
    3:  28078,
    4:  28137,
    5:  28169,
    6:  28217,
    7:  28289,
    8:  29123,
    9:  28551,
    10: 28497,
    11: 28501,
    12: 28505,
    13: 28509,
    14: 28513,
    15: 28517,
    16: 28521,
    17: 28769,
    18: 28773,
    19: 28777,
    20: 28781,
    21: 28785,
    22: 28789,
    23: 28793,
    24: 28797}

remaining_gates = int((72-24)/2)

for i in range(24 + 1, 24 + 1 + remaining_gates, 1):
    gate_to_red_centroid[i] = 29894

for i in range(24 + 1 + remaining_gates, 24 + 1 + 2*remaining_gates, 1):
    gate_to_red_centroid[i] = 29897
