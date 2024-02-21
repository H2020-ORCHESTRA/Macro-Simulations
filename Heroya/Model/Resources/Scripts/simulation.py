import sys
import depot
import parking
import platooning
from helpers import *

parkingGroup: parking.ParkingGroup

# init parameters for ALL parkings ...................................
totIn: int = 0
totOut: int = 0
occupancy: int = 0


# Parking Center #1 ..................................................

# centroid id of parking
parkingId: int = 22175
enterSectionId: int = 22169
# parkingId: int = 23010
# enterSectionId: int = 23004

truckSwitchSectionId = 22367
truckStopSectionId = 23468 #22350
robotSectionId = 22353
exitSectionId: int = 22353
# truckSwitchSectionId = 22605
# truckStopSectionId = 22595
# robotSectionId = 22592
# exitSectionId: int = 22592

# IDs of labels
occId: int = 22189
maxId: int = 22182
inId: int = 22191
outId: int = 22184
robotId: int = 22188

maxCapacity: int = 50

# Depots .............................................................
"""
centroid_depot_1: int = 22152
in_section_depot_1: int = 22149
out_section_depot_1: int = 22044
unloading_depot_1: int = 22209
ready_depot_1: int = 22211

centroid_depot_2: int = 22154
in_section_depot_2: int = 22146
out_section_depot_2: int = 22004
unloading_depot_2: int = 22213
ready_depot_2: int = 22212

centroid_depot_3: int = 486
in_section_depot_3: int = 478
out_section_depot_3: int = 496
unloading_depot_3: int = 522
ready_depot_3: int = 521
"""

centroid_depot_4: int = 22434
in_section_depot_4: int = 22437
out_section_depot_4: int = 22433
unloading_depot_4: int = 22229
ready_depot_4: int = 22228

"""
centroid_depot_5: int = 488
in_section_depot_5: int = 482
out_section_depot_5: int = 498
unloading_depot_5: int = 532
ready_depot_5: int = 531
"""

centroid_depot_6: int = 22424
in_section_depot_6: int = 22427
out_section_depot_6: int = 22423
unloading_depot_6: int = 22246
ready_depot_6: int = 22247

centroid_depot_7: int = 22439
in_section_depot_7: int = 22442
out_section_depot_7: int = 22438
unloading_depot_7: int = 22253
ready_depot_7: int = 22254

centroid_depot_8: int = 22429
in_section_depot_8: int = 22432
out_section_depot_8: int = 22428
unloading_depot_8: int = 22257
ready_depot_8: int = 22258

centroid_depot_9: int = 22444
in_section_depot_9: int = 22447
out_section_depot_9: int = 22443
unloading_depot_9: int = 22264
ready_depot_9: int = 22265

centroid_depot_yara: int = 23098
in_section_depot_yara: int = 23077
out_section_depot_yara: int = 23078
unloading_depot_yara: int = 23111
ready_depot_yara: int = 23112

# Platooning .........................................................
MAX_TRUCKS_PLATOONING = 5

section_id = 22169 #22217
end_section = 17821
start_centroid = 21734 #parkingId # 22175
end_centroid = 22115 #22176
depot_centroids = [
    centroid_depot_4,
    centroid_depot_6,
    centroid_depot_7,
    centroid_depot_8,
    centroid_depot_9,
    centroid_depot_yara
    ]

depot_infos = { # in_section: centroid, out_section
    in_section_depot_4: [centroid_depot_4, out_section_depot_4],
    in_section_depot_6: [centroid_depot_6, out_section_depot_6],
    in_section_depot_7: [centroid_depot_7, out_section_depot_7],
    in_section_depot_8: [centroid_depot_8, out_section_depot_8],
    in_section_depot_9: [centroid_depot_9, out_section_depot_9],
    in_section_depot_yara: [centroid_depot_yara, out_section_depot_yara]
    }


def AAPILoad():
    """Call when the module is loaded by Aimsun Next.

    The function is called first.
    """
    print(f"Python Version: {sys.version}")
    return 0


def AAPIInit():
    """Call when Aimsun Next starts the simulation.

    Can be used to initialize the module.
    The function is called second.
    """
    global parkingGroup, platoon, depotGroup

    load_csv_file()
    print("CSV imported!")

    platoon = platooning.Platooning(
        section_id=section_id,
        start_centroid=start_centroid,
        end_centroid=end_centroid,
        end_section=end_section,
        depot_centroids=depot_centroids,
        depot_infos=depot_infos,
        amount_of_trucks=MAX_TRUCKS_PLATOONING
        )

    parkingC1 = parking.Parking(
        title="parking Center #1",
        parkingId=parkingId,
        enterSectionId=enterSectionId,
        exitSectionId=exitSectionId,
        truckSwitchSectionId = truckSwitchSectionId,
        truckStopSectionId = truckStopSectionId,
        robotSectionId = robotSectionId,
        occId=occId,
        maxId=maxId,
        inId=inId,
        outId=outId,
        robotId=robotId,
        platooning=platoon,
        maxCapacity=maxCapacity,
        totIn=totIn,
        totOut=totOut,
        occupancy=occupancy,
    )

    parkingGroup = parking.ParkingGroup([parkingC1])

    """
    depot_1 = depot.Depot(
        title="depot 1",
        depotId=centroid_depot_1,
        inSectionId=in_section_depot_1,
        outSectionId=out_section_depot_1,
        unloadind_id=unloading_depot_1,
        ready_id=ready_depot_1
    )
    depot_2 = depot.Depot(
        title="depot 2",
        depotId=centroid_depot_2,
        inSectionId=in_section_depot_2,
        outSectionId=out_section_depot_2,
        unloadind_id=unloading_depot_2,
        ready_id=ready_depot_2
    )
    depot_3 = depot.Depot(
        title="depot 3",
        depotId=centroid_depot_3,
        inSectionId=in_section_depot_3,
        outSectionId=out_section_depot_3,
        unloadind_id=unloading_depot_3,
        ready_id=ready_depot_3
    )
    """
    depot_4 = depot.Depot(
        title="depot 4",
        depotId=centroid_depot_4,
        inSectionId=in_section_depot_4,
        outSectionId=out_section_depot_4,
        unloadind_id=unloading_depot_4,
        ready_id=ready_depot_4
    )
    """
    depot_5 = depot.Depot(
        title="depot 5",
        depotId=centroid_depot_5,
        inSectionId=in_section_depot_5,
        outSectionId=out_section_depot_5,
        unloadind_id=unloading_depot_5,
        ready_id=ready_depot_5
    )
    """
    depot_6 = depot.Depot(
        title="depot 6",
        depotId=centroid_depot_6,
        inSectionId=in_section_depot_6,
        outSectionId=out_section_depot_6,
        unloadind_id=unloading_depot_6,
        ready_id=ready_depot_6
    )
    depot_7 = depot.Depot(
        title="depot 7",
        depotId=centroid_depot_7,
        inSectionId=in_section_depot_7,
        outSectionId=out_section_depot_7,
        unloadind_id=unloading_depot_7,
        ready_id=ready_depot_7
    )
    depot_8 = depot.Depot(
        title="depot 8",
        depotId=centroid_depot_8,
        inSectionId=in_section_depot_8,
        outSectionId=out_section_depot_8,
        unloadind_id=unloading_depot_8,
        ready_id=ready_depot_8
    )
    depot_9 = depot.Depot(
        title="depot 9",
        depotId=centroid_depot_9,
        inSectionId=in_section_depot_9,
        outSectionId=out_section_depot_9,
        unloadind_id=unloading_depot_9,
        ready_id=ready_depot_9
    )
    depot_yara = depot.Depot(
        title="depot yara",
        depotId=centroid_depot_yara,
        inSectionId=in_section_depot_yara,
        outSectionId=out_section_depot_yara,
        unloadind_id=unloading_depot_yara,
        ready_id=ready_depot_yara
    )
    depotGroup = depot.DepotGroup(
        platoon=platoon,
        depots=[depot_4, depot_6, depot_7, depot_8, depot_9, depot_yara]
        )

    return 0


def AAPISimulationReady():
    """Call when Aimsun Next has initialized all and vehicles are ready to start moving.

    The function is called third.
    """
    return 0


def AAPIManage(time: float, timeSta: float, timeTrans: float, acycle: float):
    """Call at the begining of a time step, before the simulator performs any actions.

    :param time: Absolute time of simulation in seconds;
                 takes value 0 at the beginning of the simulation
    :type time: float
    :param timeSta: Time of simulation in stationary period, in seconds from midnight
    :type timeSta: float
    :param timeTrans: Duration of warm-up period, in seconds
    :type timeTrans: float
    :param cycle: Duration of each simulation step in seconds
    :type cycle: float
    """
    global parkingGroup, depotGroup

    del timeSta
    del timeTrans
    del acycle

    parkingGroup.sim_step_manage()
    depotGroup.sim_step_manage()

    return 0


def AAPIPostManage(time: float, timeSta: float, timeTrans: float, acycle: float):
    """Call at the end of a time step, after the simulator has performed actions.

    :param time: Absolute time of simulation in seconds;
                 takes value 0 at the beginning of the simulation
    :type time: float
    :param timeSta: Time of simulation in stationary period, in seconds from midnight
    :type timeSta: float
    :param timeTrans: Duration of warm-up period, in seconds
    :type timeTrans: float
    :param cycle: Duration of each simulation step in seconds
    :type cycle: float
    """
    global parkingGroup, depotGroup

    del time
    del timeSta
    del timeTrans
    del acycle

    parkingGroup.sim_step_post_manage()
    depotGroup.sim_step_post_manage()

    return 0


def AAPIFinish():
    """Call when Aimsun Next finishes the simulation.

    Can be used to terminate the module operations, write summary information, close files, etc.
    """
    global parkingGroup

    # print(f"Average time spent inside park: {sum(data.truck_times_inside_park)/len(data.truck_times_inside_park)}")
    parkingGroup.sim_step_finish()
    calculate_kpis()
    save_kpis()
    
    return 0


def AAPIUnLoad():
    """Call when the module is unloaded by Aimsun Next."""
    return 0


def AAPIPreRouteChoiceCalculation(time: float, timeSta: float):
    """Call just before a new cycle of route choice calculation is about to begin.

    It can be used to modify the sections and turnings costs to affect the route choice calculation.

    :param time: Absolute time of simulation in seconds;
                 takes value 0 at the beginning of the simulation
    :type time: float
    :param timeSta: Time of simulation in stationary period, in seconds from midnight
    :type timeSta: float
    """
    del time
    del timeSta

    return 0


def AAPIVehicleStartParking(idveh: int, idsection: int, time: float):
    """Call when a vehicle starts a parking maneuver.

    :param idveh:  Vehicule identifier
    :type idveh: int
    :param idsection: Section identifier where vehicle is doing the parking
    :type idsection: int
    :param time: Current simulation time
    :type time: float
    """
    del idveh
    del idsection
    del time

    return 0


def AAPIEnterVehicle(idveh: int, idsection: int):
    """Call when a new vehicle enters the system.

    When the vehicle enters its first section, not when it enters a Virtual queue if one is present.

    :param idveh: Identifier of the new vehicle entering the network
    :type idveh: int
    :param idsection: Identifier of the section where the vehicle enters the network
    :type idsection: int
    """
    global parkingGroup, depotGroup

    parkingGroup.api_enter_vehicle(idsection=idsection, idveh=idveh)
    depotGroup.api_enter_vehicle(idsection=idsection, idveh=idveh)

    return 0


def AAPIExitVehicle(idveh: int, idsection: int):
    """Call when a vehicle exits the network.

    :param idveh: Identifier of the new vehicle exiting the network
    :type idveh: int
    :param idsection: Identifier of the section where the vehicle exits the network
    :type idsection: int
    """
    global parkingGroup, platoon, depotGroup

    parkingGroup.api_exit_vehicle(idsection=idsection, idveh=idveh)
    # platoon.depot_entry(veh_id=idveh, depot_section=idsection)
    platoon.sim_exit(idsection=idsection, idveh=idveh)
    depotGroup.api_exit_vehicle(idsection=idsection, idveh=idveh)

    return 0


def AAPIEnterPedestrian(idPedestrian: int, originCentroid: int):
    """Call when a new pedestrian enters the system.

    When the pedestrian enters through its entrance.

    :param idPedestrian: Identifier of the new pedestrian entering the network
    :type idPedestrian: int
    :param originCentroid: Identifier of the pedestrian entrance where the pedestrian enters the network
    :type originCentroid: int
    """
    del idPedestrian
    del originCentroid

    return 0


def AAPIExitPedestrian(idPedestrian: int, destinationCentroid: int):
    """Call when a pedestrian exits the network.

    :param idPedestrian: Identifier of the new pedestrian exiting the network
    :type idPedestrian: int
    :param originCentroid: Identifier of the pedestrian exit where the pedestrian exit the network
    :type originCentroid: int
    """
    del idPedestrian
    del destinationCentroid

    return 0


def AAPIEnterVehicleSection(idveh: int, idsection: int, atime: float):
    """Call when a vehicle enters a new section.

    :param idveh: Identifier of the vehicle
    :type idveh: int
    :param idsection: Identifier of the section the vehicle is entering
    :type idsection: int
    :param atime: Absolute time of the simulation when the vehicle enters the section;
                  takes value 0 at the beginning of the simulation
    :type atime: float
    """
    del atime
    global parkingGroup

    parkingGroup.api_enter_vehicle_section(idsection=idsection, idveh=idveh)

    return 0


def AAPIExitVehicleSection(idveh: int, idsection: int, atime: float):
    """Call when a vehicle exits a section.

    :param idveh: Identifier of the vehicle
    :type idveh: int
    :param idsection: Identifier of the section the vehicle is exiting
    :type idsection: int
    :param atime: Absolute time of the simulation when the vehicle exits the section;
                  takes value 0 at the beginning of the simulation
    :type atime: float
    """
    del atime
    global parkingGroup

    parkingGroup.api_exit_vehicle_section(idsection=idsection, idveh=idveh)

    return 0
