
from AAPI import *
import joined_parking as jp

REMAINING_TIME_KEY = "remaining_time"
ROTATION_STATE_KEY = "rotation_state"
VEH_ID_KEY = "veh_id"

PLANE_TYPE = 2


class PlaneRotate():

    def __init__(self, plane_start_sections, plane_end_section, rotation_centroids, remaining_times, nb_rotation_steps):
        self.plane_start_sections = plane_start_sections
        self.plane_end_section = plane_end_section
        self.rotation_centroids = rotation_centroids
        self.remaining_times = remaining_times
        self.nb_rotation_steps = nb_rotation_steps
        self.vehicles_go_backward = []


    # Init a plane rotation if the given section (idsection) is the plane_end_section
    # This function is called by joined_plane_rotate when any vehicle exits the simulation 
    def init_plane_rotation(self, idsection):
        if idsection == self.plane_end_section:
            self.create_backward_vehicle(self.plane_start_sections[0], 
                                         PLANE_TYPE, 
                                         self.rotation_centroids[0], 
                                         self.rotation_centroids[1], 
                                         -20, 
                                         self.remaining_times[0], 
                                         1)


    def manage_rotations(self):
        for vehicle in self.vehicles_go_backward:
            vehicle[REMAINING_TIME_KEY] -= AKIGetSimulationStepTime()
        
            if vehicle[REMAINING_TIME_KEY] < 0:

                vehicle_rotation_state = vehicle[ROTATION_STATE_KEY]
                jp.add_vhc_to_remove(vehicle[VEH_ID_KEY])
                self.vehicles_go_backward.remove(vehicle)

                if vehicle_rotation_state < self.nb_rotation_steps :

                    self.create_backward_vehicle(self.plane_start_sections[vehicle_rotation_state], 
                                            PLANE_TYPE, 
                                            self.rotation_centroids[vehicle_rotation_state],
                                            self.rotation_centroids[vehicle_rotation_state+1],
                                            speed=-20,
                                            remaining_time=self.remaining_times[vehicle_rotation_state],
                                            rotation_state=vehicle_rotation_state+1)
                    
                if vehicle_rotation_state == self.nb_rotation_steps :
                    AKIEnterVehTrafficOD(self.plane_start_sections[-1], PLANE_TYPE, self.rotation_centroids[-2], self.rotation_centroids[-1], 0)


    def create_backward_vehicle(self, start_section, vehicle_type, start_centroid, end_centroid, speed = -20, remaining_time = 15, rotation_state = 1):
        new_vehid = AKIEnterVehTrafficOD(start_section, vehicle_type, start_centroid, end_centroid, 0)
        self.vehicles_go_backward.append({VEH_ID_KEY: new_vehid, REMAINING_TIME_KEY: remaining_time, ROTATION_STATE_KEY: rotation_state})
        self.set_vehicle_max_speed_from_static_infs(new_vehid, speed)


    def set_vehicle_max_speed_from_static_infs(self, idveh, desired_speed):
        static_infs = AKIVehGetStaticInf(idveh)
        static_infs.maxDesiredSpeed = desired_speed
        ret_val = AKIVehSetStaticInf(idveh, static_infs)



