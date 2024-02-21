from AAPI import *

def AAPILoad():
    return 0

def AAPIInit():
    global gateID

    gateID = 27373

    return 0

def AAPISimulationReady():
    return 0

def AAPIManage(time, timeSta, timeTrans, acycle):
    #AKIPrintString( "AAPIManage" )
    return 0

def AAPIPostManage(time, timeSta, timeTrans, acycle):                            
    #AKIPrintString( "AAPIPostManage" )
    return 0

def AAPIFinish():
    #AKIPrintString( "AAPIFinish" )
    return 0

def AAPIUnLoad():
    #AKIPrintString( "AAPIUnLoad" )
    return 0
	
def AAPIPreRouteChoiceCalculation(time, timeSta):
    #AKIPrintString( "AAPIPreRouteChoiceCalculation" )
    return 0

def AAPIEnterVehicle(idveh, idsection):
    return 0

def AAPIExitVehicle(idveh, idsection):
    return 0

def AAPIEnterPedestrian(idPedestrian, originCentroid):
    return 0

def AAPIExitPedestrian(idPedestrian, destinationCentroid):

    if destinationCentroid == gateID:
        AKIGeneratePedestrians(27398,27399,-1,1)

    return 0

def AAPIEnterVehicleSection(idveh, idsection, atime):
    return 0

def AAPIExitVehicleSection(idveh, idsection, atime):
    return 0
    
def AAPIVehicleStartParking (idveh, idsection, time):
    return 0