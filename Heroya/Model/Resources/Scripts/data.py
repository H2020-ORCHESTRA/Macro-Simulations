from AAPI import *

setup_name = "e3"

#list elem: (destination, access_time, entrance_time, platooned)
trucks_to_spawn = []
truck_times_inside_park = []
truck_waiting_times = []
entry_times = []
exit_times = []
avg_time_inside_park = 0
avg_waiting_time = 0
waiting_time_95 = 0
tot_trucks_in = 0

depot_to_centroid = {
    1:  22439,  #7
    2:  22434,  #4
    3:  22444,  #9
    4:  22424,  #6
    5:  22429,  #8
}