import joined_parking as jp
import lib.plane_rotate as pr
from AAPI import *


def AAPILoad():
    return 0
"""
REMAINING_TIME_KEY = "remaining_time"
ROTATION_STATE_KEY = "rotation_state"
VEH_ID_KEY = "veh_id"

PLANE_TYPE = 2

plane_start_sections = [27934, 27970, 27165]
plane_end_sections = [27927]
rotation_centroids = [27932, 27954, 27972, 27947]
remaining_times = [15, 16]
vehicles_go_backward = []

NB_ROTATION_STEPS = 2
"""
rotations_group = []

def AAPIInit():
    
    rotation_gate_one = pr.PlaneRotate(
        plane_start_sections    = [27934, 27970, 27165],
        plane_end_section      = 27927,
        rotation_centroids      = [27932, 27954, 27972, 27947],
        remaining_times         = [15, 16],
        vehicles_go_backward    = [],
        nb_rotation_steps       = 2
    )

    rotations_group.append(rotation_gate_one)

    return 0


def AAPISimulationReady():
    return 0


def AAPIManage(time, timeSta, timeTrans, acycle):
    for rotation in rotations_group:
        rotation.manage_rotations()
    """
    for vehicle in vehicles_go_backward:
        vehicle[REMAINING_TIME_KEY] -= AKIGetSimulationStepTime()
        if vehicle[REMAINING_TIME_KEY] < 0:
            vehicle_rotation_state = vehicle[ROTATION_STATE_KEY]
            jp.removableVhcs.append(vehicle[VEH_ID_KEY])
            vehicles_go_backward.remove(vehicle)
            if vehicle_rotation_state < NB_ROTATION_STEPS:
                create_backward_vehicle(plane_start_sections[vehicle_rotation_state], 
                                        PLANE_TYPE, 
                                        rotation_centroids[vehicle_rotation_state],
                                        rotation_centroids[vehicle_rotation_state+1],
                                        speed=-20,
                                        remaining_time=remaining_times[vehicle_rotation_state],
                                        rotation_state=vehicle_rotation_state+1)
                
            if vehicle_rotation_state == NB_ROTATION_STEPS:
                AKIEnterVehTrafficOD(plane_start_sections[-1], PLANE_TYPE, rotation_centroids[-2], rotation_centroids[-1], 0)
    """

    return 0


def AAPIPostManage(time, timeSta, timeTrans, acycle):

    return 0


def AAPIFinish():
    return 0


def AAPIUnLoad():
    return 0


def AAPIPreRouteChoiceCalculation(time, timeSta):
    return 0


def AAPIEnterVehicle(idveh, idsection):

    return 0


def AAPIExitVehicle(idveh, idsection):
    for rotation in rotations_group:
        rotation.init_plane_rotation(idsection)

    """
    if idsection == plane_end_sections[0]:
        create_backward_vehicle(plane_start_sections[0], 
                                PLANE_TYPE, 
                                rotation_centroids[0], 
                                rotation_centroids[1], 
                                -20, 
                                remaining_times[0], 
                                1)
    """
    return 0


def AAPIEnterPedestrian(idPedestrian, originCentroid):
    return 0


def AAPIExitPedestrian(idPedestrian, destinationCentroid):
    return 0


def AAPIEnterVehicleSection(idveh, idsection, atime):
    return 0


def AAPIExitVehicleSection(idveh, idsection, atime):
    return 0


def AAPIVehicleStartParking(idveh, idsection, time):
    return 0
"""
def create_backward_vehicle(start_section, vehicle_type, start_centroid, end_centroid, speed = -20, remaining_time = 15, rotation_state = 1):
    new_vehid = AKIEnterVehTrafficOD(start_section, vehicle_type, start_centroid, end_centroid, 0)
    vehicles_go_backward.append({VEH_ID_KEY: new_vehid, REMAINING_TIME_KEY: remaining_time, ROTATION_STATE_KEY: rotation_state})
    set_vehicle_max_speed_from_static_infs(new_vehid, speed)


def set_vehicle_max_speed_from_static_infs(idveh, desired_speed):
    static_infs = AKIVehGetStaticInf(idveh)
    static_infs.maxDesiredSpeed = desired_speed
    ret_val = AKIVehSetStaticInf(idveh, static_infs)
"""