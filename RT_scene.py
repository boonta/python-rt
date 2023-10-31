# Scene class
import RT_utility as rtu
import numpy as np

class Scene:
    def __init__(self) -> None:
        self.obj_list = []
        self.hit_list = None
        pass

    def add_object(self, obj):
        self.obj_list.append(obj)

    def find_intersection(self, vRay, tmin, tmax):

        np_obj_list = np.array(self.obj_list)
        found_hit = False
        closest_tmax = tmax
        hinfo = None
        for obj in np_obj_list:
            hinfo = obj.intersect(vRay, tmin, closest_tmax)
            if hinfo is not None:
                closest_tmax = hinfo.getT()
                found_hit = True
                self.hit_list = hinfo

        return found_hit

    def find_intersection(self, vRay, cInterval):

        np_obj_list = np.array(self.obj_list)
        found_hit = False
        closest_tmax = cInterval.max_val
        hinfo = None
        for obj in np_obj_list:
            hinfo = obj.intersect(vRay, rtu.Interval(cInterval.min_val, closest_tmax))
            if hinfo is not None:
                closest_tmax = hinfo.getT()
                found_hit = True
                self.hit_list = hinfo

        return found_hit


    def getHitNormalAt(self, idx):
        return self.hit_list[idx].getNormal() 
    
    def getHitList(self):
        return self.hit_list


