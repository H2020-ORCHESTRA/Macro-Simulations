# Script generating OD routes for pedestrians in malpensa airport.
# The generated routes are exported in a txt file in this same folder, and are formated as follows:
# green_centroid;red_centroid;route_name;route_percentage;[path_id;]

import itertools
import os
import csv
import random

X_RAY_KEY = "x_ray"
PASSPORT_CONTROL_KEY = "passport_control"
CHECK_IN_KEY = "check_in"
BAGGAGE_CLAIM_KEY = "baggage_claim"
BAGGAGE_DROP_KEY = "baggage_drop"

FILE_NAME = "routes.txt"


parking_passerelle_id =    [29433]
parking_green_centroids =  [16747]
parking_red_centroids =    [29416]
taxi_bus_green_centroids = [16749]
taxi_bus_red_centroids =   [29909]
trains_green_centroids =   [26886, 26890, 29145, 29147]
trains_red_centroids =     [26906, 29364, 29366, 26892]

#TODO: add fast check in centroids (and generate their routes)
parking_priority_green_centroid = [29921]
taxi_bus_priority_green_centroid = [29927]
trains_priority_green_centroid = [29925]

fast_check_in_ids = [(29902, 29903, 29899)]
USES_FAST_CHECK_IN = True

gates_green_centroids_up =        [27964, 28023, 28074, 28139, 28171, 28547, 28291, 29125]
gates_green_centroids_mid =       [28553, 28499, 28503, 28507, 28511, 28515, 28519, 28523]
gates_green_centroids_down =      [28771, 28775, 28779, 28783, 28787, 28791, 28795, 28799]
gates_green_centroids_remaining = [29896, 29898]

gates_red_centroids_up =        [27968, 28026, 28078, 28137, 28169, 28217, 28289, 29123]
gates_red_centroids_mid =       [28551, 28497, 28501, 28505, 28509, 28513, 28517, 28521]
gates_red_centroids_down =      [28769, 28773, 28777, 28781, 28785, 28789, 28793, 28797]
gates_red_centroids_remaining = [29894, 29897]

# (control_point_id, check_in_id, baggage_drop_id)
check_in_up_ids =   [(29071, 29067, 29870), (29076, 29072, 29882), (29081, 29078, 29883)]
check_in_mid_ids =  [(16807, 16787, 29885), (28334, 28330, 29886), (28339, 28337, 29887), (28345, 28341, 29888)]
check_in_down_ids = [(28366, 28365, 29889), (28359, 28348, 29890), (28351, 28356, 29892), (28367, 28360, 29893)]
x_ray_ids = [[29866,   29865,   29863], [29864 ,  29861 ,
              29862], [29859,   29860 ,  29507], [29508 ,
              29509 ,  29511], [29513 ,  29514 ,  29515],
             [29517 ,  29516 ,  29688], [29689 ,  29690]]

# (control_point_1_id, control_point_2_id, passport_control_id)
passport_control_ids = [(29409,29410,29058), (29467,29465,29472)]

return_back_passport_control_ids = [29913, 29912]

return_back_avoid_passport_control = [29530]
bagage_claim_up_ids = [29520, 29521, 29523, 29524, 29526]
bagage_claim_down_ids = [29573, 29574, 29576, 29578, 29579]

departure_routes = {
    1: ([X_RAY_KEY],27),
    2: ([X_RAY_KEY, PASSPORT_CONTROL_KEY],11),
    3: ([CHECK_IN_KEY, X_RAY_KEY],5),
    4: ([CHECK_IN_KEY, X_RAY_KEY, PASSPORT_CONTROL_KEY],2),
    5: ([BAGGAGE_DROP_KEY, X_RAY_KEY],33),
    6: ([BAGGAGE_DROP_KEY, X_RAY_KEY, PASSPORT_CONTROL_KEY],14),
    7: ([CHECK_IN_KEY, BAGGAGE_DROP_KEY, X_RAY_KEY],6),
    8: ([CHECK_IN_KEY, BAGGAGE_DROP_KEY, X_RAY_KEY, PASSPORT_CONTROL_KEY],2)
}

arrival_routes = {
    1: ([BAGGAGE_CLAIM_KEY],38.5),
    2: ([PASSPORT_CONTROL_KEY, BAGGAGE_CLAIM_KEY],16.5),
    3: ([],31.5),
    4: ([PASSPORT_CONTROL_KEY],13.5)
}

def get_check_in_list_by_red_centroid(red_centroid_id):
    if red_centroid_id in gates_red_centroids_up:
        return check_in_up_ids
    if red_centroid_id in gates_red_centroids_mid:
        return check_in_mid_ids
    if red_centroid_id in gates_red_centroids_down:
        return check_in_down_ids
    if red_centroid_id in gates_red_centroids_remaining:
        return check_in_mid_ids
    
def get_baggage_claim_list_by_green_centroid(green_centroid_id):
    if green_centroid_id in gates_green_centroids_up:
        return bagage_claim_up_ids
    if green_centroid_id in gates_green_centroids_mid:
        return bagage_claim_up_ids + bagage_claim_down_ids
    if green_centroid_id in gates_green_centroids_down:
        return bagage_claim_down_ids
    if green_centroid_id in gates_green_centroids_remaining:
        return bagage_claim_up_ids + bagage_claim_down_ids

lines_to_export = []
for green_centroid in trains_green_centroids + parking_green_centroids + taxi_bus_green_centroids:
    for red_centroid in gates_red_centroids_up + gates_red_centroids_mid + gates_red_centroids_down + gates_red_centroids_remaining:
        for route, percentage in departure_routes.values():
            # print(f"{green_centroid} - {red_centroid}: {route}, {percentage}")
            route_name = '_'.join(route)

            if route_name == "":
                route_name = "no_service_point_route"

            base_line_to_export = [green_centroid, red_centroid]
            path_lists = []

            if green_centroid in parking_green_centroids:
                path_lists.append(parking_passerelle_id)

            for cp_index, control_point in enumerate(route):
                # print(f"{cp_index}, {control_point}")
                if control_point == CHECK_IN_KEY:
                    check_in_ids = get_check_in_list_by_red_centroid(red_centroid)
                    if len(route) > cp_index+1 and route[cp_index+1] == BAGGAGE_DROP_KEY:
                        path_lists.append(check_in_ids)
                    else:
                        path_lists.append([(check_in_id[0], check_in_id[1]) for check_in_id in check_in_ids])

                if control_point == X_RAY_KEY:
                    path_lists.append(random.choice(x_ray_ids))

                if control_point == PASSPORT_CONTROL_KEY:
                    if red_centroid in gates_red_centroids_up:
                        path_lists.append(passport_control_ids)

                if control_point == BAGGAGE_DROP_KEY:
                    if cp_index != 0 and route[cp_index-1] == CHECK_IN_KEY:
                        continue
                    else:
                        path_lists.append([check_in_id[2] for check_in_id in check_in_ids])

            if PASSPORT_CONTROL_KEY not in route and red_centroid in gates_red_centroids_up:
                path_lists.append(return_back_avoid_passport_control)

            paths = list(itertools.product(*path_lists))
            paths = [[list(j) if type(j) is tuple else [j] for j in list(e)] for e in paths]
            # print(paths)
            pondered_perc = percentage/len(paths)
            for path in paths:
                line_to_export = base_line_to_export.copy()
                line_to_export.append(route_name)
                line_to_export.append(pondered_perc)
                for i in list(itertools.chain(*path)):
                    line_to_export.append(i)
                
                lines_to_export.append(line_to_export)

for fast_green_centroid in parking_priority_green_centroid + trains_priority_green_centroid + taxi_bus_priority_green_centroid:
    for red_centroid in gates_red_centroids_up + gates_red_centroids_mid + gates_red_centroids_down + gates_red_centroids_remaining:
        for route, percentage in departure_routes.values():
            # print(f"{green_centroid} - {red_centroid}: {route}, {percentage}")
            route_name = '_'.join(route)

            if route_name == "":
                route_name = "no_service_point_route"

            route_name = "fast_"+route_name

            base_line_to_export = [fast_green_centroid, red_centroid]
            path_lists = []

            if fast_green_centroid in parking_priority_green_centroid:
                path_lists.append(parking_passerelle_id)

            for cp_index, control_point in enumerate(route):
                # print(f"{cp_index}, {control_point}")
                if control_point == CHECK_IN_KEY:
                    check_in_ids = None
                    if USES_FAST_CHECK_IN:
                        check_in_ids = fast_check_in_ids
                    else:
                        check_in_ids = get_check_in_list_by_red_centroid(red_centroid)
                    if len(route) > cp_index+1 and route[cp_index+1] == BAGGAGE_DROP_KEY:
                        path_lists.append(check_in_ids)
                    else:
                        path_lists.append([(check_in_id[0], check_in_id[1]) for check_in_id in check_in_ids])

                if control_point == X_RAY_KEY:
                    path_lists.append(random.choice(x_ray_ids))

                if control_point == PASSPORT_CONTROL_KEY:
                    if red_centroid in gates_red_centroids_up:
                        path_lists.append(passport_control_ids)

                if control_point == BAGGAGE_DROP_KEY:
                    if cp_index != 0 and route[cp_index-1] == CHECK_IN_KEY:
                        continue
                    else:
                        path_lists.append([check_in_id[2] for check_in_id in check_in_ids])

            if PASSPORT_CONTROL_KEY not in route and red_centroid in gates_red_centroids_up:
                path_lists.append(return_back_avoid_passport_control)

            paths = list(itertools.product(*path_lists))
            paths = [[list(j) if type(j) is tuple else [j] for j in list(e)] for e in paths]
            # print(paths)
            pondered_perc = percentage/len(paths)
            for path in paths:
                line_to_export = base_line_to_export.copy()
                line_to_export.append(route_name)
                line_to_export.append(pondered_perc)
                for i in list(itertools.chain(*path)):
                    line_to_export.append(i)
                
                lines_to_export.append(line_to_export)


for green_centroid in gates_green_centroids_up + gates_green_centroids_mid + gates_green_centroids_down + gates_green_centroids_remaining:
    for red_centroid in parking_red_centroids + trains_red_centroids + taxi_bus_red_centroids:
        for route, percentage in arrival_routes.values():
            # print(f"{green_centroid} - {red_centroid}: {route}, {percentage}")
            route_name = '_'.join(route)

            if route_name == "":
                route_name = "no_service_point_route"

            base_line_to_export = [green_centroid, red_centroid]
            path_lists = []
            if PASSPORT_CONTROL_KEY not in route and green_centroid in gates_green_centroids_up:
                path_lists.append(return_back_avoid_passport_control)
            for control_point in route:
                # print(f"{cp_index}, {control_point}")
                if control_point == BAGGAGE_CLAIM_KEY:
                    # bagage_claim_ids = get_baggage_claim_list_by_green_centroid(green_centroid)
                    bagage_claim_ids = get_baggage_claim_list_by_green_centroid(green_centroid)
                    path_lists.append(bagage_claim_ids)

                if control_point == PASSPORT_CONTROL_KEY and green_centroid in gates_green_centroids_up:
                    path_lists.append(return_back_passport_control_ids)
                    
                if control_point == None:
                    pass

            # print(path_lists)
            paths = list(itertools.product(*path_lists))
            paths = [[list(j) if type(j) is tuple else [j] for j in list(e)] for e in paths]
            # print(paths)
            pondered_perc = percentage/len(paths)
            for path in paths:
                line_to_export = base_line_to_export.copy()
                line_to_export.append(route_name)
                line_to_export.append(pondered_perc)
                for i in list(itertools.chain(*path)):
                    line_to_export.append(i)
                # print(line_to_export)
                lines_to_export.append(line_to_export)

file_path = os.path.join(os.getcwd(), FILE_NAME)
with open(file_path, "w", newline="") as f:
    wr = csv.writer(f, delimiter=";")
    wr.writerows(lines_to_export)
