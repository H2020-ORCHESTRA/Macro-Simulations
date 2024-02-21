"""Library providing class to handle platooning."""

from collections import deque
from random import random, choice, gauss
from math import ceil
from helpers import *

from AAPI import *

import typing
import parking as pk
import attributes_lib as attr
import utils
import data


# ROBOT_VEH_TYPE_POS = 2
ROBOT_VEH_TYPE_POS = 7
TRUCK_VEH_TYPE_POS = 3

class Platooning:
    """Handle logic to simulate platooning."""

    def __init__(
        self,
        section_id,
        start_centroid,
        end_centroid,
        end_section,
        depot_centroids,
        depot_infos,
        amount_of_trucks,
    ):
        """Construct parking object."""
        self.section_id = section_id
        self.start_centroid = start_centroid
        self.end_centroid = end_centroid
        self.end_section = end_section
        self.depot_centroids = depot_centroids
        self.depot_infos = depot_infos
        self.amount_of_trucks = amount_of_trucks

        self.dest_depot_attr = attr.create_attr(int, "dest_depot")
        self.depots_attr = attr.create_attr(str, "depots")
        self.add_pilot_car_attr = attr.create_attr(int, "add_pilot_car")
        self.start_time_attr = attr.create_attr(int, "start_time")

        self.vehicles_to_spawn = []
        self.vehicles_to_respawn = []
        self.additional_pilot_cars = 0


    def spawn_vehicle_if_possible(self):
        if len(self.vehicles_to_spawn) > 0:
            # vehicle = self.vehicles_to_spawn[0]
            # vehicle_type_pos = vehicle[0]
            # start_centroid = vehicle[1]

            # veh_id = AKIEnterVehTrafficOD(self.section_id, vehicle_type_pos, start_centroid, self.depot_centroids[0], 1)

            # attr.set_attr(veh_id, self.dest_depot_attr, choice(self.depot_centroids))
            # attr.set_attr(veh_id, self.depots_attr, utils.list_to_string(self.depot_centroids[1:]))
            
            vehicle_type_pos = self.vehicles_to_spawn[0]
            veh_id = AKIEnterVehTrafficOD(self.section_id, vehicle_type_pos, self.start_centroid, choice(self.depot_centroids), 1)
            if veh_id < 0:
                return False, vehicle_type_pos
            
            # self.vehicles_to_spawn.remove(vehicle)
            self.vehicles_to_spawn.remove(vehicle_type_pos)
            if vehicle_type_pos == pk.ROBOT_VEH_TYPE_POS:
                self.set_vehicle_max_speed_from_static_infs(veh_id, 5)
                # self.set_vehicle_destination_from_static_infs(veh_id, self.depot_centroids[0])
                self.set_vehicle_destination_from_static_infs(veh_id, self.end_centroid)
                attr.set_attr(veh_id, self.add_pilot_car_attr, 0)

            self.set_veh_as_authorized(veh_id)
            return True, vehicle_type_pos
        
        return False, 0
    

    def respawn_vehicle_if_possible(self):
        if len(self.vehicles_to_respawn) > 0:
            vehicle = self.vehicles_to_respawn[0]
            vehicle_type_pos = vehicle[0]
            dest_depot = vehicle[1]
            depots = vehicle[2]
            in_section = vehicle[3]
            start_depot = vehicle[4]

            if len(depots):
                veh_id = AKIEnterVehTrafficOD(in_section, vehicle_type_pos, start_depot, depots[0], 1)
                attr.set_attr(veh_id, self.depots_attr, utils.list_to_string(depots[1:]))
            else:
                veh_id = AKIEnterVehTrafficOD(in_section, vehicle_type_pos, start_depot, self.end_centroid, 1)

            attr.set_attr(veh_id, self.dest_depot_attr, dest_depot)
            
            if veh_id < 0:
                return False, vehicle_type_pos
            
            self.vehicles_to_respawn.remove(vehicle)
            if vehicle_type_pos == pk.ROBOT_VEH_TYPE_POS:
                self.set_vehicle_max_speed_from_static_infs(veh_id, 5)
                attr.set_attr(veh_id, self.dest_depot_attr, self.end_centroid)
                attr.set_attr(veh_id, self.add_pilot_car_attr, vehicle[5])

            self.set_veh_as_authorized(veh_id)
            return True, vehicle_type_pos
        
        return False, 0
    
    
    def spawn_additional_pilot_car_if_possible(self):
        if self.additional_pilot_cars > 0:
            veh_id = AKIEnterVehTrafficOD(self.section_id, ROBOT_VEH_TYPE_POS, self.start_centroid, self.depot_centroids[0], 1)

            if veh_id < 0:
                return False, ROBOT_VEH_TYPE_POS
            
            print(f"Spawned additional pilot car!")
            self.set_vehicle_max_speed_from_static_infs(veh_id, 5)
            attr.set_attr(veh_id, self.dest_depot_attr, self.end_centroid)
            attr.set_attr(veh_id, self.depots_attr, utils.list_to_string(self.depot_centroids[1:]))
            attr.set_attr(veh_id, self.add_pilot_car_attr, 1)
            
            self.additional_pilot_cars -= 1
            return True, ROBOT_VEH_TYPE_POS
        
        return False, ROBOT_VEH_TYPE_POS


    def manage_step(self):
        _, _ = self.respawn_vehicle_if_possible()
        success, veh_type_pos = self.spawn_vehicle_if_possible()
        _, _ = self.spawn_additional_pilot_car_if_possible()
        return success, veh_type_pos


    def set_veh_as_authorized(self, veh_id):
        attr.track(veh_id)
        authorized_attr = attr.create_attr(int, "authorized")
        attr.set_attr(veh_id, authorized_attr, 1)


    def set_vehicle_max_speed_from_static_infs(self, idveh, desired_speed):
        static_infs = AKIVehGetStaticInf(idveh)
        static_infs.maxDesiredSpeed = desired_speed
        ret_val = AKIVehSetStaticInf(idveh, static_infs)


    def set_vehicle_destination_from_static_infs(self, idveh, destination):
        static_infs = AKIVehGetStaticInf(idveh)
        if destination:
            static_infs.centroidDest = destination
        else:
            static_infs.centroidDest = choice(self.depot_centroids)
        ret_val = AKIVehSetStaticInf(idveh, static_infs)


    def get_vehicle_type_pos_from_static_infs(self, idveh):
        static_infs = AKIVehGetStaticInf(idveh)
        veh_type_pos = static_infs.type
        return veh_type_pos


    def do_platooning(self):
        # self.vehicles_to_spawn.append((pk.ROBOT_VEH_TYPE_POS, self.start_centroid))
        # for i in range(self.amount_of_trucks):
        #     self.vehicles_to_spawn.append((pk.TRUCK_VEH_TYPE_POS, self.start_centroid))
        self.vehicles_to_spawn.append(pk.ROBOT_VEH_TYPE_POS)
        for i in range(self.amount_of_trucks):
            self.vehicles_to_spawn.append(pk.TRUCK_VEH_TYPE_POS)


    def depot_entry(self, veh_id, depot_section):
        if depot_section in list(self.depot_infos.keys()):
            # dest_depot = attr.get_attr(veh_id, self.dest_depot_attr, int)
            # depots = utils.string_to_list(attr.get_attr(veh_id, self.depots_attr, str))
            # current_depot = self.depot_infos[depot_section][0]
            # depot_in_section = self.depot_infos[depot_section][1]
            # veh_type_pos = self.get_vehicle_type_pos_from_static_infs(veh_id)

            # if dest_depot != current_depot:
            #     if veh_type_pos == ROBOT_VEH_TYPE_POS:
            #         add_pilot_car = attr.get_attr(veh_id, self.add_pilot_car_attr, int)
            #         self.vehicles_to_respawn.append((veh_type_pos, dest_depot, depots, depot_in_section, current_depot, add_pilot_car))
            #     else:
            #         self.vehicles_to_respawn.append((veh_type_pos, dest_depot, depots, depot_in_section, current_depot, 0))

            # self.vehicles_to_respawn.append((veh_type_pos, dest_depot, depots, depot_in_section, current_depot, 0))
            pass

    def sim_exit(self, idsection, idveh):
        if idsection == self.end_section and AKIVehGetInf(idveh).type == TRUCK_VEH_TYPE_POS:
            cur_time_in_mins = AKIGetCurrentSimulationTime()/60
            start_time = attr.get_attr(idveh, self.start_time_attr, int)
            time_inside_park = cur_time_in_mins - start_time
            print(f"{cur_time_in_mins} / {start_time} / {time_inside_park}")
            data.truck_times_inside_park.append(time_inside_park)
            data.exit_times.append(cur_time_in_mins)
            pass
