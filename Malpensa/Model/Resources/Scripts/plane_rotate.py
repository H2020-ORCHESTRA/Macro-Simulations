from lib.parking import Parking, ParkingGroup

from AAPI import *


def AAPILoad():
    return 0


def AAPIInit():
    # --------------------------------------------------------------------
    global parkingGroup

    # init parameters for ALL parkings ...................................
    totIn = 0
    totOut = 0
    occupancy = 0

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

    parkingN = Parking(
            title="parking N",
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

    parkingC1 = Parking(
            title="parking Center #1",
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

    parkingC2 = Parking(
            title="parking Center #2",
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

    parkingS = Parking(
            title="parking S",
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

    # --------------------------------------------------------------------

    # removableVhcs contains a list of all vehicle IDs that are to be removed.
    global removableVhcs
    removableVhcs = []

    return 0


def AAPISimulationReady():
    return 0


def AAPIManage(time, timeSta, timeTrans, acycle):
    global removableVhcs

    # map(AKIVehTrackedRemove, removableVhcs)
    for rmv in list(removableVhcs):
        # AKIPrintString(f"removing vhc {rmv}")
        removableVhcs.remove(rmv)
        AKIVehSetAsTracked(rmv)
        AKIVehTrackedRemove(rmv)
    return 0


def AAPIPostManage(time, timeSta, timeTrans, acycle):
    global parkingGroup

    # Update label values of parkings
    for p in parkingGroup.parkings:
        p.updateLabels()
    return 0


def AAPIFinish():
    return 0


def AAPIUnLoad():
    return 0


def AAPIPreRouteChoiceCalculation(time, timeSta):
    return 0


def AAPIEnterVehicle(idveh, idsection):
    global parkingGroup

    # Handle parking exit
    for p in parkingGroup.parkings:
        if idsection == p.outSectionId:
            p.totOut = p.totOut + 1
            p.occupancy = p.occupancy - 1
        if p.occupancy < 0: # if parking empty
            removableVhcs.append(idveh)
            p.totOut = p.totOut - 1
            p.occupancy = p.occupancy + 1
    return 0


def AAPIExitVehicle(idveh, idsection):
    global parkingGroup

    # Handle parking entrance
    for p, n in zip(parkingGroup.parkings, parkingGroup.get_nexts()):
        if idsection == p.inSectionId:
            p.totIn = p.totIn + 1
            p.occupancy = p.occupancy + 1
        if p.occupancy > p.maxCapacity:
            AKIEnterVehTrafficOD(p.outSectionId, 0, p.parkingId, n.parkingId, 0)
            p.totIn = p.totIn - 1
            p.occupancy = p.occupancy - 1
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
