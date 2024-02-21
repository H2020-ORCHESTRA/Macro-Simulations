"""cccc."""

from AAPI import *
import typing


def track(idveh: int):
    """Tracks a given idveh car."""
    AKIVehSetAsTracked(idveh)


def untrack(idveh: int):
    """Untracks a given idveh car."""
    AKIVehSetAsNoTracked(idveh)


def create_attr(type: type, name: str) -> typing.Any:
    """Create an attribute for cars.

    :param type type: Type of the attribute to create
    :param str name: Name of the attribute to create
    :raise TypeError if type is not supported
    :return: The attribute
    :rtype: Any
    """
    if type == int:
        a_type = INTEGER_TYPE
    elif type == float:
        a_type = DOUBLE_TYPE
    elif type == str:
        a_type = STRING_TYPE
    else:
        raise TypeError(f"[Car] Attribute type {type} not supported!")

    internal_name = name.replace(" ", "")
    attr = ANGConnCreateAttribute(
        AKIConvertFromAsciiString("GKSimVehicle"),
        AKIConvertFromAsciiString(f"GKSimVehicle::{internal_name}_{type}"),
        AKIConvertFromAsciiString(name),
        a_type,
        EXTERNAL,
    )

    return attr


def set_attr(idveh: int, attr: typing.Any, attr_value: typing.Union[int, float, str]):
    """Set the value of an attribute.

    :param int idveh: ID of the vehicle for which the set an attribute
    :param Any attr: The attribute to set
    :param int|float|str attr_value: The value to set the attribute to
    :raise TypeError if type is not supported
    """
    vehicleInfo = AKIVehTrackedGetInf(idveh)
    vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)
    if type(attr_value) == int:
        ANGConnSetAttributeValueInt(attr, vehicleANG, attr_value)
    elif type(attr_value) == float:
        ANGConnSetAttributeValueDouble(attr, vehicleANG, attr_value)
    elif type(attr_value) == str:
        ANGConnSetAttributeValueStringA(attr, vehicleANG, attr_value)
    else:
        raise TypeError(f"[Car] Attribute type {type(attr_value)} not supported!")

def get_attr(idveh: int, attr: typing.Any, attr_type: type):
    """Get the value of an attribute.

    :param int idveh: ID of the vehicle for which the set an attribute
    :param Any attr: The attribute to set
    :param int|float|str attr_value: The value to set the attribute to
    :raise TypeError if type is not supported
    """
    vehicleInfo = AKIVehTrackedGetInf(idveh)
    vehicleANG = ANGConnVehGetGKSimVehicleId(vehicleInfo.idVeh)
    if attr_type == int:
        return ANGConnGetAttributeValueInt(attr, vehicleANG)
    elif attr_type == float:
        return ANGConnGetAttributeValueDouble(attr, vehicleANG)
    elif attr_type == str:
        return ANGConnGetAttributeValueStringA(attr, vehicleANG)
    else:
        raise TypeError(f"[Car] Attribute type {attr_type} not supported!")
    
def get_attr_pointer(attr_type: type, attr_name: str):
    """Get the pointer to an attribute.

    :param type attr_type: The type of the attribute
    :param str attr_name: The internal name of the attribute
    :raise TypeError if type is not supported
    :return: The pointer to the attribute
    :rtype: Any
    """
    if attr_type == (int or float or str):
        internal_name = attr_name.replace(" ", "")
        print(f"GKSimVehicle::{internal_name}_{attr_type}")
        attr_pointer = ANGConnGetAttribute(f"GKSimVehicle::{internal_name}_{attr_type}")
        # attr_pointer = ANGConnGetAttribute(f"{attr_name}")
    else:
        raise TypeError(f"Attribute type {attr_type} not supported!")

    return attr_pointer
