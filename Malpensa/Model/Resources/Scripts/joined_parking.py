# Due to Aimsun forcing us to use their own Python (version 3.7.1), it is
# necessary to add path for third party libraries installed on that python
# version.
#
# Note: if on Linux, use 'HOME' instead of 'USERPROFILE'
import sys
import os
sys.path += [f"{os.getenv('USERPROFILE')}/AppData/Local/Programs/Python/Python37/lib/site-packages"]

from AAPI import *
from lib.dynamic_graph import DynamicGraph 
from lib.parking import Parking, ParkingGroup


def AAPILoad():
	return 0


def AAPIInit():
	# --------------------------------------------------------------------
	global parkingGroup
	parkingGroup = ParkingGroup()

	# init parameters for ALL parkings ...................................
	totIn = 0
	totOut = 0
	occupancy = 0

	parkingId = 27790

	# Parking N ..........................................................

	# centroid id of parking
	inSectionId = 27613
	outSectionId = 27614

	# IDs of labels
	occId = 27860
	maxId = 27864
	inId = 27861
	outId = 27859

	maxCapacity = 200

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
	inSectionId = 27458
	outSectionId = 27489

	# IDs of labels
	occId = 27812
	maxId = 27809
	inId = 27810
	outId = 27808

	maxCapacity = 240

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
	inSectionId = 27510
	outSectionId = 27507

	# IDs of labels
	occId = 27819
	maxId = 27816
	inId = 27817
	outId = 27815

	maxCapacity = 260

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
	inSectionId = 27608
	outSectionId = 27609

	# IDs of labels
	occId = 27826
	maxId = 27823
	inId = 27824
	outId = 27822

	maxCapacity = 210

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
	global t
	t = 0

	global graphs
	graphs = []
	for p in parkingGroup.parkings:
		graphs.append(DynamicGraph(p.title))

	return 0


def AAPISimulationReady():
	return 0

	
def AAPIManage(time, timeSta, timeTrans, acycle):
	return 0


def AAPIPostManage(time, timeSta, timeTrans, acycle):
	global filename, data, graphs
	global t
	global parkingGroup

	# Update label values of parkings
	for p, g in zip(parkingGroup.parkings, graphs):
		ANGConnSetText(p.inId,  AKIConvertFromAsciiString(str(p.totIn)))
		ANGConnSetText(p.outId, AKIConvertFromAsciiString(str(p.totOut)))
		ANGConnSetText(p.occId, AKIConvertFromAsciiString(str(p.occupancy)))
		ANGConnSetText(p.maxId, AKIConvertFromAsciiString(str(p.maxCapacity)))

		g.on_running(t, p.occupancy)
	t = t+1

	return 0


def AAPIFinish():
	return 0


def AAPIUnLoad():
	return 0

	
def AAPIPreRouteChoiceCalculation(time, timeSta):
	return 0


def AAPIEnterVehicle(idveh, idsection):
	global parkingGroup

	for p in parkingGroup.parkings:
		# Handle parking exit
		if idsection == p.outSectionId:
			p.totOut = p.totOut + 1
			p.occupancy = p.occupancy - 1
		if p.occupancy < 0: # if parking empty
			AKIRemoveVehicle(idsection, idveh)
			p.totOut = p.totOut - 1
			p.occupancy = p.occupancy + 1

	return 0


def AAPIExitVehicle(idveh, idsection):
	global parkingGroup

	for p, n in zip(parkingGroup.parkings, parkingGroup.get_nexts()):
		# Handle parking entrance
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


def AAPIVehicleStartParking (idveh, idsection, time):
	return 0
