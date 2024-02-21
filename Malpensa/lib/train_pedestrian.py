"""Library providing classes to handle train stops."""
from typing import List
from random import random, choice, shuffle

from AAPI import *
import lib.attributes_lib as attr
import lib.simdata as data



class TrainStop:
    """Handle logic to simulate train stops."""

    def __init__(
        self,
        stopId,
        destroy_centroid
    ):
        """Construct trainstop object."""
        self.stopId = stopId
        self.destroy_centroid = destroy_centroid

        self.pedestriansToSpawn = []

        # to do better (with constructor's initialization)
        # gate destinations (red centroids)
        self.outPedestrianCentroidId = [27968, 28026, 28078, 28137, 28169, 28217, 28289, 29123, 
                                        28551, 28497, 28501, 28505, 28509, 28513, 28517, 28521,
                                        28769, 28773, 28777, 28781, 28785, 28789, 28793, 28797]




class TrainStopGroup:
    """Intelligent Train stop list that provide functions to handle them."""

    trainstopsid = [29137, 26567, 26569, 26571]
    fast_check_in_stopid = 29922
    exit_centroids = [29852, 29853, 29854, 29855]
    fast_check_in_exit_centroid = 29930

    prioritized_peds_to_spawn = []

    def __init__(self):
        
        self.trainstops: List[TrainStop] = [TrainStop(ts,ec) for ts,ec in zip(self.trainstopsid,self.exit_centroids)]
        self.pedestrians_to_be_checked = []
        self.pedestrians_to_remove = []
        self.authorized_attr = attr.create_attr(int, "authorized")

        self.removableVhcs: List[int] = []


    def remove_pedestrians(self):
        for pedestrian in self.pedestrians_to_remove:
            static_infs = AKIPedestrianGetStaticInf(pedestrian)
            orig_id = static_infs.originID
            if orig_id in self.trainstopsid:
                static_infs.destinationID = self.exit_centroids[self.trainstopsid.index(orig_id)]
            if orig_id == self.fast_check_in_stopid:
                static_infs.destinationID = self.fast_check_in_exit_centroid
            AKIPedestrianSetStaticInf(static_infs)
            self.pedestrians_to_remove.remove(pedestrian)

    def add_pedestrian_to_train_stop(self, end_centroid):
        ts = choice(self.trainstops)
        ts.pedestriansToSpawn.append(end_centroid)

    def add_priority_pedestrian_to_train_stop(self, end_centroid):
        self.prioritized_peds_to_spawn.append(end_centroid)

    def check_if_pedestrian_can_spawn(self, start_centroid, end_centroid):

        if start_centroid == self.fast_check_in_stopid and len(self.prioritized_peds_to_spawn) > 0 \
                                                    and end_centroid in self.prioritized_peds_to_spawn:
            self.prioritized_peds_to_spawn.remove(end_centroid)
            return True
        
        trainstops_copy = self.trainstops.copy()
        shuffle(trainstops_copy)
        for ts in trainstops_copy:
            ts: TrainStop
            if start_centroid != self.fast_check_in_stopid and len(ts.pedestriansToSpawn) > 0 \
                                        and any(x in [-1, end_centroid] for x in ts.pedestriansToSpawn):
                if -1 in ts.pedestriansToSpawn:
                    ts.pedestriansToSpawn.remove(-1)
                else:
                    ts.pedestriansToSpawn.remove(end_centroid)

                return True
        
        return False
    
    def print_pedestrians_to_spawn_lists(self):
        peds_to_be_spawned = sum([len(ts.pedestriansToSpawn) for ts in self.trainstops])
        if peds_to_be_spawned > 0:
            print(f"[TRAIN] Remaining pax to be spawned: {peds_to_be_spawned}")

    def sim_step_manage(self):
        """Handle manage."""

        cur_time_in_mins = AKIGetCurrentSimulationTime()/60
        while(len(data.peds_to_spawn_trains) > 0 and cur_time_in_mins > data.peds_to_spawn_trains[0][0]):
            ped_end_centroid = data.peds_to_spawn_trains[0][1]
            ped_status = data.peds_to_spawn_trains[0][2]
            data.peds_to_spawn_trains.remove(data.peds_to_spawn_trains[0])
            print(f"[TRAIN] Pedestrian going to gate {ped_end_centroid} added at {cur_time_in_mins}")
            if ped_status == "NORMAL":
                self.add_pedestrian_to_train_stop(ped_end_centroid)
            elif ped_status == "PRIORITY":
                self.add_priority_pedestrian_to_train_stop(ped_end_centroid)


        for pedestrian in self.pedestrians_to_be_checked:
            pedestrian['remaining_time'] -= AKIGetSimulationStepTime()
            if pedestrian['remaining_time'] < 0:
                # PRINT
                self.print_pedestrians_to_spawn_lists()
                # PRINT
                static_infs = AKIPedestrianGetStaticInf(pedestrian['id'])
                end_centroid = static_infs.destinationID
                start_centroid = static_infs.originID
                if self.check_if_pedestrian_can_spawn(start_centroid, end_centroid):
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
