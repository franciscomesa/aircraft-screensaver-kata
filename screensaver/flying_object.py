from abc import abstractmethod, ABC

from screensaver.direction import Direction
from screensaver.position import Position


# TODO: BADSMELLS May be rename it to Flyable?
class FlyingObject(ABC):
    @abstractmethod
    def current_position(self) -> Position:
        pass

    @abstractmethod
    def is_colliding_with(self, flying_object) -> bool:
        pass

    @abstractmethod
    def move(self, direction: Direction = None) -> None:
        pass
