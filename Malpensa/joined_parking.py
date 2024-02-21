from lib.parking import Parking, ParkingGroup
from lib.train_pedestrian import TrainStop, TrainStopGroup
from lib.taxi_pedestrian import TaxiBusStopGroup
from lib.kpis import *
import lib.attributes_lib as attr
import lib.simdata as data
import csv

from AAPI import *

pedestrians_to_track = []
pedestrians_to_track_2 = []
pedestrians_to_track_3 = []

EXCEL_FILE_PATH = "C://tmp//agents_1_600.csv"
GATE_COL = 2
PLANE_COL = 3
PED_SPAWN_TIME_COL = 4
STATUS_COL = 5
VEHICLE_COL = 6

MAX_PASSENGER_SPEED = 1.6

TRAIN_TIME_OFFSET = 0
GLOBAL_OFFSET = 0 #240

def AAPILoad():
    return 0

def add_parking_pedestrian(row):
    data.peds_to_spawn_parking.append((row[PED_SPAWN_TIME_COL] - GLOBAL_OFFSET,data.gate_to_red_centroid[int(row[GATE_COL])], row[STATUS_COL]))

def add_train_pedestrian(row):
    data.peds_to_spawn_trains.append((row[PED_SPAWN_TIME_COL] - TRAIN_TIME_OFFSET - GLOBAL_OFFSET,data.gate_to_red_centroid[int(row[GATE_COL])], row[STATUS_COL]))

def add_bus_taxi_pedestrian(row):
    data.peds_to_spawn_bus_taxi.append((row[PED_SPAWN_TIME_COL] - GLOBAL_OFFSET,data.gate_to_red_centroid[int(row[GATE_COL])], row[STATUS_COL]))

def sort_pedestrian_data_lists_by_spawn_time():
    data.peds_to_spawn_parking = sorted(data.peds_to_spawn_parking, key=lambda x: x[0])
    data.peds_to_spawn_trains = sorted(data.peds_to_spawn_trains, key=lambda x: x[0])
    data.peds_to_spawn_bus_taxi = sorted(data.peds_to_spawn_bus_taxi, key=lambda x: x[0])

def load_csv_file():
    print(f"CSV file has to be located at: C://tmp//agents_1_600.csv")
    init_sim_time = (AKIGetIniSimTime()/60)
    with open(EXCEL_FILE_PATH, 'r') as file:
        reader = csv.reader(file, delimiter=";")
        for e,row in enumerate(reader):
            if e == 0:
                continue
            shift = -2
            row[3] = sum(map(int,[row[3], -init_sim_time, shift]))
            row[4] = sum(map(int,[row[4], -init_sim_time, shift]))
            if "CAR" in row[VEHICLE_COL]:
                add_parking_pedestrian(row)
            elif "TAXI" in row[VEHICLE_COL] or "COACH" in row[VEHICLE_COL] or "E" in row[VEHICLE_COL]:
                add_bus_taxi_pedestrian(row)
            else:
                add_train_pedestrian(row)

    sort_pedestrian_data_lists_by_spawn_time()
    



def AAPIInit():
    # --------------------------------------------------------------------
    global parkingGroup
    global trainstops
    global taxibusstops
    global kpiList

    load_csv_file()

    trainstops = TrainStopGroup()
    taxibusstops = TaxiBusStopGroup()

    ped_kpis_list = []
    ped_kpi_dict = {}
    for cur_dict in [check_in_coords, x_ray_coords, passport_check_coords, gates_coords]:
        ped_kpi_dict.update(cur_dict)

    for index, coords in ped_kpi_dict.items():
        ped_kpi = AreaPedRateKPI(index, coords, 60)
        ped_kpis_list.append(ped_kpi)

    
    #TODO: create alarm list (and others) and append them for the global kpiList
    alarm_kpis_list = []
    alarm_kpis_list.append(AreaPedAlarmKPI("check_in_1_alarm",check_in_coords['checkin_1'], 60, 0.3))

    kpiList = KPIList(ped_kpis_list+alarm_kpis_list)

    # init parameters for ALL parkings ...................................
    totIn = 0
    totOut = 0

    # Parking N ..........................................................

    # centroid id of parking
    parkingId = 27790
    inSectionId = 27613
    outSectionId = 27614

    # IDs of labels
    occId = 27860
    maxId = 27864
    inId = 27861
    outId = 27859

    maxCapacity = 1200
    occupancy = 600

    parkingN = Parking(
            title="parking 1", #parking N
            parkingId=parkingId,
            inSectionId=inSectionId,
            outSectionId=outSectionId,
            occId=occId,
            maxId=maxId,
            inId=inId,
            outId=outId,
            maxCapacity=maxCapacity,
            totIn=totIn,
            totOut=totOut,
            occupancy=occupancy
            )

    # Parking Center #1 ..................................................

    # centroid id of parking
    parkingId = 27912
    inSectionId = 27458
    outSectionId = 27489

    # IDs of labels
    occId = 27812
    maxId = 27809
    inId = 27810
    outId = 27808

    maxCapacity = 2700
    occupancy = 1300

    parkingC1 = Parking(
            title="parking 2", # parking Center #1
            parkingId=parkingId,
            inSectionId=inSectionId,
            outSectionId=outSectionId,
            occId=occId,
            maxId=maxId,
            inId=inId,
            outId=outId,
            maxCapacity=maxCapacity,
            totIn=totIn,
            totOut=totOut,
            occupancy=occupancy
            )

    # Parking Center #2 ..................................................

    # centroid id of parking
    parkingId = 27913
    inSectionId = 27510
    outSectionId = 27507

    # IDs of labels
    occId = 27819
    maxId = 27816
    inId = 27817
    outId = 27815

    maxCapacity = 1600
    occupancy = 800

    parkingC2 = Parking(
            title="parking 3", # parking Center #2
            parkingId=parkingId,
            inSectionId=inSectionId,
            outSectionId=outSectionId,
            occId=occId,
            maxId=maxId,
            inId=inId,
            outId=outId,
            maxCapacity=maxCapacity,
            totIn=totIn,
            totOut=totOut,
            occupancy=occupancy
            )

    # Parking S ..........................................................

    # centroid id of parking
    parkingId = 27918
    inSectionId = 27608
    outSectionId = 27609

    # IDs of labels
    occId = 27826
    maxId = 27823
    inId = 27824
    outId = 27822

    maxCapacity = 1200
    occupancy = 600

    parkingS = Parking(
            title="parking 4", # parking S
            parkingId=parkingId,
            inSectionId=inSectionId,
            outSectionId=outSectionId,
            occId=occId,
            maxId=maxId,
            inId=inId,
            outId=outId,
            maxCapacity=maxCapacity,
            totIn=totIn,
            totOut=totOut,
            occupancy=occupancy
            )

    parkingGroup = ParkingGroup([parkingN, parkingC1, parkingC2, parkingS])

    return 0


def AAPISimulationReady():
    return 0

test_pedestrian_box = {
    "x_left":  477718.8145, 
    "x_right": 477736.4374, 
    "y_bottom": 5053093.7676,
    "y_top":    5053104.9868
}

test_pedestrian_box_2 = {
    "x_left":  477726.1, 
    "x_right": 477733.0, 
    "y_bottom": 5053091.1,
    "y_top":    5053105.1
}

waiting_times = {}

speed_sampling_counter = 0
speed_sampling_max_counter = 60

def AAPIManage(time, timeSta, timeTrans, acycle):
    global parkingGroup
    global taxibusstops
    global kpiList
    global speed_sampling_counter, speed_sampling_max_counter

    kpiList.api_manage(AKIGetSimulationStepTime())

    ped_kpis = kpiList.get_ped_kpis()
    for ped in pedestrians_to_track:
        speed_sampling_counter += 1
        if speed_sampling_counter >= speed_sampling_max_counter:
            speed_sampling_counter = 0  # reset counter
            if ped not in data.passenger_concrete_speed.keys():
                data.passenger_concrete_speed[ped] = []
            data.passenger_concrete_speed[ped].append((AKIPedestrianGetStaticInf(ped).preferredWalkSpeed-AKIPedestrianGetInf(ped).speed)/AKIPedestrianGetStaticInf(ped).preferredWalkSpeed)
        for ped_kpi in ped_kpis:
            ped_kpi.sample(ped)

    ##################### TEST CODE
    """
    for pedestrian in pedestrians_to_track:
        pedestrian_pos = AKIPedestrianGetInf(pedestrian).position
        if is_pos_in_box(pedestrian_pos, test_pedestrian_box):
            if pedestrian not in waiting_times.keys():
                waiting_times[pedestrian] = 0
            waiting_times[pedestrian] += AKIGetSimulationStepTime()
            print(f"Pedestrian {pedestrian} detected! He waited for {waiting_times[pedestrian]} seconds")
    """

    for pedestrian in pedestrians_to_track_2:
        pedestrian_speed = AKIPedestrianGetInf(pedestrian).speed
        pedestrian_prefered_speed = AKIPedestrianGetStaticInf(pedestrian).preferredWalkSpeed
        if pedestrian_speed < 0.001:
            pedestrian_speed = 0
        print(f"speed : {pedestrian_speed}/{pedestrian_prefered_speed}")
        
        
    current_sim_time = AKIGetCurrentSimulationTime()
    for pedestrian in pedestrians_to_wait:
        pedestrian_pos = AKIPedestrianGetInf(pedestrian).position
        pedestrian_static_infs = AKIPedestrianGetStaticInf(pedestrian)
        if pedestrian_static_infs.destinationID in gates_pedestrian_centroids_out:
            cur_timetable = timetable_per_gate[pedestrian_static_infs.destinationID]
            if is_pos_in_box(pedestrian_pos, cur_timetable['pedestrian_box']) and \
                                            is_current_time_in_interval(current_sim_time, cur_timetable['offset'] * 60, cur_timetable['wait_duration'] * 60, TOTAL_DURATION * 60, cur_timetable['driving_offset'] * 60):
                pedestrian_static_infs.preferredWalkSpeed = 0
            else:
                pedestrian_static_infs.preferredWalkSpeed = 1.6
            
            AKIPedestrianSetStaticInf(pedestrian_static_infs)
        
        else:
            pedestrians_to_wait.remove(pedestrian)
        

    ##################### TEST CODE

    parkingGroup.sim_step_manage()
    taxibusstops.sim_step_manage()
    trainstops.sim_step_manage()
    return 0


def AAPIPostManage(time, timeSta, timeTrans, acycle):
    global parkingGroup

    parkingGroup.sim_step_post_manage()
    return 0


def AAPIFinish():
    global parkingGroup
    global kpiList
    parkingGroup.post_data_for_each_parking()
    
    ped_kpis: List[PedestrianKPI] = kpiList.get_ped_kpis()
    for ped_kpi in ped_kpis:
        with open(f'c://tmp//KPIs//{ped_kpi.get_name()}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for k,v in ped_kpi.sample_per_timestamp.items():
                writer.writerow([k,v])

    sorted_travel_times = sorted(list(data.travel_time_distribution.items()), key=lambda x: x[0])
    total_passengers = sum([x[1] for x in sorted_travel_times])
    mean_travel_time = sum(x[0]*x[1] for x in sorted_travel_times)/total_passengers
    potential_waiting_time = 0
    cur_sum_val = 0

    for pax_per_travel_time in sorted_travel_times:
        cur_sum_val += pax_per_travel_time[1]
        if cur_sum_val > 0.95*total_passengers:
            potential_waiting_time = pax_per_travel_time[0] - mean_travel_time
            with open("C://tmp//KPIs//potential_waiting_time.txt", "w") as potential_waiting_time_file:
                potential_waiting_time_file.write(f"{round(potential_waiting_time*100)/100} minutes of potential waiting time\n")
            break

    waiting_times = []
    for ped, wait_time in data.travel_time_per_passenger.items():
        mean_concrete_speed = sum(data.passenger_concrete_speed[ped])/len(data.passenger_concrete_speed[ped])
        diff_max_speed_concrete_speed = mean_concrete_speed
        waiting_times.append(wait_time*diff_max_speed_concrete_speed)

    mean_waiting_time = sum(waiting_times)/len(waiting_times)
    with open("C://tmp//KPIs//mean_waiting_time.txt", "w") as mean_waiting_time_file:
        mean_waiting_time_file.write(f"{round(mean_waiting_time*100)/100} minutes of mean waiting time\n")


    with open(f'c://tmp//KPIs//travel_time_distribution.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for k,v in sorted_travel_times:
            writer.writerow([k,v])

    #TODO: sorted travel times -> get mean travel time, then 95 percentile, and compute difference between 95 percentile and mean.

    print("KPIs measures saved at 'C:/tmp/KPIs/*'")
    return 0


def AAPIUnLoad():
    return 0


def AAPIPreRouteChoiceCalculation(time, timeSta):
    return 0


def AAPIEnterVehicle(idveh: int, idsection: int):
    global parkingGroup

    parkingGroup.api_enter_vehicle(idsection=idsection, idveh=idveh)
    return 0


def AAPIExitVehicle(idveh: int, idsection: int):
    global parkingGroup

    parkingGroup.api_exit_vehicle(idsection=idsection, idveh=idveh)
    return 0



test_in_centroid = 16749
test_in_centroid_2 = 27398
test_out_centroid_2 = 27399


parkings_pedestrian_centroid_in = 16747
parkings_pedestrian_fast_check_in_green_centroid = 29921

gates_pedestrian_centroids_in = [27964, 28023, 28074, 28139, 28171, 28547, 28291, 29125,
                                 28553, 28499, 28503, 28507, 28511, 28515, 28519, 28523,
                                 28771, 28775, 28779, 28783, 28787, 28791, 28795, 28799]

gates_pedestrian_centroids_out = [27968, 28026, 28078, 28137, 28169, 28217, 28289, 29123,
                                  28551, 28497, 28501, 28505, 28509, 28513, 28517, 28521,
                                  28769, 28773, 28777, 28781, 28785, 28789, 28793, 28797]



pedestrians_to_wait = []

def AAPIEnterPedestrian(idPedestrian, originCentroid):
    global parkingGroup
    global trainstops
    global taxibusstops
    static_infs = AKIPedestrianGetStaticInf(idPedestrian)

    #pedestrians_to_wait.append(idPedestrian)
    attr.track(idPedestrian)

    """
    if static_infs.destinationID in gates_pedestrian_centroids_out:
        pedestrians_to_wait.append(idPedestrian)
        attr.track(idPedestrian)
    """

    if originCentroid in [parkings_pedestrian_centroid_in, parkings_pedestrian_fast_check_in_green_centroid]:
        attr.track(idPedestrian)
        parkingGroup.api_enter_pedestrian(idPedestrian)

    elif originCentroid in trainstops.trainstopsid + [trainstops.fast_check_in_stopid]:
        attr.track(idPedestrian)
        trainstops.api_enter_pedestrian(idPedestrian)

    elif originCentroid in [taxibusstops.taxi_bus_green_centroid, taxibusstops.taxi_bus_fast_check_in_green_centroid]:
        attr.track(idPedestrian)
        taxibusstops.api_enter_pedestrian(idPedestrian)

    else:
        print(f"allowed ped: {originCentroid}")

    if originCentroid in gates_pedestrian_centroids_in:
        pass
        #attr.track(idPedestrian)
        #attr.set_as_authorized(idPedestrian)
    #if originCentroid == test_in_centroid:
    pedestrians_to_track.append(idPedestrian)
    #if originCentroid == test_in_centroid_2:
    #    pedestrians_to_track_2.append(idPedestrian)
    return 0

parkings_pedestrian_centroid_out = 29416

def AAPIExitPedestrian(idPedestrian, destinationCentroid):
    global parkingGroup
    attr.untrack(idPedestrian)
    static_infs = AKIPedestrianGetStaticInf(idPedestrian)
    if idPedestrian in data.passenger_start_time.keys():
        travel_time = round((AKIGetCurrentSimulationTime() - data.passenger_start_time[idPedestrian])/60)
        data.travel_time_per_passenger[idPedestrian] = travel_time
        data.passenger_start_time.pop(idPedestrian)
        if travel_time in data.travel_time_distribution.keys():
            data.travel_time_distribution[travel_time] += 1
        else:
            data.travel_time_distribution[travel_time] = 1

    if static_infs.originID != parkings_pedestrian_centroid_in:
        parkingGroup.add_pedestrian_count_to_parking()

    if destinationCentroid == parkings_pedestrian_centroid_out:
        parkingGroup.api_exit_pedestrian(idPedestrian)

    if idPedestrian in pedestrians_to_track_3:
        pedestrians_to_track_3.remove(idPedestrian)
        
    if idPedestrian in pedestrians_to_track_2:
        pedestrians_to_track_2.remove(idPedestrian)
        
    if idPedestrian in pedestrians_to_track:
        pedestrians_to_track.remove(idPedestrian)
    return 0

def AAPIEnterVehicleSection(idveh, idsection, atime):
    return 0


def AAPIExitVehicleSection(idveh, idsection, atime):
    return 0


def AAPIVehicleStartParking(idveh, idsection, time):
    return 0
    
    
def is_current_time_in_interval(current_sim_time, offset, wait_duration, total_duration, driving_offset=2.5 * 60):
    offset +=  driving_offset
    if offset + wait_duration < total_duration:
        return current_sim_time % total_duration > offset and current_sim_time % total_duration < offset + wait_duration
    else:
        if offset > total_duration:
            return current_sim_time % total_duration > offset % total_duration and current_sim_time % total_duration < (offset + wait_duration) % total_duration
        else:
            return current_sim_time % total_duration > offset or current_sim_time % total_duration < (offset + wait_duration) % total_duration

def is_pos_in_box(position, box, border=1):
    if  position.x > box["x_left"] - border and \
        position.x < box["x_right"] + border and \
        position.y > box["y_bottom"] - border and \
        position.y < box["y_top"] + border:
        return True
    else:
        return False
    
def add_vhc_to_remove(idveh):
    global parkingGroup
    parkingGroup.removableVhcs.append(idveh)


check_in_coords = {
    'checkin_1': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477610.7,
        'x_right':  477618.6,
        'y_top':    5052831.7,
        'y_bottom': 5052825.6
    },
    'checkin_2': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477631.1,
        'x_right':  477636.8,
        'y_top':    5052821.3,
        'y_bottom': 5052815.0
    },
    'checkin_3': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477650.5,
        'x_right':  477654.7,
        'y_top':    5052808.8,
        'y_bottom': 5052804.4
    },
    'checkin_4': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477649.2,
        'x_right':  477655.7,
        'y_top':    5052755.6,
        'y_bottom': 5052752.4
    },
    'checkin_5': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477654.2,
        'x_right':  477659.1, 
        'y_top':    5052733.7,
        'y_bottom': 5052730.6
    },
    'checkin_6': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477658.1, 
        'x_right':  477662.9,
        'y_top':    5052713.8,
        'y_bottom': 5052710.7
    },
    'checkin_7': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477662.1, 
        'x_right':  477666.9, 
        'y_top':    5052696.0,
        'y_bottom': 5052692.9
    },
    'checkin_8': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477674.4, 
        'x_right':  477677.2, 
        'y_top':    5052635.4,
        'y_bottom': 5052633.8
    },
    'checkin_9': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477678.8, 
        'x_right':  477685.4, 
        'y_top':    5052613.7,
        'y_bottom': 5052612.0
    },
    'checkin_10': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477682.6, 
        'x_right':  477685.4, 
        'y_top':    5052593.3,
        'y_bottom': 5052591.6
    },
    'checkin_11': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477686.2, 
        'x_right':  477689.0, 
        'y_top':    5052575.5,
        'y_bottom': 5052573.8
    },
    'fast_checkin': {
        'service_point_name': 'CHECK_IN',
        'x_left':   477676.3, 
        'x_right':  477679.8, 
        'y_top':    5052667.5,
        'y_bottom': 5052664.5
    }
}

x_ray_coords = {
    'x_ray_1': {
        'service_point_name': 'X_RAY',
        'x_left':   477678.2, 
        'x_right':  477687.6, 
        'y_top':    5052801.2,
        'y_bottom': 5052795.8
    },
    'x_ray_2': {
        'service_point_name': 'X_RAY',
        'x_left':   477679.8, 
        'x_right':  477688.3, 
        'y_top':    5052794.4,
        'y_bottom': 5052789.6
    },
    'x_ray_3':  {'x_left': 477681.0, 'x_right': 477689.5, 'y_top': 5052787.7, 'y_bottom': 5052782.9, 'service_point_name': 'X_RAY'}, 
    'x_ray_4':  {'x_left': 477682.4, 'x_right': 477690.9, 'y_top': 5052780.4, 'y_bottom': 5052775.6, 'service_point_name': 'X_RAY'}, 
    'x_ray_5':  {'x_left': 477683.7, 'x_right': 477692.2, 'y_top': 5052773.4, 'y_bottom': 5052768.6, 'service_point_name': 'X_RAY'}, 
    'x_ray_6':  {'x_left': 477685.1, 'x_right': 477693.6, 'y_top': 5052766.0, 'y_bottom': 5052761.3, 'service_point_name': 'X_RAY'}, 
    'x_ray_7':  {'x_left': 477686.8, 'x_right': 477695.3, 'y_top': 5052759.0, 'y_bottom': 5052754.3, 'service_point_name': 'X_RAY'}, 
    'x_ray_8':  {'x_left': 477688.2, 'x_right': 477696.7, 'y_top': 5052751.6, 'y_bottom': 5052746.9, 'service_point_name': 'X_RAY'}, 
    'x_ray_9':  {'x_left': 477689.7, 'x_right': 477698.2, 'y_top': 5052745.3, 'y_bottom': 5052740.6, 'service_point_name': 'X_RAY'}, 
    'x_ray_10': {'x_left': 477691.0, 'x_right': 477699.5, 'y_top': 5052737.8, 'y_bottom': 5052733.0, 'service_point_name': 'X_RAY'},
    'x_ray_11': {'x_left': 477710.7, 'x_right': 477719.8, 'y_top': 5052663.2, 'y_bottom': 5052658.0, 'service_point_name': 'X_RAY'},
    'x_ray_12': {'x_left': 477712.1, 'x_right': 477721.2, 'y_top': 5052655.9, 'y_bottom': 5052650.6, 'service_point_name': 'X_RAY'},
    'x_ray_13': {'x_left': 477713.3, 'x_right': 477722.4, 'y_top': 5052649.9, 'y_bottom': 5052643.7, 'service_point_name': 'X_RAY'},
    'x_ray_14': {'x_left': 477714.8, 'x_right': 477723.9, 'y_top': 5052641.6, 'y_bottom': 5052636.4, 'service_point_name': 'X_RAY'},
    'x_ray_15': {'x_left': 477715.9, 'x_right': 477724.9, 'y_top': 5052634.6, 'y_bottom': 5052629.4, 'service_point_name': 'X_RAY'},
    'x_ray_16': {'x_left': 477717.4, 'x_right': 477726.5, 'y_top': 5052627.6, 'y_bottom': 5052622.3, 'service_point_name': 'X_RAY'},
    'x_ray_17': {'x_left': 477718.6, 'x_right': 477727.7, 'y_top': 5052620.9, 'y_bottom': 5052615.6, 'service_point_name': 'X_RAY'},
    'x_ray_18': {'x_left': 477719.9, 'x_right': 477729.0, 'y_top': 5052614.1, 'y_bottom': 5052608.9, 'service_point_name': 'X_RAY'},
    'x_ray_19': {'x_left': 477721.3, 'x_right': 477730.4, 'y_top': 5052606.7, 'y_bottom': 5052601.5, 'service_point_name': 'X_RAY'},
    'x_ray_20': {'x_left': 477722.6, 'x_right': 477731.6, 'y_top': 5052599.9, 'y_bottom': 5052594.6, 'service_point_name': 'X_RAY'}
}

passport_check_coords = {
    'passport_check_1': {
        'service_point_name': 'PASSPORT_CHECK',
        'x_left':   477560.1,
        'x_right':  477593.5,
        'y_top':    5052987.5,
        'y_bottom': 5052969.0
    },
    'passport_check_2': {
        'service_point_name': 'PASSPORT_CHECK',
        'x_left':   477623.7,
        'x_right':  477643.7,
        'y_top':    5052925.4,
        'y_bottom': 5052894.0
    }
}

gates_coords = {
    'gate_1': { 
        'service_point_name': 'GATE',
        'x_left':   477725.1,
        'x_right':  477733.0,
        'y_top':    5053105.1,
        'y_bottom': 5053091.1
    },
    'gate_2': {
        'service_point_name': 'GATE',
        'x_left':   477773.7,
        'x_right':  477780.6,
        'y_top':    5053114.5,
        'y_bottom': 5053100.4
    },
    'gate_3': {
        'service_point_name': 'GATE',
        'x_left':   477788.4,
        'x_right':  477795.8,
        'y_top':    5053111.9,
        'y_bottom': 5053097.9
    },
    'gate_4': {
        'service_point_name': 'GATE',
        'x_left':   477778.6,
        'x_right':  477798.7,
        'y_top':    5053088.2,
        'y_bottom': 5053082.5
    },
    'gate_5': {
        'service_point_name': 'GATE',
        'x_left':   477780.1,
        'x_right':  477800.3,
        'y_top':    5053073.7,
        'y_bottom': 5053068.3
    },
    'gate_6': {
        'service_point_name': 'GATE',
        'x_left':   477763.3,
        'x_right':  477769.3,
        'y_top':    5053062.9,
        'y_bottom': 5053048.4
    },
    'gate_7': {
        'service_point_name': 'GATE',
        'x_left':   477736.2,
        'x_right':  477742.5,
        'y_top':    5053056.8,
        'y_bottom': 5053042.5
    },
    'gate_8': {
        'service_point_name': 'GATE',
        'x_left':   477783.1,
        'x_right':  477789.6,
        'y_top':    5052750.2,
        'y_bottom': 5052735.7
    },
    'gate_9': {
        'service_point_name': 'GATE',
        'x_left':   477623.7,
        'x_right':  477643.7,
        'y_top':    5052925.4,
        'y_bottom': 5052894.0
    },
    'gate_10': {
        'service_point_name': 'GATE',
        'x_left':   477832.9,
        'x_right':  477839.4,
        'y_top':    5052763.1,
        'y_bottom': 5052748.7
    },
    'gate_11': {
        'service_point_name': 'GATE',
        'x_left':   477853.0,
        'x_right':  477859.5,
        'y_top':    5052760.5,
        'y_bottom': 5052746.0
    }, 
    'gate_12': {
        'service_point_name': 'GATE',
        'x_left':   477842.6,
        'x_right':  477862.4,
        'y_top':    5052740.6,
        'y_bottom': 5052734.1
    },
    'gate_13': {
        'service_point_name': 'GATE',
        'x_left':   477844.5,
        'x_right':  477864.4,
        'y_top':    5052721.0,
        'y_bottom': 5052714.4
    },
    'gate_14': {
        'service_point_name': 'GATE',
        'x_left':   477824.6,
        'x_right':  477831.1,
        'y_top':    5052713.1,
        'y_bottom': 5052698.8
    },
    'gate_15': {
        'service_point_name': 'GATE',
        'x_left':   477858.1,
        'x_right':  477864.5,
        'y_top':    5052407.3,
        'y_bottom': 5052392.9
    },
    'gate_16': {
        'service_point_name': 'GATE',
        'x_left':   477776.9,
        'x_right':  477783.8,
        'y_top':    5052717.9,
        'y_bottom': 5052703.6
    },
    'gate_17': {
        'service_point_name': 'GATE',
        'x_left':   477858.1,
        'x_right':  477864.5,
        'y_top':    5052407.3,
        'y_bottom': 5052392.9
    },
    'gate_18': {
        'service_point_name': 'GATE',
        'x_left':   477900.9,
        'x_right':  477907.4,
        'y_top':    5052415.4,
        'y_bottom': 5052401.0
    },
    'gate_19': {
        'service_point_name': 'GATE',
        'x_left':   477918.6,
        'x_right':  477925.5,
        'y_top':    5052410.8,
        'y_bottom': 5052396.5
    },
    'gate_20': {
        'service_point_name': 'GATE',
        'x_left':   477907.9,
        'x_right':  477927.7,
        'y_top':    5052392.7,
        'y_bottom': 5052386.1
    },
    'gate_21': {
        'service_point_name': 'GATE',
        'x_left':   477912.0,
        'x_right':  477931.8,
        'y_top':    5052372.5,
        'y_bottom': 5052366.0
    },
    'gate_22': {
        'service_point_name': 'GATE',
        'x_left':   477899.3,
        'x_right':  477906.4,
        'y_top':    5052367.2,
        'y_bottom': 5052353.1
    },
    'gate_23': {
        'service_point_name': 'GATE',
        'x_left':   477867.5,
        'x_right':  477874.4,
        'y_top':    5052362.2,
        'y_bottom': 5052347.8
    },
    'gate_24': {
        'service_point_name': 'GATE',
        'x_left':   477843.8,
        'x_right':  477850.7,
        'y_top':    5052371.5,
        'y_bottom': 5052357.0
    }}


TOTAL_DURATION = 48

#units: in minutes
timetable_per_gate = {
    27968: {'offset': 36, 
            'driving_offset': 2.5,
            'wait_duration': 2,
            'pedestrian_box': {
                "x_left":   477726.1,
                "x_right":  477733.0, 
                "y_top":    5053105.1,
                "y_bottom": 5053091.1,
            }},
    28026: {'offset': 22, 
            'driving_offset': 2.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477773.9,
                'x_right':  477780.0,
                'y_top':    5053114.7,
                'y_bottom': 5053100.2
            }},
    28078: {'offset': 0, 
            'driving_offset': 2.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477789.1,
                'x_right':  477795.1,
                'y_top':    5053112.2,
                'y_bottom': 5053097.7
            }},
    28137: {'offset': 6, 
            'driving_offset': 2.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477778.7,
                'x_right':  477798.5,
                'y_top':    5053088.7,
                'y_bottom': 5053082.1
            }},
    28169: {'offset': 44, 
            'driving_offset': 2.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477780.2,
                'x_right':  477800.0,
                'y_top':    5053074.2,
                'y_bottom': 5053067.6
            }},
    28217: {'offset': 12, 
            'driving_offset': 2.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477763.3,
                'x_right':  477769.3,
                'y_top':    5053062.9,
                'y_bottom': 5053048.4
            }},
    28289: {'offset': 38, 
            'driving_offset': 2.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477736.2,
                'x_right':  477742.5,
                'y_top':    5053056.8,
                'y_bottom': 5053042.5
            }},
    29123: {'offset': 28, 
            'driving_offset': 2.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477717.4,
                'x_right':  477723.8,
                'y_top':    5053063.9,
                'y_bottom': 5053049.5
            }},##################################
    28551: {'offset': 18, 
            'driving_offset': 3.0,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477783.1,
                'x_right':  477789.6,
                'y_top':    5052750.2,
                'y_bottom': 5052735.7
            }},
    28497: {'offset': 34,  #10
            'driving_offset': 3.0,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477832.9,
                'x_right':  477839.4,
                'y_top':    5052763.1,
                'y_bottom': 5052748.7
            }},
    28501: {'offset': 24, 
            'driving_offset': 3.0,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477853.0,
                'x_right':  477859.5,
                'y_top':    5052760.5,
                'y_bottom': 5052746.0
            }},
    28505: {'offset': 32, #12
            'driving_offset': 3.0,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477842.6,
                'x_right':  477862.4,
                'y_top':    5052740.6,
                'y_bottom': 5052734.1
            }},
    28509: {'offset': 2, 
            'driving_offset': 3.0,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477844.5,
                'x_right':  477864.4,
                'y_top':    5052721.0,
                'y_bottom': 5052714.4
            }},
    28513: {'offset': 8,  #14
            'driving_offset': 3.0,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477824.6,
                'x_right':  477831.1,
                'y_top':    5052713.1,
                'y_bottom': 5052698.8
            }},
    28517: {'offset': 26, 
            'driving_offset': 3.0,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477800.5,
                'x_right':  477807.0,
                'y_top':    5052710.0,
                'y_bottom': 5052695.5
            }},
    28521: {'offset': 46, #16
            'driving_offset': 3.0,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477776.9,
                'x_right':  477783.8,
                'y_top':    5052717.9,
                'y_bottom': 5052703.6
            }},
    28769: {'offset': 16, 
            'driving_offset': 3.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477858.1,
                'x_right':  477864.5,
                'y_top':    5052407.3,
                'y_bottom': 5052392.9
            }},
    28773: {'offset': 40, #18
            'driving_offset': 3.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477900.9,
                'x_right':  477907.4,
                'y_top':    5052415.4,
                'y_bottom': 5052401.0
            }},
    28777: {'offset': 30, 
            'driving_offset': 3.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477918.6,
                'x_right':  477925.5,
                'y_top':    5052410.8,
                'y_bottom': 5052396.5
            }},
    28781: {'offset': 14, #20
            'driving_offset': 3.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477907.9,
                'x_right':  477927.7,
                'y_top':    5052392.7,
                'y_bottom': 5052386.1
            }},
    28785: {'offset': 42, 
            'driving_offset': 3.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477912.0,
                'x_right':  477931.8,
                'y_top':    5052372.5,
                'y_bottom': 5052366.0
            }},
    28789: {'offset': 20, #22
            'driving_offset': 3.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477899.3,
                'x_right':  477906.4,
                'y_top':    5052367.2,
                'y_bottom': 5052353.1
            }},
    28793: {'offset': 4, 
            'driving_offset': 3.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477867.5,
                'x_right':  477874.4,
                'y_top':    5052362.2,
                'y_bottom': 5052347.8
            }},
    28797: {'offset': 10, #24
            'driving_offset': 3.5,
            'wait_duration': 2,
            'pedestrian_box': {
                'x_left':   477843.8,
                'x_right':  477850.7,
                'y_top':    5052371.5,
                'y_bottom': 5052357.0
            }}
}