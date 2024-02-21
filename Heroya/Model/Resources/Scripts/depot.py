"""Library providing classes to handle parkings."""

from typing import List
from random import random, choice, gauss, randint
from math import ceil

from AAPI import *
import typing
import attributes_lib as attr
import platooning

# ROBOT_VEH_TYPE_ID = 154
ROBOT_VEH_TYPE_ID = 23494
TRUCK_VEH_TYPE_ID = 159
# ROBOT_VEH_TYPE_POS = 2
ROBOT_VEH_TYPE_POS = 7
TRUCK_VEH_TYPE_POS = 3
MAX_TRUCKS_PLATOONING = 5


class Depot:
    """Handle logic to simulate depots."""

    def __init__(
        self,
        title,
        depotId,
        inSectionId,
        outSectionId,
        unloadind_id,
        ready_id
    ):
        """Construct depot object."""
        self.title: str = title
        self.depotId: int = depotId
        self.inSectionId: int = inSectionId
        self.outSectionId: int = outSectionId
        self.unloading_id: int = unloadind_id
        self.ready_id: int =  ready_id

        self.unloading: int = 0
        self.ready: int = 0

        self.trucks_unloading: List[List[int, float]] = [] # Truck id, timestamp when ready
        self.trucks_ready: List[int] = [] # Truck id
        self.tmp_trucks_ready_count: int = 0
        self.trucks_to_spawn: List[int] = []
        self.pilot_cars_exiting: List[int] = []

        self.exit_centroid: int = 22115

        self.dest_depot_attr = attr.create_attr(int, "dest_depot")
        self.add_pilot_car_attr = attr.create_attr(int, "add_pilot_car")
        self.access_time_attr = attr.create_attr(int, "access_time")
        self.start_time_attr = attr.create_attr(int, "start_time")

    def updateLabels(self):
        """Update visual information about depot."""
        # ANGConnSetText(self.unloading_id, AKIConvertFromAsciiString(str(self.unloading)))
        # ANGConnSetText(self.ready_id, AKIConvertFromAsciiString(str(self.ready)))
        ANGConnSetText(self.unloading_id, AKIConvertFromAsciiString(str(len(self.trucks_unloading))))
        ANGConnSetText(self.ready_id, AKIConvertFromAsciiString(str(len(self.trucks_ready))))

    def spawn_vehicle_if_possible(self):
        # if len(self.trucks_to_spawn) > 0:
        #     vehicle = self.trucks_to_spawn[0]
        #     veh_id = AKIEnterVehTrafficOD(self.outSectionId, TRUCK_VEH_TYPE_POS, self.depotId, self.exit_centroid, 1)
            
        #     if veh_id < 0:
        #         return False, None
        #     else:
        #         attr.set_attr(veh_id, self.dest_depot_attr, self.exit_centroid)
        #         self.trucks_to_spawn.remove(vehicle)
        #         # self.tmp_trucks_ready_count -= 1
        #         self.set_veh_as_authorized(veh_id)

        #     return True, TRUCK_VEH_TYPE_POS
        
        if len(self.trucks_ready) > 0:
            vehicle = self.trucks_ready[0]
            veh_id = AKIEnterVehTrafficOD(self.outSectionId, TRUCK_VEH_TYPE_POS, self.depotId, self.exit_centroid, 1)
            
            if veh_id < 0:
                return False, None
            else:
                attr.set_attr(veh_id, self.dest_depot_attr, self.exit_centroid)
                attr.set_attr(veh_id, self.start_time_attr, vehicle[2])
                print(f"{vehicle[2]}")
                self.trucks_ready.remove(vehicle)
                # self.tmp_trucks_ready_count -= 1
                self.set_veh_as_authorized(veh_id)

            return True, TRUCK_VEH_TYPE_POS
        
        return False, None


    def manage_step(self):
        for vehicle in self.trucks_unloading:
            vehicle[1] -= AKIGetSimulationStepTime()
            if vehicle[1] <= 0:
                self.trucks_ready.append(vehicle)
                self.tmp_trucks_ready_count += 1
                self.trucks_unloading.remove(vehicle)

        # for car in self.pilot_cars_exiting:
        #     add_pilot_car = attr.get_attr(car, self.add_pilot_car_attr, int)
        #     print(f"Is it an additional pilot car? : {True if add_pilot_car else False}")
        #     if add_pilot_car:
        #         print(f"additional pilot left depot")
        #         while len(self.trucks_ready):
        #             self.trucks_to_spawn.append(self.trucks_ready.pop(0))

        success, veh_type_pos = self.spawn_vehicle_if_possible()
        return success, veh_type_pos

    def set_veh_as_authorized(self, veh_id):
        attr.track(veh_id)
        authorized_attr = attr.create_attr(int, "authorized")
        attr.set_attr(veh_id, authorized_attr, 1)

    def get_vehicle_type_pos_from_static_infs(self, idveh):
        static_infs = AKIVehGetStaticInf(idveh)
        veh_type_pos = static_infs.type
        return veh_type_pos

    def parkCar(self, idsection, idveh):
        """Park a car and spawn pedestrians if there is enough space in the parking.

        :param idsection: identifier of the last section the car was on before unspawning
        :type idsection: integer

        :param num_of_pedestrian: number of pedestrians that is dropped when the car is succesfully parked
        :type num_of_pedestrian: integer
        """
        if idsection == self.inSectionId and AKIVehGetInf(idveh).type == TRUCK_VEH_TYPE_POS:
            # dest_depot = attr.get_attr(idveh, self.dest_depot_attr, int)
            # if dest_depot == self.depotId:
            #     # self.unloading += 1
            #     # add truck to list with timestamp
            #     self.trucks_unloading.append([idveh, AKIGetSimulationStepTime() + randint(60, 300)])
            # self.trucks_unloading.append([idveh, AKIGetSimulationStepTime() + randint(60, 300)])
            # print(f"{attr.get_attr(idveh, self.start_time_attr, int)}")
            self.trucks_unloading.append([idveh, attr.get_attr(idveh, self.access_time_attr, int), attr.get_attr(idveh, self.start_time_attr, int)])


    def unparkCar(self, idsection, idveh):
        """Unpark a car if there is at least one car in the parking.

        :param idsection: identifier of the section the car spawned on
        :type idsection: integer
        """
        if idsection == self.outSectionId:
            # veh_type_pos = self.get_vehicle_type_pos_from_static_infs(idveh)
            # if veh_type_pos == ROBOT_VEH_TYPE_POS:
            #     # add to list, then later traverse list to check if additonal pilot car or not
            #     self.pilot_cars_exiting.append(idveh)

            #     # add_pilot_car = attr.get_attr(idveh, self.add_pilot_car_attr, int)
            #     # # print(f"Is it an additional pilot car? : {True if add_pilot_car else False}")
            #     # if add_pilot_car:
            #     #     print(f"additional pilot left depot")
            #     #     while len(self.trucks_ready):
            #     #         self.trucks_to_spawn.append(self.trucks_ready.pop(0))
            pass


class DepotGroup:
    """Intelligent depot list that provide functions to handle them."""

    def __init__(
        self,
        platoon,
        depots: List[Depot] = []
    ):
        """Construct depot object.

        :param depots: list of depot elements forming the ParkingGroup
        """
        self.depots: List[Depot] = depots
        self.platoon: platooning.Platooning = platoon

        self.tot_trucks_ready: int = 0

    def sim_step_manage(self):
        """Handle manage."""
        for p in self.depots:
            p.manage_step()

    def sim_step_post_manage(self):
        """Handle post manage."""
        for p in self.depots:
            p.updateLabels()
            self.tot_trucks_ready += p.tmp_trucks_ready_count
            p.tmp_trucks_ready_count = 0

        # pilot_cars_to_spawn = self.tot_trucks_ready//5
        # if pilot_cars_to_spawn > 0:
        #     self.platoon.additional_pilot_cars += pilot_cars_to_spawn
        #     self.tot_trucks_ready -= pilot_cars_to_spawn*5


    def api_enter_vehicle(self, idsection: int, idveh: int):
        """Handle depot exit.

        :param idsection: Id of the section from where the vehicle left the parking
        :type idsection: int

        :param idveh: Id of the vehicule
        :type idveh: int
        """
        for p in self.depots:
            p.unparkCar(idsection, idveh)

    def api_exit_vehicle(self, idsection: int, idveh: int):
        """Handle depot entrance.

        :param idsection: Id of the section from where the vehicle entered the depot
        :type idsection: int

        :param idveh: Id of the vehicle
        :type idveh: int
        """
        for p in self.depots:
            p.parkCar(idsection, idveh)
