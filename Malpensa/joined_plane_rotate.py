import lib.plane_rotate as pr
from AAPI import *


def AAPILoad():
    return 0


def AAPIInit():
    global rotations_group
    rotations_group = []
    
    aicraft_one_rotation_gate_one = pr.PlaneRotate(
        plane_start_sections = [27934, 27970, 28017],
        plane_end_section = 27927,
        rotation_centroids = [27932, 27954, 27972, 27947],
        remaining_times = [15, 25],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_one_rotation_gate_one)


    aicraft_one_rotation_gate_two = pr.PlaneRotate(
        plane_start_sections = [28004, 28011, 28070],
        plane_end_section = 27999,
        rotation_centroids = [27996, 27997, 27998, 27947],
        remaining_times = [12, 25],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_one_rotation_gate_two)


    aicraft_one_rotation_gate_three = pr.PlaneRotate(
        plane_start_sections = [28049, 28051, 28056, 28122],
        plane_end_section = 28044,
        rotation_centroids = [28059, 28060, 28061, 28062, 27947],
        remaining_times = [3.5, 3.3, 25],
        nb_rotation_steps = 3
    )
    rotations_group.append(aicraft_one_rotation_gate_three)


    aicraft_one_rotation_gate_four = pr.PlaneRotate(
        plane_start_sections = [28144, 28104, 28099, 28103, 27165],
        plane_end_section = 28095,
        rotation_centroids = [28146, 28111, 28112, 28113, 28114, 27947],
        remaining_times = [10, 5.5, 7, 30],
        nb_rotation_steps = 4
    )
    rotations_group.append(aicraft_one_rotation_gate_four)


    aicraft_one_rotation_gate_five = pr.PlaneRotate(
        plane_start_sections = [28176, 28187, 28194, 28385],
        plane_end_section = 28166,
        rotation_centroids = [28180, 28181, 28182, 28183, 27947],
        remaining_times = [53.2, 10.5, 10],
        nb_rotation_steps = 3
    )
    rotations_group.append(aicraft_one_rotation_gate_five)


    aicraft_one_rotation_gate_six = pr.PlaneRotate(
        plane_start_sections = [28251, 28239, 28245, 28385],
        plane_end_section = 28219,
        rotation_centroids = [28230, 28231, 28232, 28233, 27947],
        remaining_times = [21, 60, 10],
        nb_rotation_steps = 3
    )
    rotations_group.append(aicraft_one_rotation_gate_six)


    aicraft_one_rotation_gate_seven = pr.PlaneRotate(
        plane_start_sections = [28296, 28307, 28314, 28385],
        plane_end_section = 28293,
        rotation_centroids = [28300, 28301, 28302, 28303, 27947],
        remaining_times = [22.5, 70, 11],
        nb_rotation_steps = 3
    )
    rotations_group.append(aicraft_one_rotation_gate_seven)

    aicraft_one_rotation_gate_eight = pr.PlaneRotate(
        plane_start_sections = [29100, 29103, 29107, 28385],
        plane_end_section = 29096,
        rotation_centroids = [29111, 29112, 29113, 29114, 27947],
        remaining_times = [21, 77, 11],
        nb_rotation_steps = 3
    )
    rotations_group.append(aicraft_one_rotation_gate_eight)

    aicraft_two_rotation_gate_one = pr.PlaneRotate(
        plane_start_sections = [28557, 28588, 28616, 28568],
        plane_end_section = 28451,
        rotation_centroids = [28443, 28591, 28592, 28620, 27947],
        remaining_times = [15, 7.5, 32],
        nb_rotation_steps = 3
    )
    rotations_group.append(aicraft_two_rotation_gate_one)


    aicraft_two_rotation_gate_two = pr.PlaneRotate(
        plane_start_sections = [28598, 28602, 28562],
        plane_end_section = 28452,
        rotation_centroids = [28444, 28604, 28605, 27947],
        remaining_times = [12, 7.5],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_two_rotation_gate_two)


    aicraft_two_rotation_gate_three = pr.PlaneRotate(
        plane_start_sections = [28803, 28806, 28561],
        plane_end_section = 28453,
        rotation_centroids = [28445, 28812, 28813, 27947],
        remaining_times = [12, 7],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_two_rotation_gate_three)


    aicraft_two_rotation_gate_four = pr.PlaneRotate(
        plane_start_sections = [28824, 28829, 28568],
        plane_end_section = 28454,
        rotation_centroids = [28446, 28831, 28832, 27947],
        remaining_times = [15, 7.5],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_two_rotation_gate_four)


    aicraft_two_rotation_gate_five = pr.PlaneRotate(
        plane_start_sections = [28839, 28843, 28892],
        plane_end_section = 28455,
        rotation_centroids = [28447, 28847, 28848, 27947],
        remaining_times = [15, 7.5],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_two_rotation_gate_five)


    aicraft_two_rotation_gate_six = pr.PlaneRotate(
        plane_start_sections = [28855, 28858, 28581],
        plane_end_section = 28456,
        rotation_centroids = [28448, 28862, 28863, 27947],
        remaining_times = [14, 15],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_two_rotation_gate_six)


    aicraft_two_rotation_gate_seven = pr.PlaneRotate(
        plane_start_sections = [28870, 28875, 28581],
        plane_end_section = 28457,
        rotation_centroids = [28449, 28877, 28878, 27947],
        remaining_times = [12, 13],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_two_rotation_gate_seven)


    aicraft_two_rotation_gate_eight = pr.PlaneRotate(
        plane_start_sections = [28889, 28897, 28901, 28903, 28574],
        plane_end_section = 28458,
        rotation_centroids = [28450, 28907, 28908, 28909, 28917, 27947],
        remaining_times = [14, 9, 21, 17],
        nb_rotation_steps = 4
    )
    rotations_group.append(aicraft_two_rotation_gate_eight)


    aicraft_three_rotation_gate_one = pr.PlaneRotate(
        plane_start_sections = [28923, 28926, 28931, 28719],
        plane_end_section = 28711,
        rotation_centroids = [28703, 28935, 28936, 28937, 27947],
        remaining_times = [14, 6, 27],
        nb_rotation_steps = 3
    )
    rotations_group.append(aicraft_three_rotation_gate_one)
    

    aicraft_three_rotation_gate_two = pr.PlaneRotate(
        plane_start_sections = [28945, 28950, 28964],
        plane_end_section = 28738,
        rotation_centroids = [28704, 28953, 28954, 27947],
        remaining_times = [14, 6],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_three_rotation_gate_two)

    
    aicraft_three_rotation_gate_three = pr.PlaneRotate(
        plane_start_sections = [28961, 28968, 28713],
        plane_end_section = 28739,
        rotation_centroids = [28705, 28971, 28972, 27947],
        remaining_times = [14, 6],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_three_rotation_gate_three)

    
    aicraft_three_rotation_gate_four = pr.PlaneRotate(
        plane_start_sections = [28979, 28982, 28719],
        plane_end_section = 28740,
        rotation_centroids = [28706, 28986, 28987, 27947],
        remaining_times = [14, 6],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_three_rotation_gate_four)

    
    aicraft_three_rotation_gate_five = pr.PlaneRotate(
        plane_start_sections = [28993, 28997, 28720],
        plane_end_section = 28741,
        rotation_centroids = [28707, 29001, 29002, 27947],
        remaining_times = [14, 6],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_three_rotation_gate_five)


    aicraft_three_rotation_gate_six = pr.PlaneRotate(
        plane_start_sections = [29008, 29015, 28735],
        plane_end_section = 28742,
        rotation_centroids = [28708, 29016, 29017, 27947],
        remaining_times = [14, 16],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_three_rotation_gate_six)

            
    aicraft_three_rotation_gate_seven = pr.PlaneRotate(
        plane_start_sections = [29028, 29033, 29024],
        plane_end_section = 28743,
        rotation_centroids = [28709, 29035, 29036, 27947],
        remaining_times = [14, 16],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_three_rotation_gate_seven)

                
    aicraft_three_rotation_gate_eight = pr.PlaneRotate(
        plane_start_sections = [29043, 29046, 29024],
        plane_end_section = 28744,
        rotation_centroids = [28710, 29050, 29051, 27947],
        remaining_times = [20, 4],
        nb_rotation_steps = 2
    )
    rotations_group.append(aicraft_three_rotation_gate_eight)

    return 0


def AAPISimulationReady():
    return 0


def AAPIManage(time, timeSta, timeTrans, acycle):
    global rotations_group
    
    for rotation in rotations_group:
        rotation.manage_rotations()

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
