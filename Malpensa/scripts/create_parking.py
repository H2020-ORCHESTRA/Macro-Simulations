# TODO
#
# [ ] Add element in a group 'Parking' (create if doesn't exist ?)
# [ ] Create a polygon (color-orange, size, etc.)
# [ ] Create labels (title; Occ, Max, In, Out)
# [ ] Create texts for values (color-black/gray)


def createParkingUI(model, pos):
    labels = GKSystem.getSystem().newObject("GKText", model)
    labels.setText(QString("Occ\nMax\nIn\nOut"))
    labels.setHeight(100)
    labels.setPosition(77) # TODO

    selectParkingLayer(model, pos)


def selectParkingLayer(model, pos):
    parkingLayerName = "Parking"

    parkingLayerExists = False
    layerType = model.getType( "GKLayer" )
    for types in model.getCatalog().getUsedSubTypesFromType(layerType):
        for layer in types.values():
            if layer == parkingLayerName:
                parkingLayerExists = True
    if not parkingLayerExists: # create layer if doesn't exist
        parkingLayer = GKSystem.getSystem().newObject( "GKLayer", model )
        parkingLayer.setName(QString(parkingLayerName))
    parkingLayer.setActiveLayer()



# 'target' should be a position in the map

if target != None:
    createParkingUI(model, target)
    # Be sure that you reset the UNDO buffer after a modification that cannot be undone
    model.getCommander().addCommand(None)
else:
    model.reportError("Create ParkingUI", "This script must be launched from somwhere in a map")
