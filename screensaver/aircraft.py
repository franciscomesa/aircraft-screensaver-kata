from typing import Union

from screensaver.direction import Direction
from screensaver.flying_object import FlyingObject
from screensaver.position import Position
from screensaver.territory import Territory
from screensaver.InvalidPositionError import InvalidPositionError


# TODO: BADSMELL: Territory as dependency
class Aircraft(FlyingObject):
    def __init__(self, position: Position, territory: Territory, direction: Direction = Direction.North):
        self.position = position
        self.territory = territory
        self.direction = direction

    def current_position(self) -> Position:
        return self.position.copy()

    def move(self, direction: Direction = None) -> None:
        if direction is None:
            direction = self.direction
        else:
            self.direction = direction
        new_position = self.calculate_new_position(direction)
        self.position = new_position
        self.territory.detect_collisions(self)

    def calculate_new_position(self, direction):
        diff_position = calculate_position_differential_from(direction)
        match direction:
            case direction.NorthEast:
                if self.territory.at_northern_border(self.position):
                    diff_position.latitude = 1
                if self.territory.at_eastern_border(self.position):
                    diff_position.longitude = -1
            case direction.NorthWest:
                if self.territory.at_northern_border(self.position):
                    diff_position.latitude = 1
                if self.territory.at_western_border(self.position):
                    diff_position.longitude = 1
            case direction.SouthEast:
                if self.territory.at_southern_border(self.position):
                    diff_position.latitude = -1
                if self.territory.at_eastern_border(self.position):
                    diff_position.longitude = -1
            case direction.SouthWest:
                if self.territory.at_southern_border(self.position):
                    diff_position.latitude = -1
                if self.territory.at_western_border(self.position):
                    diff_position.longitude = 1
            case direction.North:
                if self.territory.at_northern_border(self.position):
                    diff_position.latitude = 1
            case direction.South:
                if self.territory.at_southern_border(self.position):
                    diff_position.latitude = -1
            case direction.East:
                if self.territory.at_eastern_border(self.position):
                    diff_position.longitude = -1
            case direction.West:
                if self.territory.at_western_border(self.position):
                    diff_position.longitude = 1

        new_position = Position.add(self.position, diff_position)
        return new_position

    def is_colliding_with(self, flying_object: FlyingObject) -> bool:
        return self.position == flying_object.current_position()


def create(position: Position, territory: Territory, direction: Direction = None) -> Union[
    Aircraft, InvalidPositionError]:
    # TODO: Do not use parameter at error if only is used here
    if territory.is_out_of(position):
        return InvalidPositionError("The position cant be out of the territory")

    aircraft = Aircraft(position, territory, direction)
    territory.register(aircraft)
    return aircraft


# TODO: Position + Direction = Movement?
def calculate_position_differential_from(direction) -> Position:
    match direction:
        case direction.NorthEast:
            return Position(1, -1)  # Default NortEast move
        case direction.NorthWest:
            return Position(-1, -1)
        case direction.SouthEast:
            return Position(1, 1)
        case direction.SouthWest:
            return Position(-1, 1)
        case direction.North:
            return Position(0, -1)
        case direction.South:
            return Position(0, +1)
        case direction.East:
            return Position(1, 0)
        case direction.West:
            return Position(-1, 0)
