"""Library providing classes to handle parkings."""

from collections import deque
from typing import List
from random import random, choice, gauss, shuffle
from math import ceil

from AAPI import *
from typing import Dict
import datetime
import csv
import lib.attributes_lib as attr
import lib.simdata as data

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
        inSectionId,
        outSectionId,
        occId,
        maxId,
        inId,
        outId,
        maxCapacity=10,
        totIn=0,
        totOut=0,
        occupancy=0,
        pedestrianCount=0,
        maxPedestrians=5,
    ):
        """Construct parking object."""
        self.title = title
        self.parkingId = parkingId
        self.inSectionId = inSectionId
        self.outSectionId = outSectionId
        self.totIn = totIn
        self.totOut = totOut
        self.occupancy = occupancy
        self.maxCapacity = maxCapacity
        self.occId = occId
        self.maxId = maxId
        self.inId = inId
        self.outId = outId

        self.pedestrianCount = pedestrianCount
        self.pedestriansToSpawnCount = []
        self.maxPedestrians = maxPedestrians
        self.data_to_post = []

        # data infos init
        self.id = 0
        self.timestamp = 0

        # to do better (with constructor's initialization)
        self.inPedestrianCentroidId = [16747]
        self.outPedestrianCentroidId = [27968, 28026, 28078, 28137, 28169, 28217, 28289, 29123, 
                                        28551, 28497, 28501, 28505, 28509, 28513, 28517, 28521,
                                        28769, 28773, 28777, 28781, 28785, 28789, 28793, 28797]

    def updateLabels(self):
        """Update visual information about parking."""
        ANGConnSetText(self.inId, AKIConvertFromAsciiString(str(self.totIn)))
        ANGConnSetText(self.outId, AKIConvertFromAsciiString(str(self.totOut)))
        ANGConnSetText(self.occId, AKIConvertFromAsciiString(str(self.occupancy)))
        ANGConnSetText(self.maxId, AKIConvertFromAsciiString(str(self.maxCapacity)))


    def parkCar(self, idsection, num_of_pedestrian=-1):
        """Park a car and spawn pedestrians if there is enough space in the parking.

        :param idsection: identifier of the last section the car was on before unspawning
        :type idsection: integer

        :param num_of_pedestrian: number of pedestrians that is dropped when the car is succesfully parked
        :type num_of_pedestrian: integer
        """
        if idsection == self.inSectionId:
            if self.occupancy < self.maxCapacity:
                self.totIn += 1
                self.occupancy += 1
                self.store_data()
                if num_of_pedestrian < 1:
                    num_of_pedestrian = 3
                
                for i in range(num_of_pedestrian):
                    pass
                    #self.pedestriansToSpawnCount.append(-1)

                return True
            else:
                return False
        else:
            return True

    def unparkCar(self, idsection):
        """Unpark a car if there is at least one car in the parking.

        :param idsection: identifier of the section the car spawned on
        :type idsection: integer
        """
        if idsection == self.outSectionId:
            if self.pedestrianCount > 0:
                amountOfPedestrians = 3
                if self.occupancy > 0 and self.pedestrianCount >= amountOfPedestrians:
                    self.pedestrianCount -= amountOfPedestrians
                    self.totOut += 1
                    self.occupancy -= 1
                    self.store_data()

                    return True, amountOfPedestrians
            # if parking empty
            return False, 0
        # if not current parking
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

    def generate_pedestrians(
        self,
        amount_pedestrian: int,
        specific_in_centroid: int = -1,
        specific_out_centroid: int = -1,
    ):
        """Generate some pedestrians and let them walk to their out centroid.

        In and out centroids are randomly choosen from all pedestrian centroids stored in
        self.inPedestrianCentroidId and self.outPedestrianCentroidId.

        :param amount_pedestrian: amount of pedestrians that is dropped when the car is succesfully parked
        :type num_of_pedestrian: int

        :param specific_in_centroid: identifier of a specific source centroid where pedestrians should spawn
        if equal to -1, then a random centroid from self.inPedestrianCentroidId is choosen.
        :type specific_in_centroid: int

        :param specific_out_centroid: identifier of a specific destination centroid where pedestrians should go
        if equal to -1, then a random centroid from self.outPedestrianCentroidId is choosen.
        :type specific_out_centroid: int

        :return returnVal: equal or greater than 0 if pedestrians are successfully generated, lower than 0 else.
        :type returnVal: int
        """
        # make the pedestrian exit the parking from one of the different centroid,
        # and choose one destination where the pedestrian will walk
        in_centroid = choice(self.inPedestrianCentroidId)
        out_centroid = choice(self.outPedestrianCentroidId)

        # if a specific route is given, set the in/out centroids as the given route
        if specific_in_centroid != -1:
            in_centroid = specific_in_centroid
        if specific_out_centroid != -1:
            out_centroid = specific_out_centroid

        returnVal = AKIGeneratePedestrians(in_centroid, out_centroid, -1, amount_pedestrian)
        return returnVal

    simulation_date = datetime.datetime(2023, 5, 23, 8, 0)
    originelle_date = datetime.datetime(1970, 1, 1)

    delta_date = simulation_date - originelle_date

    sim_date_offset = 0 #int(delta_date.total_seconds())

    def store_data(self):
        """Store parking data in order to send them to the web API at the end of simulation."""
        #if self.online:
        data = {
            "timestamp_uid": self.timestamp,
            "value": self.occupancy,
            "timestamp": str(self.sim_date_offset + AKIGetCurrentSimulationTime()/60),
        }
        self.data_to_post.append(data)


    def post_data(self):
        """Post parking data to the web API."""
        #if self.online:
        print(f"SENDING DATA RIGHT NOW: {datetime.datetime.now()}")
        with open(f'c://tmp//KPIs//{self.title}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for data in self.data_to_post:
                writer.writerow([data['timestamp'],data['value']])
                #post_succeed = w_api.post_parking_results(self.id, self.data_to_post)
                #if not post_succeed:
                #    print("The data transfer did not succeed.")

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

    def init_parking_datas(self) -> None:
        """Initialize the parkings with the latest parking configuration added in the web API."""
        for p in self.parkings:
            parking: Parking = p
            self.pedestrians_to_be_checked = []
            self.pedestrians_to_remove = []
            self.fast_check_in_green_centroid = 29921
            self.remove_pedestrian_centroid = 29416
            self.prioritized_pedestrians_to_spawn = []
            self.authorized_attr = attr.create_attr(int, "authorized")

            data = None

            """
            try:
                data = w_api.get_parking_config(p.parkingId)
            except w_api.OfflineException:
                continue
            """

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

    def remove_pedestrians(self):
        for pedestrian in self.pedestrians_to_remove:
            static_infs = AKIPedestrianGetStaticInf(pedestrian)
            static_infs.destinationID = self.remove_pedestrian_centroid
            AKIPedestrianSetStaticInf(static_infs)
            self.pedestrians_to_remove.remove(pedestrian)

    def add_pedestrian_to_parking(self, end_centroid):
        p = choice(self.parkings)
        p.pedestriansToSpawnCount.append(end_centroid)

    def add_prioritized_pedestrian_to_parking(self, end_centroid):
        self.prioritized_pedestrians_to_spawn.append(end_centroid)

    def check_if_pedestrian_can_spawn(self, start_centroid, end_centroid):
        if start_centroid == self.fast_check_in_green_centroid:
            if len(self.prioritized_pedestrians_to_spawn) > 0 \
                    and end_centroid in self.prioritized_pedestrians_to_spawn:
                self.prioritized_pedestrians_to_spawn.remove(end_centroid)
                return True
        else:
            parkings_copy = self.parkings.copy()
            shuffle(parkings_copy)
            for p in parkings_copy:
                p: Parking
                if len(p.pedestriansToSpawnCount) > 0 and any(x in [-1, end_centroid] for x in p.pedestriansToSpawnCount):
                    if -1 in p.pedestriansToSpawnCount:
                        p.pedestriansToSpawnCount.remove(-1)
                    else:
                        p.pedestriansToSpawnCount.remove(end_centroid)

                    return True
        
        return False
    
    def print_pedestrians_to_spawn_lists(self):
        peds_to_be_spawned = sum([len(p.pedestriansToSpawnCount) for p in self.parkings])
        if peds_to_be_spawned > 0:
            print(f"[PAKRING] Remaining pax to be spawned: {peds_to_be_spawned}")


    def sim_step_manage(self):
        """Handle manage."""

        cur_time_in_mins = AKIGetCurrentSimulationTime()/60
        while(len(data.peds_to_spawn_parking) > 0 and cur_time_in_mins > data.peds_to_spawn_parking[0][0]):
            ped_end_centroid = data.peds_to_spawn_parking[0][1]
            ped_status = data.peds_to_spawn_parking[0][2]
            data.peds_to_spawn_parking.remove(data.peds_to_spawn_parking[0])
            print(f"[PARKING] Pedestrian going to gate {ped_end_centroid} added at {cur_time_in_mins}")
            if ped_status == "NORMAL":
                self.add_pedestrian_to_parking(ped_end_centroid)
            if ped_status == "PRIORITY":
                self.add_prioritized_pedestrian_to_parking(ped_end_centroid)


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

    def sim_step_post_manage(self):
        """Handle post manage."""
        for p in self.parkings:
            p.updateLabels()

    def api_enter_vehicle(self, idsection: int, idveh: int):
        """Handle parking exit.

        :param idsection: Id of the section from where the vehicle left the parking
        :type idsection: int

        :param idveh: Id of the vehicule
        :type idveh: int
        """
        for p in self.parkings:
            successful, amountOfPedestrians = p.unparkCar(idsection)
            if not successful:
                self.removableVhcs.append(idveh)

    def api_exit_vehicle(self, idsection: int, idveh: int):
        """Handle parking entrance.

        :param idsection: Id of the section from where the vehicle entered the parking
        :type idsection: int

        :param idveh: Id of the vehicule
        :type idveh: int
        """
        del idveh

        for p, n in zip(self.parkings, self.get_nexts()):
            successful = p.parkCar(idsection)
            if not successful:
                AKIEnterVehTrafficOD(p.outSectionId, 0, p.parkingId, n.parkingId, 0)

    
    def add_pedestrian_to_be_controlled(self, idPedestrian, end_centroid, remaining_time):
        self.pedestrians_to_be_checked.append({'id': idPedestrian, 'end_centroid': end_centroid, 'remaining_time': remaining_time})

    def api_enter_pedestrian(self, idPedestrian):
        end_centroid = AKIPedestrianGetStaticInf(idPedestrian).destinationID
        self.add_pedestrian_to_be_controlled(idPedestrian, end_centroid, remaining_time=2)

    def add_pedestrian_count_to_parking(self):
        parking = choice(self.parkings)
        parking.pedestrianCount += 1


    def api_exit_pedestrian(self, idPedestrian):
        if attr.is_authorized(idPedestrian):
            self.add_pedestrian_count_to_parking()

    def post_data_for_each_parking(self):
        """Post parking data to the web API for each parking."""
        for p in self.parkings:
            p.post_data()

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
