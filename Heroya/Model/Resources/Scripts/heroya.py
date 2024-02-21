from AAPI import *

def AAPILoad():
	return 0


def AAPIInit():
	global centroidListLand, centroidListSea, sectionListLandTruck, sectionListLandTug, sectionListSea
	global truckTypePos, shipTypePos, truckList, tugList, shipList, vehicleLoadAtt, vehicleCapacityAtt, vehicleMaxLoadAtt
	global depotLoadAtt, depotCapacityAtt, depotMaxCapacityAtt, cycleCount
	global depotCurrentLoad, dockCurrentLoad, depotList, dockList

	cycleCount = 0
	depotCurrentLoad = []
	dockCurrentLoad= []
	truckList = []
	tugList = []
	shipList = []
	depotList = []
	dockList = []

	centroidListLand = [
		21734, 22115,	# north entry/exit
		22127, 22131,	# tug entry 1 / 2
		22129, 22132	# tug exit 1 / 2
		]
	centroidListSea = [14192, 14196]	# north, south
	sectionListLandTruck = [
		17817, 16281,	# entry north/south
		22046, 22007,	# pre-depot 1 / 2
		22067, -1,		# intermediate 1 / 2
		22043, 22004,	# depot 1 / 2
		17821, 16005	# exit north/south
		]
	sectionListLandTug = [
		15203, 21845,	# entry 1/2
		22056, 22138,	# pre-depot 1 / 2
		22044, 22005,	# depot 1 / 2
		22035, 22026,	# pre-dock 1 / 2
		22034, 22025,	# dock 1 / 2
		15124, 14990,	# pre-exit 1/2
		15201, 21846 	# exit 1/2
		]
	sectionListSea = [
		14619, 14465,	# entry north/south
		14473, 14478,	# pre-dock 1 / 2
		22076, 22079,	# intermediate 1 / 2
		14457, 14460,	# dock 1 / 2
		14618, 14487	# exit north/south
	]

	idTruck = ANGConnGetObjectIdByType(AKIConvertFromAsciiString("Truck"), AKIConvertFromAsciiString("GKVehicle"), False)
	truckTypePos = AKIVehGetVehTypeInternalPosition(idTruck)

	idShip = ANGConnGetObjectIdByType(AKIConvertFromAsciiString("Ship"), AKIConvertFromAsciiString("GKVehicle"), False)
	shipTypePos = AKIVehGetVehTypeInternalPosition(idShip)

	vehicleLoadAtt = ANGConnCreateAttribute(AKIConvertFromAsciiString("GKSimVehicle"),
                    AKIConvertFromAsciiString("GKSimVehicle::VehLoadInt"),
                    AKIConvertFromAsciiString("Vehicle Load"), INTEGER_TYPE, EXTERNAL)
	vehicleCapacityAtt = ANGConnCreateAttribute(AKIConvertFromAsciiString("GKSimVehicle"),
                    	AKIConvertFromAsciiString("GKSimVehicle::VehCapacityInt"),
                    	AKIConvertFromAsciiString("Vehicle Capacity"), INTEGER_TYPE, EXTERNAL)
	vehicleMaxLoadAtt = ANGConnCreateAttribute(AKIConvertFromAsciiString("GKSimVehicle"),
                    	AKIConvertFromAsciiString("GKSimVehicle::VehMaxLoadInt"),
                    	AKIConvertFromAsciiString("Vehicle max. Load"), INTEGER_TYPE, EXTERNAL)

	depotLoadAtt = ANGConnCreateAttribute(AKIConvertFromAsciiString("GKBuilding"),
                    AKIConvertFromAsciiString("GKBuilding::depotLoad"),
                    AKIConvertFromAsciiString("Depot Load"), INTEGER_TYPE, EXTERNAL)
	depotCapacityAtt = ANGConnCreateAttribute(AKIConvertFromAsciiString("GKBuilding"),
                    	AKIConvertFromAsciiString("GKBuilding::depotCapacity"),
                    	AKIConvertFromAsciiString("Depot Capacity"), INTEGER_TYPE, EXTERNAL)
	depotMaxCapacityAtt = ANGConnCreateAttribute(AKIConvertFromAsciiString("GKBuilding"),
                    	AKIConvertFromAsciiString("GKBuilding::depotMaxCapacity"),
                    	AKIConvertFromAsciiString("Depot max. Capacity"), INTEGER_TYPE, EXTERNAL)


	depotList.append(ANGConnGetObjectIdByType(AKIConvertFromAsciiString("depot_1"), AKIConvertFromAsciiString("GKBuilding"), False))
	depotCurrentLoad.append(0)
	depotList.append(ANGConnGetObjectIdByType(AKIConvertFromAsciiString("depot_2"), AKIConvertFromAsciiString("GKBuilding"), False))
	depotCurrentLoad.append(0)

	dockList.append(ANGConnGetObjectIdByType(AKIConvertFromAsciiString("dock_1"), AKIConvertFromAsciiString("GKBuilding"), False))
	dockCurrentLoad.append(0)
	dockList.append(ANGConnGetObjectIdByType(AKIConvertFromAsciiString("dock_2"), AKIConvertFromAsciiString("GKBuilding"), False))
	dockCurrentLoad.append(0)


	for depot in depotList:
		ANGConnSetAttributeValueInt(depotLoadAtt, depot, 0)
		ANGConnSetAttributeValueInt(depotCapacityAtt, depot, 2500)
		ANGConnSetAttributeValueInt(depotMaxCapacityAtt, depot, 2500)

	for dock in dockList:
		ANGConnSetAttributeValueInt(depotLoadAtt, dock, 0)
		ANGConnSetAttributeValueInt(depotCapacityAtt, dock, 100000)
		ANGConnSetAttributeValueInt(depotMaxCapacityAtt, dock, 100000)

	return 0


def AAPISimulationReady():
	return 0

	
def AAPIManage(time, timeSta, timeTrans, acycle):
	global centroidListLand, centroidListSea, sectionListLandTruck, sectionListLandTug, sectionListSea
	global truckTypePos, shipTypePos, cycleCount

	if cycleCount == 0:
		AKIEnterVehTrafficOD(sectionListLandTug[0], truckTypePos, centroidListLand[2], centroidListLand[4], True)
		AKIEnterVehTrafficOD(sectionListLandTug[1], truckTypePos, centroidListLand[3], centroidListLand[5], True)
	if cycleCount == 10:
		AKIEnterVehTrafficOD(sectionListLandTug[0], truckTypePos, centroidListLand[2], centroidListLand[4], True)
		AKIEnterVehTrafficOD(sectionListLandTug[1], truckTypePos, centroidListLand[3], centroidListLand[5], True)
	# if cycleCount == 20:
	# 	AKIEnterVehTrafficOD(sectionListLandTug[0], truckTypePos, centroidListLand[2], centroidListLand[4], True)
	# 	AKIEnterVehTrafficOD(sectionListLandTug[1], truckTypePos, centroidListLand[3], centroidListLand[5], True)
	# if cycleCount == 30:
	# 	AKIEnterVehTrafficOD(sectionListLandTug[0], truckTypePos, centroidListLand[2], centroidListLand[4], True)
	# 	AKIEnterVehTrafficOD(sectionListLandTug[1], truckTypePos, centroidListLand[3], centroidListLand[5], True)

	cycleCount = cycleCount + 1
	timeSim = round(time - timeTrans)
	AKIPrintString("Elapsed time (cylce): {}".format(timeSim))

	# if timeSim%20 == 0:
	# 	AKIEnterVehTrafficOD(sectionListLandTruck[0], truckTypePos, centroidListLand[0], centroidListLand[1], True)

	# TODO: tugmaster
	# Maybe once in init

	if timeSim%600 == 0:
		AKIEnterVehTrafficOD(sectionListSea[0], shipTypePos, centroidListSea[0], centroidListSea[1], True)
		AKIEnterVehTrafficOD(sectionListSea[1], shipTypePos, centroidListSea[1], centroidListSea[0], True)

	for vehicle in tugList:
		vehicleInfo = AKIVehTrackedGetInf(vehicle)
		if vehicleInfo.idSection == sectionListLandTug[10]:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, 22052)
		if vehicleInfo.idSection == sectionListLandTug[11]:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListLandTug[7])
	# for vehicle in truckList:
	# 	vehicleInfo = AKIVehTrackedGetInf(vehicle)
	# 	if vehicleInfo.idSection == sectionListLandTruck[4]:
	# 		AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListLandTruck[6])
	
	# for vehicle in shipList:
	# 	vehicleInfo = AKIVehTrackedGetInf(vehicle)
	# 	if vehicleInfo.idSection == sectionListSea[4]:
	# 		AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListSea[6])
	# 	if vehicleInfo.idSection == sectionListSea[5]:
	# 		AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListSea[7])

	for vehicle in truckList:
		vehicleInfo = AKIVehTrackedGetInf(vehicle)
		vehicleStaticInfo = AKIVehTrackedGetStaticInf(vehicleInfo.idVeh)
		vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)
		maxLoad = int(round(vehicleStaticInfo.length)*50)

		# depot 1
		if vehicleInfo.idSection == sectionListLandTruck[2]:
			ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, 0)
			ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad)

			ANGConnSetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG, maxLoad)
			AKIVehSetAsTracked(vehicle)
			#truckList.append(idveh)

		# depot 2
		if vehicleInfo.idSection == sectionListLandTruck[3]:
			ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, maxLoad)
			ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, 0)

			ANGConnSetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG, maxLoad)
			AKIVehSetAsTracked(vehicle)
			#truckList.append(idveh)

	for vehicle in shipList:
		vehicleInfo = AKIVehTrackedGetInf(vehicle)
		vehicleStaticInfo = AKIVehTrackedGetStaticInf(vehicleInfo.idVeh)
		vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)
		maxLoad = int(round(vehicleStaticInfo.length)*250)

		# dock 1
		if vehicleInfo.idSection == sectionListSea[2]:
			ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, maxLoad)
			ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, 0)

			ANGConnSetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG, maxLoad)
			AKIVehSetAsTracked(vehicle)
			#truckList.append(idveh)

		# dock 2
		if vehicleInfo.idSection == sectionListSea[3]:
			ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, 0)
			ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad)

			ANGConnSetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG, maxLoad)
			AKIVehSetAsTracked(vehicle)
			#truckList.append(idveh)

	for vehicle in tugList:
		vehicleInfo = AKIVehTrackedGetInf(vehicle)
		vehicleStaticInfo = AKIVehTrackedGetStaticInf(vehicleInfo.idVeh)
		vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)
		maxLoad = int(round(vehicleStaticInfo.length)*50)

		# depot/dock 1
		if vehicleInfo.idSection == sectionListLandTug[0]:
			ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, 0)
			ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad)

			ANGConnSetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG, maxLoad)
			AKIVehSetAsTracked(vehicle)
			#truckList.append(idveh)

		# depot/dock 2
		if vehicleInfo.idSection == sectionListLandTug[1]:
			ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, 0)
			ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad)

			ANGConnSetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG, maxLoad)
			AKIVehSetAsTracked(vehicle)
			#truckList.append(idveh)

	return 0


def AAPIPostManage(time, timeSta, timeTrans, acycle):
	global sectionListLandTruck, sectionListLandTug, sectionListSea
	global truckList, tugList, shipList, vehicleLoadAtt, vehicleCapacityAtt, vehicleMaxLoadAtt
	global depotLoadAtt, depotCapacityAtt, depotMaxCapacityAtt
	global depotCurrentLoad, dockCurrentLoad, depotList, dockList

	# Truck handling
	for vehicle in truckList:
		vehicleInfo = AKIVehTrackedGetInf(vehicle)
		vehicleStaticInfo = AKIVehTrackedGetStaticInf(vehicleInfo.idVeh)
		vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)

		nbVehicleDepot1 = AKIVehStateGetNbVehiclesSection(sectionListLandTruck[6], True) + AKIVehStateGetNbVehiclesSection(sectionListLandTruck[4], True)
		nbVehicleDepot2 = AKIVehStateGetNbVehiclesSection(sectionListLandTruck[7], True)

		# Direct vehicle to go to depot
		if vehicleInfo.idSection == sectionListLandTruck[2] and nbVehicleDepot1 <= 0 and depotCurrentLoad[0] >= 0:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListLandTruck[4])
		if vehicleInfo.idSection == sectionListLandTruck[3] and nbVehicleDepot2 <= 0 and depotCurrentLoad[1] < 1000:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListLandTruck[7])

		# Vehicle at depot 1 (unload depot, load vehicle)
		if vehicleInfo.idSection == sectionListLandTruck[6]:
			load = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
			maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)

			if load < maxLoad:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
				if depotCurrentLoad[0] > 50:
					load = load + 25
					depotCurrentLoad[0] = depotCurrentLoad[0] - 25
					ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, load)
					ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-load)
			else:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)

		# Vehicle at depot 2 (load depot, unload vehicle)
		if vehicleInfo.idSection == sectionListLandTruck[7]:
			load = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
			maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)

			if load > 0:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
				if depotCurrentLoad[1] < 1000:
					load = load - 25
					depotCurrentLoad[1] = depotCurrentLoad[1] + 25
					ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, load)
					ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-load)
			else:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)

	# Tug handling
	for vehicle in tugList:
		vehicleInfo = AKIVehTrackedGetInf(vehicle)
		vehicleStaticInfo = AKIVehTrackedGetStaticInf(vehicleInfo.idVeh)
		vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)

		nbVehicleDepot1 = AKIVehStateGetNbVehiclesSection(sectionListLandTug[4], True)
		nbVehicleDepot2 = AKIVehStateGetNbVehiclesSection(sectionListLandTug[5], True)

		nbVehicleDock1 = AKIVehStateGetNbVehiclesSection(sectionListLandTug[8], True)
		nbVehicleDock2 = AKIVehStateGetNbVehiclesSection(sectionListLandTug[9], True)

		# Direct vehicle to go to depot
		if vehicleInfo.idSection == sectionListLandTug[2] and nbVehicleDepot1 <= 0 and depotCurrentLoad[0] < 1000:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListLandTug[4])
		if vehicleInfo.idSection == sectionListLandTug[3] and nbVehicleDepot2 <= 0 and depotCurrentLoad[1] >= 0:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListLandTug[5])

		# Direct vehicle to go to dock
		if vehicleInfo.idSection == sectionListLandTug[6] and nbVehicleDock1 <= 0:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListLandTug[8])
		if vehicleInfo.idSection == sectionListLandTug[7] and nbVehicleDock2 <= 0:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListLandTug[9])

		

		# Vehicle at depot 1
		if vehicleInfo.idSection == sectionListLandTug[4]:
			load = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
			maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)

			if load > 0:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
				if depotCurrentLoad[0] < 1000:
					load = load - 25
					depotCurrentLoad[0] = depotCurrentLoad[0] + 25
					ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, load)
					ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-load)
			else:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)

		# Vehicle at depot 2
		if vehicleInfo.idSection == sectionListLandTug[5]:
			load = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
			maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)

			if load < maxLoad:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
				if depotCurrentLoad[1] > 100:
					load = load + 25
					depotCurrentLoad[1] = depotCurrentLoad[1] - 25
					ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, load)
					ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-load)
			else:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)

		# Vehicle at dock 1
		if vehicleInfo.idSection == sectionListLandTug[8]:
			load = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
			maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)

			if load < maxLoad:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
				if dockCurrentLoad[0] > 100:
					load = load + 25
					dockCurrentLoad[0] = dockCurrentLoad[0] - 25
					ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, load)
					ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-load)
			else:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)

		# Vehicle at dock 2
		if vehicleInfo.idSection == sectionListLandTug[9]:
			load = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
			maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)

			if load > 0:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
				if dockCurrentLoad[1] < 100000:
					load = load - 25
					dockCurrentLoad[1] = dockCurrentLoad[1] + 25
					ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, load)
					ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-load)
			else:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)
	
	# Ship handling
	for vehicle in shipList:
		vehicleInfo = AKIVehTrackedGetInf(vehicle)
		vehicleStaticInfo = AKIVehTrackedGetStaticInf(vehicleInfo.idVeh)
		vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)

		nbVehicleDock1 = AKIVehStateGetNbVehiclesSection(sectionListSea[6], True) + AKIVehStateGetNbVehiclesSection(sectionListSea[4], True)
		nbVehicleDock2 = AKIVehStateGetNbVehiclesSection(sectionListSea[7], True) + AKIVehStateGetNbVehiclesSection(sectionListSea[5], True)

		# Direct vehicle to go to dock
		if vehicleInfo.idSection == sectionListSea[2] and nbVehicleDock1 <= 0:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListSea[4])
		if vehicleInfo.idSection == sectionListSea[3] and nbVehicleDock2 <= 0:
			AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionListSea[5])

		# Vehicle at dock 1
		if vehicleInfo.idSection == sectionListSea[6]:
			load = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
			maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)

			if load > 0:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
				if dockCurrentLoad[0] < 100000:
					load = load - 100
					dockCurrentLoad[0] = dockCurrentLoad[0] + 100
					ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, load)
					ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-load)
			else:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)

		# Vehicle at dock 2
		if vehicleInfo.idSection == sectionListSea[7]:
			load = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
			maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)

			if load < maxLoad:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
				if dockCurrentLoad[1] > 200:
					load = load + 100
					dockCurrentLoad[1] = dockCurrentLoad[1] - 100
					ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, load)
					ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-load)
			else:
				AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)



	# for vehicle in vehicleList:
	# 	vehicleInfo = AKIVehTrackedGetInf(vehicle)
	# 	vehicleStaticInfo = AKIVehTrackedGetStaticInf(vehicleInfo.idVeh)
	# 	vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)

	# 	nbVehicleUnloading = AKIVehStateGetNbVehiclesSection(sectionList[4], True)
	# 	nbVehicleLoading = AKIVehStateGetNbVehiclesSection(sectionList[3], True)

	# 	if vehicleInfo.idSection == sectionList[2] and nbVehicleLoading <= 0 and depotCurrentLoad > 0:
	# 		AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionList[3])
	# 	if vehicleInfo.idSection == sectionList[7] and nbVehicleUnloading <= 0 and depotCurrentLoad < 1000:
	# 		AKIVehTrackedModifyNextSection(vehicleInfo.idVeh, sectionList[4])

	# 	if vehicleInfo.idSection == sectionList[3]:
	# 		loadLoad = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
	# 		maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)
	# 		ANGConnSetText(441, AKIConvertFromAsciiString(str(loadLoad)))
	# 		ANGConnSetText(442, AKIConvertFromAsciiString(str(round(vehicleStaticInfo.length))))
	# 		ANGConnSetText(439, AKIConvertFromAsciiString(str(round(vehicleInfo.CurrentStopTime))))
	# 		ANGConnSetText(422, AKIConvertFromAsciiString(str(depotCurrentLoad)))

	# 		if loadLoad < maxLoad:
	# 			AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
	# 			if depotCurrentLoad > 0:
	# 				loadLoad = loadLoad + 5
	# 				depotCurrentLoad = depotCurrentLoad - 5
	# 				ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, loadLoad)
	# 				ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-loadLoad)
	# 		else:
	# 			AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)

	# 	if vehicleInfo.idSection == sectionList[4]:
	# 		loadUnload = ANGConnGetAttributeValueInt(vehicleLoadAtt, vehicleANG)
	# 		maxLoad = ANGConnGetAttributeValueInt(vehicleMaxLoadAtt, vehicleANG)
	# 		ANGConnSetText(420, AKIConvertFromAsciiString(str(loadUnload)))
	# 		ANGConnSetText(418, AKIConvertFromAsciiString(str(round(vehicleStaticInfo.length))))
	# 		ANGConnSetText(414, AKIConvertFromAsciiString(str(round(vehicleInfo.CurrentStopTime))))
	# 		ANGConnSetText(422, AKIConvertFromAsciiString(str(depotCurrentLoad)))

	# 		if loadUnload > 0:
	# 			AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 0)
	# 			if depotCurrentLoad < 1000:
	# 				loadUnload = loadUnload - 5
	# 				depotCurrentLoad = depotCurrentLoad + 5
	# 				ANGConnSetAttributeValueInt(vehicleLoadAtt, vehicleANG, loadUnload)
	# 				ANGConnSetAttributeValueInt(vehicleCapacityAtt, vehicleANG, maxLoad-loadUnload)
	# 		else:
	# 			AKIVehTrackedForceSpeed(vehicleInfo.idVeh, 50)

		for i, depot in enumerate(depotList):
			# depotCurrentLoad[i] = 0 if depotCurrentLoad[i] < 0 else depotCurrentLoad[i]
			AKIPrintString("veh depot {} load: {}".format(i+1, depotCurrentLoad[i]))
			depotMaxCapacity = ANGConnGetAttributeValueInt(depotMaxCapacityAtt, depot)
			ANGConnSetAttributeValueInt(depotLoadAtt, depot, depotCurrentLoad[i])
			ANGConnSetAttributeValueInt(depotCapacityAtt, depot, depotMaxCapacity-depotCurrentLoad[i])

		for i, dock in enumerate(dockList):
			# dockCurrentLoad[i] = 0 if dockCurrentLoad[i] < 0 else dockCurrentLoad[i]
			dockMaxCapacity = ANGConnGetAttributeValueInt(depotMaxCapacityAtt, dock)
			ANGConnSetAttributeValueInt(depotLoadAtt, dock, dockCurrentLoad[i])
			ANGConnSetAttributeValueInt(depotCapacityAtt, dock, dockMaxCapacity-dockCurrentLoad[i])

	return 0


def AAPIFinish():
	return 0


def AAPIUnLoad():
	return 0

	
def AAPIPreRouteChoiceCalculation(time, timeSta):
	return 0


def AAPIEnterVehicle(idveh, idsection):
	global sectionListLandTruck, sectionListLandTug, sectionListSea
	global truckList, tugList, shipList, vehicleLoadAtt, vehicleCapacityAtt, vehicleMaxLoadAtt

	# Set every vehicle that enters the section as tracked to be able to modify their parameters afterwards
	# Trucks
	if idsection in sectionListLandTruck:
		AKIVehSetAsTracked(idveh)
		truckList.append(idveh)

	# Tug masters
	elif idsection in sectionListLandTug:
		AKIVehSetAsTracked(idveh)
		tugList.append(idveh)

	# Ship
	elif idsection in sectionListSea:
		AKIVehSetAsTracked(idveh)
		shipList.append(idveh)

	return 0


def AAPIExitVehicle(idveh, idsection):
	global sectionListLandTruck, sectionListLandTug, sectionListSea
	global truckList, tugList, shipList

	# Set every vehicle that exits the section as non-tracked
	if idsection in sectionListLandTruck:
		AKIVehSetAsNoTracked(idveh)
		truckList.remove(idveh)
	elif idsection in sectionListLandTug:
		AKIVehSetAsNoTracked(idveh)
		tugList.remove(idveh)
	elif idsection in sectionListSea:
		AKIVehSetAsNoTracked(idveh)
		shipList.remove(idveh)

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
