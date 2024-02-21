"""Library providing classes to handle parkings."""

from collections import deque
from typing import List
from random import random, choice, gauss
from math import ceil

from AAPI import *
from typing import Dict
import platooning as pltooning
import datetime
import attributes_lib as attr
import os
import data

# ROBOT_VEH_TYPE_ID = 154
ROBOT_VEH_TYPE_ID = 23494
TRUCK_VEH_TYPE_ID = 159
# ROBOT_VEH_TYPE_POS = 2
ROBOT_VEH_TYPE_POS = 7
TRUCK_VEH_TYPE_POS = 3
MAX_TRUCKS_PLATOONING = 5
ROBOT_PLATOONING_SPEED = 5
MAX_SPEED = 80

class ParkingDatas:
    """Constants used by Parking and ParkingGroup classes."""

    PEDESTRIANS_IN_CENTROID_KEY = "in_centroid"
    PEDESTRIANS_OUT_CENTROID_KEY = "out_centroid"
    WAITING_TIME_KEY = "waiting_time"


class Parking:
    """Handle logic to simulate parkings."""

    def __init__(
        self,
        title,
        parkingId,
        enterSectionId,
        exitSectionId,
        truckSwitchSectionId,
        truckStopSectionId,
        robotSectionId,
        occId,
        maxId,
        inId,
        outId,
        robotId,
        platooning,
        maxCapacity=10,
        totIn=0,
        totOut=0,
        occupancy=0,
    ):
        """Construct parking object."""
        self.title = title
        self.parkingId = parkingId
        self.enterSectionId = enterSectionId
        self.exitSectionId = exitSectionId
        self.truckSwitchSectionId = truckSwitchSectionId
        self.truckStopSectionId = truckStopSectionId
        self.robotSectionId = robotSectionId
        self.totIn = totIn
        self.totOut = totOut
        self.occupancy = occupancy
        self.maxCapacity = maxCapacity
        self.occId = occId
        self.maxId = maxId
        self.inId = inId
        self.outId = outId
        self.robotId = robotId
        self.platooning: pltooning.Platooning = platooning

        self.robot_count = 0
        self.maxCapacity = maxCapacity
        self.tototIn = totIn
        self.tototOut = totOut
        self.occupancy = occupancy
        self.authorized_attr = attr.create_attr(int, "authorized")
        self.guided_attr = attr.create_attr(int, "guided")
        self.access_time_attr = attr.create_attr(int, "access_time")
        self.start_time_attr = attr.create_attr(int, "start_time")
        self.data_to_post = []
        self.are_cars_authorized = []
        self.vehicles_to_handle = []
        self.trucks_to_platoon = []
        self.trucks_to_switch_lane = []
        self.trucks_to_verify = []
        self.truck_to_authorize = []
        self.truck_start_waiting = {}

        self.available_cavs = 1
        self.cav_already_spawned = False
        self.tot_platooned = 0

        # data infos init
        self.id = 0
        self.timestamp = 0
        self.online = True


    def updateLabels(self):
        """Update visual information about parking."""
        ANGConnSetText(self.inId, AKIConvertFromAsciiString(str(self.totIn)))
        ANGConnSetText(self.outId, AKIConvertFromAsciiString(str(self.totOut)))
        ANGConnSetText(self.occId, AKIConvertFromAsciiString(str(self.occupancy)))
        ANGConnSetText(self.maxId, AKIConvertFromAsciiString(str(self.maxCapacity)))
        # ANGConnSetText(self.robotId, AKIConvertFromAsciiString(str(self.robot_count)))
        ANGConnSetText(self.robotId, AKIConvertFromAsciiString(str(self.available_cavs)))


    def is_vehicle_authorized(self, idveh):
        return attr.get_attr(idveh, self.authorized_attr, int) == 1
    
    def is_vehicle_guided(self, idveh):
        return attr.get_attr(idveh, self.guided_attr, int) == 1
    
    def get_vehicle_infs(self, idveh):
        return AKIVehGetInf(idveh)

    def get_vehicle_type_pos(self, idveh):
        return AKIVehGetInf(idveh).type

    def authorize_trucks(self):
        for i in range(MAX_TRUCKS_PLATOONING):
            if len(self.vehicles_to_handle) > 0:
                vehicles_to_handle_index = 0
                while(vehicles_to_handle_index < len(self.vehicles_to_handle) and self.get_vehicle_type_pos(self.vehicles_to_handle[vehicles_to_handle_index]) != TRUCK_VEH_TYPE_POS):
                    vehicles_to_handle_index += 1
                
                if vehicles_to_handle_index == len(self.vehicles_to_handle): return

                self.platooning.set_veh_as_authorized(self.vehicles_to_handle[vehicles_to_handle_index])
                self.platooning.set_vehicle_max_speed_from_static_infs(self.vehicles_to_handle[vehicles_to_handle_index], MAX_SPEED)
                self.vehicles_to_handle.remove(self.vehicles_to_handle[vehicles_to_handle_index])
    

    def enter_vehicle_section(self, idsection, idveh):
        cur_sim_time_min = AKIGetCurrentSimulationTime()/60
        if idsection == self.enterSectionId:
            data.entry_times.append(cur_sim_time_min)
            attr.track(idveh)
            if self.is_vehicle_guided(idveh):   # TEST!!!!!!!
                self.vehicles_to_handle.append(idveh)

        if idsection == self.truckSwitchSectionId:
            if self.get_vehicle_type_pos(idveh) == TRUCK_VEH_TYPE_POS:
                self.truck_start_waiting[idveh] = cur_sim_time_min
                AKIVehSetAsTracked(idveh)
                # self.platooning.set_vehicle_destination_from_static_infs(idveh, None)
                self.totIn += 1
                self.occupancy += 1
                # if random() > 0.3:
                if self.is_vehicle_guided(idveh):
                    AKIVehTrackedModifyLane(idveh, -1)
                    self.trucks_to_platoon.append(idveh)
                    self.tot_platooned += 1
                else:
                    attr.set_attr(idveh, self.authorized_attr, 1)
                    self.truck_to_authorize.append(idveh)

        if idsection == self.truckStopSectionId: # and attr.get_attr(idveh, self.authorized_attr, int) == 0:
            if not self.is_vehicle_authorized(idveh) and self.get_vehicle_type_pos(idveh) == TRUCK_VEH_TYPE_POS:
                self.platooning.set_vehicle_max_speed_from_static_infs(idveh, 0)
                pass
            else:
                self.truck_to_authorize.remove(idveh)

        if idsection == self.robotSectionId:
            if self.get_vehicle_type_pos(idveh) == ROBOT_VEH_TYPE_POS:
                self.robot_count += 1
                self.cav_already_spawned = False

        if idsection == self.exitSectionId:
            if self.get_vehicle_type_pos(idveh) == ROBOT_VEH_TYPE_POS:
                self.robot_count -= 1
                self.platooning.set_vehicle_max_speed_from_static_infs(idveh, 15)
                for index, truck in enumerate(self.trucks_to_platoon):
                    attr.set_attr(truck, self.authorized_attr, 1)
                    self.trucks_to_switch_lane.append((truck, 2*index))
                
                self.trucks_to_platoon = []

            elif self.get_vehicle_type_pos(idveh) == TRUCK_VEH_TYPE_POS:
                self.totOut += 1
                self.occupancy -=1
                self.trucks_to_verify.remove(idveh)
            

    def exit_vehicle_section(self, idsection, idveh):
        if idsection == self.exitSectionId:
            if self.get_vehicle_type_pos(idveh) == TRUCK_VEH_TYPE_POS:
                cur_sim_time_min = AKIGetCurrentSimulationTime()/60
                waiting_time = cur_sim_time_min - self.truck_start_waiting[idveh]
                del self.truck_start_waiting[idveh]
                data.truck_waiting_times.append(waiting_time)
        if idsection == 17821:
            if self.get_vehicle_type_pos(idveh) == ROBOT_VEH_TYPE_POS:
                self.available_cavs += 1


    def redirect_vehicles(self):
        """Redirect a vehicle in its correct next_section if the vehicle entered the parking."""
        for vehicle in self.vehicles_to_handle:
            veh_infs = self.get_vehicle_infs(vehicle)
            if veh_infs.idSection == self.enterSectionId:
                if self.get_vehicle_type_pos(vehicle) == TRUCK_VEH_TYPE_POS:
                    AKIVehTrackedModifyNextSection(vehicle, self.truckSwitchSectionId)
                elif self.get_vehicle_type_pos(vehicle) == ROBOT_VEH_TYPE_POS:
                    if self.is_vehicle_authorized(vehicle):
                        AKIVehTrackedModifyNextSection(vehicle, self.truckSwitchSectionId)
                    else:
                        AKIVehTrackedModifyNextSection(vehicle, self.robotSectionId)


    def manage_step(self):
        #spawn trucks
        cur_time_in_mins = AKIGetCurrentSimulationTime()/60
        # while(len(data.trucks_to_spawn) > 0 and cur_time_in_mins > data.trucks_to_spawn[0][2]):
        if len(data.trucks_to_spawn) > 0 and cur_time_in_mins > data.trucks_to_spawn[0][2]:
            end_centroid = int(data.trucks_to_spawn[0][0])
            access_time = int(data.trucks_to_spawn[0][1])
            truck_guided = int(data.trucks_to_spawn[0][3])

            veh_id = AKIEnterVehTrafficOD(self.enterSectionId, TRUCK_VEH_TYPE_POS, 21734, end_centroid, 1)
            # print(f"{veh_id} / {data.trucks_to_spawn[0]}")
            if veh_id >= 0:
                data.trucks_to_spawn.remove(data.trucks_to_spawn[0])
                print(f"{'Guided' if truck_guided else 'Unguided'} truck with id {veh_id} going to depot {end_centroid} added at {cur_time_in_mins}")
                attr.set_attr(veh_id, self.access_time_attr, access_time)
                attr.set_attr(veh_id, self.start_time_attr, cur_time_in_mins)
                if truck_guided:
                    attr.set_attr(veh_id, self.guided_attr, 1)
            elif veh_id < -7004:
                data.trucks_to_spawn.remove(data.trucks_to_spawn[0])
                print(f"Error {veh_id}: Discarded {'guided' if truck_guided else 'unguided'} truck to {end_centroid}")
            else:
                print(f"Error {veh_id}: Continue and retry")
                pass

        # make trucks leave the waiting zone with some delay for each consecutive truck
        for index, (truckId, remaining_time) in enumerate(self.trucks_to_switch_lane):
            new_remaining_time = remaining_time - AKIGetSimulationStepTime()
            if new_remaining_time > 0:
                self.trucks_to_switch_lane[index] = (truckId, new_remaining_time)
            else:
                self.trucks_to_switch_lane.remove((truckId, remaining_time))
                self.platooning.set_vehicle_max_speed_from_static_infs(truckId, 100)
                self.trucks_to_verify.append(truckId)
                AKIVehTrackedModifyLane(truckId, 1)

        # verify if the authorized trucks are turning back to their lane and switch again if it's the case
        for truckId in self.trucks_to_verify:
            if AKIVehGetInf(truckId).numberLane == 1:
                AKIVehTrackedModifyLane(truckId, 1)
            # AKIVehTrackedModifyLane(truckId, -1)

        did_veh_spawn, veh_type_pos = self.platooning.manage_step()
        if did_veh_spawn:
            if veh_type_pos == ROBOT_VEH_TYPE_POS:
                self.robot_count -= 1
            elif veh_type_pos == TRUCK_VEH_TYPE_POS:
                self.occupancy -= 1
                self.totOut += 1

        for truck in self.truck_to_authorize:
            AKIVehTrackedModifyLane(truck, 1)

        if self.trucks_to_platoon and self.available_cavs > 0 and not self.cav_already_spawned:
            veh_id = AKIEnterVehTrafficOD(self.enterSectionId, ROBOT_VEH_TYPE_POS, 21734, 22115, 1)
            if veh_id > 0:
                self.available_cavs -= 1
                self.cav_already_spawned = True

        # for vehicle in self.are_cars_authorized:
        #     vehicle['remaining_time'] -= AKIGetSimulationStepTime()
        #     if vehicle['remaining_time'] < 0:
        #         if not self.is_vehicle_authorized(vehicle['idveh']):

        #             veh_type_pos = AKIVehGetInf(vehicle['idveh']).type
        #             if veh_type_pos == ROBOT_VEH_TYPE_POS:
        #                 self.robot_count += 1
        #             elif veh_type_pos == TRUCK_VEH_TYPE_POS:
        #                 self.totOut -= 1
        #                 self.occupancy += 1

        #             AKIVehSetAsTracked(vehicle['idveh'])
        #             AKIVehTrackedRemove(vehicle['idveh'])

        #         self.are_cars_authorized.remove(vehicle)


    def post_manage_step(self):
        self.updateLabels()
        # self.redirect_vehicles()  # TEST!!!!!!!

    def add_vehicle_to_be_controlled(self, idveh, remaining_time):
        self.are_cars_authorized.append({'idveh': idveh, 'remaining_time': remaining_time})

    def shouldDoPlatooning(self):
        return self.robot_count > 0 and self.occupancy >= MAX_TRUCKS_PLATOONING

    def handlePlatooning(self):
        if self.shouldDoPlatooning():
            self.platooning.do_platooning()

    def parkCar(self, idsection, idveh):
        """Park a car and spawn pedestrians if there is enough space in the parking.

        :param idsection: identifier of the last section the car was on before unspawning
        :type idsection: integer

        :param num_of_pedestrian: number of pedestrians that is dropped when the car is succesfully parked
        :type num_of_pedestrian: integer
        """
        # if idsection == self.enterSectionId:
        #     veh_type_pos = AKIVehGetInf(idveh).type
        #     #print(f"veh_type: {veh_type}")
        #     if veh_type_pos == ROBOT_VEH_TYPE_POS or veh_type_pos == TRUCK_VEH_TYPE_POS:
        #         if veh_type_pos == ROBOT_VEH_TYPE_POS:
        #             self.robot_count += 1
        #             self.store_data()
        #         elif veh_type_pos == TRUCK_VEH_TYPE_POS:
        #             if self.occupancy >= self.maxCapacity:
        #                 return False
        #             self.totIn += 1
        #             self.occupancy += 1    
        #             self.store_data()
                
        #         self.handlePlatooning()
        return True

    def unparkCar(self, idsection, idveh):
        """Unpark a car if there is at least one car in the parking.

        :param idsection: identifier of the section the car spawned on
        :type idsection: integer
        """
        # if idsection == self.exitSectionId:
        #     veh_type_pos = AKIVehGetInf(idveh).type

        #     if veh_type_pos == ROBOT_VEH_TYPE_POS:
        #         if self.robot_count == 0:
        #             return False, 0
        #         self.robot_count -= 1
        #         self.add_vehicle_to_be_controlled(idveh, AKIGetSimulationStepTime()/3)

        #     elif veh_type_pos == TRUCK_VEH_TYPE_POS:
        #         if self.occupancy == 0:
        #             return False, 0
        #         self.totOut += 1
        #         self.occupancy -= 1
        #         self.add_vehicle_to_be_controlled(idveh, AKIGetSimulationStepTime()/3)
                
        #     else:
        #         return False, 0

        #     self.store_data()

        return True, 0


    def generate_waiting_time(self, mean=600, std=20):
        """Return a float corresponding to waiting time.

        This integer is randomly choosen from a gaussian distribution,
        the mean and standard deviation can be given as function parameter.

        :param mean: The mean of the gaussian distribution, also called mu.
        :type mean: number

        :param std: The standard deviation of the gaussian distribution, also called sigma.
        :type std: number
        """
        return gauss(mean, std)

    simulation_date = datetime.datetime(2023, 5, 23, 8, 0)
    originelle_date = datetime.datetime(1970, 1, 1)

    delta_date = simulation_date - originelle_date

    sim_date_offset = int(delta_date.total_seconds())

    def store_data(self):
        """Store parking data in order to send them to the web API at the end of simulation."""
        if self.online:
            data = {
                "timestamp_uid": self.timestamp,
                "value": self.occupancy,
                "robot_count": self.robot_count,
                "timestamp": str(self.sim_date_offset + AKIGetCurrentSimulationTime()),
            }
            self.data_to_post.append(data)

    def set_offline(self):
        """Set the online status to false, which means that the simulation won't post data to the web API."""
        self.online = False


class ParkingGroup:
    """Intelligent Parking list that provide functions to handle them."""

    def __init__(self, parkings: List[Parking] = []):
        """Construct parking object.

        :param parkings: list of Parking elements forming the ParkingGroup
        """
        self.parkings: List[Parking] = parkings
        self.init_parking_datas()

        # removableVhcs contains a list of all vehicle IDs that are to be removed.
        self.removableVhcs: List[int] = []
        self.testList: List[int] = []

    def init_parking_datas(self) -> None:
        """Initialize the parkings with the latest parking configuration added in the web API."""
        for p in self.parkings:
            parking: Parking = p

            data = None

            if data is not None:
                sim_list = data["sim_inputs"]

                most_recent_sim: Dict = {}
                most_recent_timestamp: datetime.datetime = datetime.datetime.fromtimestamp(0)
                for sim in sim_list:
                    cur_timestamp = datetime.datetime.strptime(sim["timestamp"], "%Y-%m-%dT%H:%M:%S.%f")
                    if (
                        most_recent_timestamp == datetime.datetime.fromtimestamp(0)
                        or most_recent_timestamp < cur_timestamp
                    ):
                        most_recent_timestamp = cur_timestamp
                        most_recent_sim = sim

                parking.maxCapacity = most_recent_sim["max_capacity"]
                parking.occupancy = most_recent_sim["default_occupancy"]
                parking.id = most_recent_sim["id"]
                parking.timestamp = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())

    def sim_step_manage(self):
        """Handle manage."""
        for p in self.parkings:
            p.manage_step()

        for rmv in list(self.removableVhcs):
            self.removableVhcs.remove(rmv)
            AKIVehSetAsTracked(rmv)
            AKIVehTrackedRemove(rmv)

    def sim_step_post_manage(self):
        """Handle post manage."""
        for p in self.parkings:
            p.updateLabels()

    def sim_step_finish(self):
        """Handle sim wrap-up"""
        # tot_trucks_in = 0
        # tot_tucks_platooned = 0

        for p in self.parkings:
            data.tot_trucks_in += p.totIn
            # tot_tucks_platooned += p.tot_platooned

        # cwd = os.getcwd()
        # print(f"Working dir: {cwd}")
        # f = open("./kpi.txt", "w")
        # f.write(f"Total trucks in: {tot_trucks_in}\n")
        # f.write(f"Total trucks platooned: {tot_tucks_platooned}\n")
        # f.close()

    def api_enter_vehicle(self, idsection: int, idveh: int):
        """Handle parking exit.

        :param idsection: Id of the section from where the vehicle left the parking
        :type idsection: int

        :param idveh: Id of the vehicule
        :type idveh: int
        """
        for p in self.parkings:
            successful, amountOfPedestrians = p.unparkCar(idsection, idveh)
            if not successful:
                self.removableVhcs.append(idveh)

    def api_exit_vehicle(self, idsection: int, idveh: int):
        """Handle parking entrance.

        :param idsection: Id of the section from where the vehicle entered the parking
        :type idsection: int

        :param idveh: Id of the vehicule
        :type idveh: int
        """
        for p, n in zip(self.parkings, self.get_nexts()):
            successful = p.parkCar(idsection, idveh)
            if not successful:
                AKIEnterVehTrafficOD(p.exitSectionId, 0, p.parkingId, n.parkingId, 0)
                

    def api_enter_vehicle_section(self, idsection: int, idveh: int):
        for p in self.parkings:
            p.enter_vehicle_section(idsection, idveh)

    def api_exit_vehicle_section(self, idsection: int, idveh: int):
        for p in self.parkings:
            p.exit_vehicle_section(idsection, idveh)

    def get_nexts(self):
        """Return the next destination for parking if current is full.

        Currently, returns the next one in the parking list.

        E.g. parkings = [ 1, 2, 3 ]
             nexts =    [ 2, 3, 1 ]

             So that if a car goes into parking 3 full, it then tries
             to go into parking 1.
        """
        nexts = deque(self.parkings)
        nexts.rotate(-1)

        return nexts
