from statistics import mean
import lib.simdata as data
from AAPI import *
from typing import List


class KPI:
    def __init__(self, name: str):  # (sampling each minute when sampling_interval = 60)
        self.name = name

    def get_name(self):
        return self.name

    def api_manage(self, cur_sim_delta_time):
        pass


class KPIList:
    kpis: List[KPI]

    def __init__(
        self, kpis: List[KPI] = []
    ):  # (sampling each minute when sampling_interval = 60)
        self.kpis = kpis

    def add_kpi(self, kpi: KPI):
        self.kpis.append(kpi)

    def get_kpis(self):
        return self.kpis

    def get_ped_kpis(self):
        return [kpi for kpi in self.kpis if isinstance(kpi, PedestrianKPI)]

    def get_car_kpis(self):
        return [kpi for kpi in self.kpis if isinstance(kpi, CarKPI)]

    def api_manage(self, cur_sim_delta_time):
        for kpi in self.kpis:
            kpi.api_manage(cur_sim_delta_time)


class CarKPI(KPI):
    sample_per_timestamp = {}
    """
    def __init__(self, name: str, sampling_interval: int = 60): #(sampling each minute when sampling_interval = 60)
        super().__init__(name)
        self.sampling_interval = sampling_interval
        self.cur_counter = sampling_interval

    def api_manage(self, cur_sim_delta_time):
        cur_counter -= cur_sim_delta_time
        if cur_counter <= 0:
            cur_counter = self.sampling_interval - cur_counter
            self.save_samples()
            return True
        return False

    # HAS TO BE OVERRIDEN WHEN INHERITING
    def sample(self, veh_id):
        pass

    # HAS TO BE OVERRIDEN WHEN INHERITING
    def save_samples(self):
        pass

    def get_samples_mean(self):
        return mean(self.sample_per_timestamp.values())
    
    def round_timestamp(self, timestamp):
        return round(timestamp/self.sampling_interval)

    def get_sample_at_timestamp(self, timestamp):
        return self.sample_per_timestamp[self.round_timestamp(timestamp)]
    
    def set_sample_at_timestamp(self, timestamp, val):
        self.sample_per_timestamp[self.round_timestamp(timestamp)] = val
    """


class PedestrianKPI(KPI):
    def __init__(
        self, name: str, sampling_interval: int = 60
    ):  # (sampling each minute when sampling_interval = 60)
        super().__init__(name)
        self.sample_per_timestamp = {}
        self.sampling_interval = sampling_interval
        self.cur_counter = sampling_interval

    def api_manage(self, cur_sim_delta_time):
        self.cur_counter -= cur_sim_delta_time
        if self.cur_counter <= 0:
            self.cur_counter = self.sampling_interval - self.cur_counter
            self.save_samples()
            return True
        return False

    # HAS TO BE OVERRIDEN WHEN INHERITING
    def sample(self, ped):
        pass

    # HAS TO BE OVERRIDEN WHEN INHERITING
    def save_samples(self):
        pass

    def get_samples_mean(self):
        return mean(self.sample_per_timestamp.values())

    def round_timestamp(self, timestamp):
        return round(timestamp / self.sampling_interval)

    def get_sample_at_timestamp(self, timestamp):
        return self.sample_per_timestamp[self.round_timestamp(timestamp)]

    def set_sample_at_timestamp(self, timestamp, val):
        #print(f"from set_sample_at_timestamp: {val}")
        self.sample_per_timestamp[self.round_timestamp(timestamp)] = val


class AreaPedRateKPI(PedestrianKPI):
    def __init__(self, name: str, coords, sampling_interval: int = 60):
        super().__init__(name, sampling_interval)
        self.cur_peds = {}
        self.coords = coords

    def sample(self, ped):
        ped_pos = AKIPedestrianGetInf(ped).position
        if (
            ped_pos.x > self.coords["x_left"]
            and ped_pos.x < self.coords["x_right"]
            and ped_pos.y > self.coords["y_bottom"]
            and ped_pos.y < self.coords["y_top"]
        ):
            if ped not in self.cur_peds.keys():
                self.cur_peds[ped] = (1,True)

            if self.coords["service_point_name"] == 'GATE':
                if ped in data.passenger_start_time:
                    travel_time = round((AKIGetCurrentSimulationTime() - data.passenger_start_time[ped])/60)
                    data.passenger_start_time.pop(ped)
                    if travel_time in data.travel_time_distribution.keys():
                        data.travel_time_distribution[travel_time] += 1
                    else:
                        data.travel_time_distribution[travel_time] = 1
            
            

    def save_samples(self):
        """
        print(
            f"SAVING SAMPLES: {self.cur_peds} at time: {self.round_timestamp(AKIGetCurrentSimulationTime())}"
        )"""

        self.set_sample_at_timestamp(
            timestamp=AKIGetCurrentSimulationTime(), val=len([1 for v in self.cur_peds.values() if v[1] == True])
        )
        #print(f"from save_samples: {len(self.cur_peds)}")

        for key,value in self.cur_peds.items():
            if value[1] == True:
                new_val = (value[0], False)
                self.cur_peds[key] = new_val


class AreaPedAlarmKPI(PedestrianKPI):
    def __init__(self, name: str, coords, sampling_interval: int = 60, alarm_threshold = 40):
        super().__init__(name, sampling_interval)
        self.cur_peds = {}
        self.coords = coords
        self.alarm_threshold = alarm_threshold*60


    def sample(self, ped):
        ped_pos = AKIPedestrianGetInf(ped).position
        if (
            ped_pos.x > self.coords["x_left"]
            and ped_pos.x < self.coords["x_right"]
            and ped_pos.y > self.coords["y_bottom"]
            and ped_pos.y < self.coords["y_top"]
        ):
            if ped in self.cur_peds:
                self.cur_peds[ped] += AKIGetSimulationStepTime()

                if self.cur_peds[ped] > self.alarm_threshold:
                    print(f"KPI {self.get_name} DETECTED PASSENGER WAITING FOR MORE THAN {self.alarm_threshold/60} MINUTES")
                    with open("C:/Users/tony.licata/Documents/aimsun_projects/TrainMalpensa/alarm.txt", "w") as alarm_file:
                        alarm_file.write(f"{self.get_name()},{self.alarm_threshold},{len(self.cur_peds)}\n")

            else:
                self.cur_peds[ped] = AKIGetSimulationStepTime()
            
        else:
            if ped in self.cur_peds:
                self.cur_peds.pop(ped)

    def save_samples(self):
        """
        print(
            f"SAVING SAMPLES: {self.cur_peds} at time: {self.round_timestamp(AKIGetCurrentSimulationTime())}"
        )"""

        self.set_sample_at_timestamp(
            timestamp=AKIGetCurrentSimulationTime(), val=len(self.cur_peds)
        )
        #print(f"from save_samples: {len(self.cur_peds)}")

        self.cur_peds.clear()