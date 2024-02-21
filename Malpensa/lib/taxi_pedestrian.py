"""Library providing classes to handle train stops."""
from typing import List
from random import random, choice, shuffle

from AAPI import *
import lib.attributes_lib as attr
import lib.simdata as data



class TaxiBusStop:
    """Handle logic to simulate taxi_bus stops."""

    def __init__(
        self,
        stopId,
        destroy_centroid
    ):
        """Construct taxi_bus stop object."""
        self.stopId = stopId
        self.destroy_centroid = destroy_centroid

        self.pedestriansToSpawn = []

        # to do better (with constructor's initialization)
        # gate destinations (red centroids)
        self.outPedestrianCentroidId = [27968, 28026, 28078, 28137, 28169, 28217, 28289, 29123, 
                                        28551, 28497, 28501, 28505, 28509, 28513, 28517, 28521,
                                        28769, 28773, 28777, 28781, 28785, 28789, 28793, 28797]




class TaxiBusStopGroup:
    """Intelligent Train stop list that provide functions to handle them."""

    taxi_bus_green_centroid = 16749
    taxi_bus_fast_check_in_green_centroid = 29927
    exit_centroid = 29909
    prioritized_peds_to_spawn = []

    def __init__(self):
        
        self.taxi_bus_stops: List[TaxiBusStop] = [TaxiBusStop(self.taxi_bus_green_centroid, self.exit_centroid)]
        self.pedestrians_to_be_checked = []
        self.pedestrians_to_remove = []
        self.authorized_attr = attr.create_attr(int, "authorized")

        self.removableVhcs: List[int] = []


    def remove_pedestrians(self):
        for pedestrian in self.pedestrians_to_remove:
            static_infs = AKIPedestrianGetStaticInf(pedestrian)
            orig_id = static_infs.originID
            if orig_id == self.taxi_bus_green_centroid or orig_id == self.taxi_bus_fast_check_in_green_centroid:
                static_infs.destinationID = self.exit_centroid
            AKIPedestrianSetStaticInf(static_infs)
            self.pedestrians_to_remove.remove(pedestrian)

    def add_pedestrian_to_taxi_bus_stop(self, end_centroid):
        ts = choice(self.taxi_bus_stops)
        ts.pedestriansToSpawn.append(end_centroid)

    def add_prioritized_pedestrian_to_taxi_bus_stop(self, end_centroid):
        self.prioritized_peds_to_spawn.append(end_centroid)

    def check_if_pedestrian_can_spawn(self, start_centroid, end_centroid):
        if start_centroid == self.taxi_bus_fast_check_in_green_centroid :
            if len(self.prioritized_peds_to_spawn) > 0 and end_centroid in self.prioritized_peds_to_spawn:
                self.prioritized_peds_to_spawn.remove(end_centroid)
                return True
            else:
                return False
        
        trainstops_copy = self.taxi_bus_stops.copy()
        shuffle(trainstops_copy)
        for tbs in trainstops_copy:
            tbs: TaxiBusStop
            if len(tbs.pedestriansToSpawn) > 0 and any(x in [-1, end_centroid] for x in tbs.pedestriansToSpawn):
                if -1 in tbs.pedestriansToSpawn:
                    tbs.pedestriansToSpawn.remove(-1)
                else:
                    tbs.pedestriansToSpawn.remove(end_centroid)

                return True
        
        return False
    
    def print_pedestrians_to_spawn_lists(self):
        peds_to_be_spawned = sum([len(ts.pedestriansToSpawn) for ts in self.taxi_bus_stops])
        if peds_to_be_spawned > 0:
            print(f"[TAXI_BUS] Remaining pax to be spawned: {peds_to_be_spawned}")

    def sim_step_manage(self):
        """Handle manage."""

        cur_time_in_mins = AKIGetCurrentSimulationTime()/60
        while(len(data.peds_to_spawn_bus_taxi) > 0 and cur_time_in_mins > data.peds_to_spawn_bus_taxi[0][0]):
            ped_end_centroid = data.peds_to_spawn_bus_taxi[0][1]
            ped_status = data.peds_to_spawn_bus_taxi[0][2]
            data.peds_to_spawn_bus_taxi.remove(data.peds_to_spawn_bus_taxi[0])
            print(f"[TAXI_BUS] Pedestrian going to gate {ped_end_centroid} added at {cur_time_in_mins}")
            if ped_status == "NORMAL":
                self.add_pedestrian_to_taxi_bus_stop(ped_end_centroid)
            elif ped_status == "PRIORITY":
                self.add_prioritized_pedestrian_to_taxi_bus_stop(ped_end_centroid)


        for pedestrian in self.pedestrians_to_be_checked:
            pedestrian['remaining_time'] -= AKIGetSimulationStepTime()
            if pedestrian['remaining_time'] < 0:
                # PRINT
                self.print_pedestrians_to_spawn_lists()
                # PRINT
                static_infs = AKIPedestrianGetStaticInf(pedestrian['id'])
                end_centroid = static_infs.destinationID
                origin_centroid = static_infs.originID
                if self.check_if_pedestrian_can_spawn(origin_centroid, end_centroid):
                    attr.set_as_authorized(pedestrian['id'])
                    data.passenger_start_time[pedestrian['id']] = AKIGetCurrentSimulationTime()
                else:
                    AKIVehSetAsTracked(pedestrian['id'])
                    AKIVehTrackedRemove(pedestrian['id'])
                    self.pedestrians_to_remove.append(pedestrian['id'])
                
                self.pedestrians_to_be_checked.remove(pedestrian)

        for rmv in list(self.removableVhcs):
            self.removableVhcs.remove(rmv)
            AKIVehSetAsTracked(rmv)
            AKIVehTrackedRemove(rmv)

        self.remove_pedestrians()

    
    def add_pedestrian_to_be_controlled(self, idPedestrian, end_centroid, remaining_time):
        self.pedestrians_to_be_checked.append({'id': idPedestrian, 'end_centroid': end_centroid, 'remaining_time': remaining_time})

    def api_enter_pedestrian(self, idPedestrian):
        end_centroid = AKIPedestrianGetStaticInf(idPedestrian).destinationID
        self.add_pedestrian_to_be_controlled(idPedestrian, end_centroid, remaining_time=2)
