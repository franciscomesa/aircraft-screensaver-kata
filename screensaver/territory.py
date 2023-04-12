from typing import List

from screensaver.flying_object import FlyingObject
from screensaver.position import Position


class Territory:
    def __init__(self, max_longitude: int = 100, max_latitude: int = 100):
        self.max_longitude = max_longitude
        self.min_longitude = 0
        self.max_latitude = max_latitude
        self.min_latitude = 0
        self.flying_objects = []

    # TODO: BADSMELL: Guard clause missing.
    #                 At this moment we don't know if this is a good name.
    def register(self, flying_object: FlyingObject):
        self.flying_objects.append(flying_object)
        # Proposal: handle the case of registering a collision

    def at_northern_border(self, position: Position) -> bool:
        return position.latitude == self.min_latitude

    def at_eastern_border(self, position: Position) -> bool:
        return position.longitude == self.max_longitude

    def detect_collisions(self, flying_object: FlyingObject):
        other_objects = [f for f in self.flying_objects if f != flying_object]
        for other_object in other_objects:
            if flying_object.is_colliding_with(other_object):
                self.flying_objects.remove(flying_object)
                self.flying_objects.remove(other_object)

    def get_flying_objects(self) -> List[FlyingObject]:
        return self.flying_objects.copy()

    def is_out_of(self, position: Position) -> bool:
        return (position.longitude > self.max_longitude or
                position.latitude > self.max_latitude or
                position.longitude < self.min_longitude or
                position.latitude < self.min_latitude)
