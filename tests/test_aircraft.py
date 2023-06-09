import unittest
from assertpy import assert_that

from screensaver import aircraft
from screensaver.direction import Direction
from screensaver.InvalidPositionError import InvalidPositionError
from screensaver.position import Position
from screensaver.territory import Territory


class TestAircraft(unittest.TestCase):
    def test_aircraft_cant_be_positioned_out_of_the_territory(self):
        an_aircraft = aircraft.create(
            Position(longitude=5000, latitude=5000), Territory(max_longitude=200, max_latitude=200))

        assert_that(an_aircraft).is_instance_of(InvalidPositionError)

    def test_aircraft_changes_position_when_moving(self):
        an_aircraft = aircraft.create(
            Position(longitude=5, latitude=5), Territory(max_longitude=200, max_latitude=200))

        an_aircraft.move(Direction.NorthEast)

        assert_that(an_aircraft.current_position())\
            .is_equal_to(Position(longitude=6, latitude=4))

    def test_aircraft_keeps_the_direction(self):
        an_aircraft = aircraft.create(
            Position(longitude=5, latitude=5), Territory(max_longitude=200, max_latitude=200), Direction.North)

        an_aircraft.move()
        an_aircraft.move()

        assert_that(an_aircraft.current_position())\
            .is_equal_to(Position(longitude=5, latitude=3))

    def test_aircraft_bounces_at_the_territory_northern_border(self):
        territory = Territory(max_longitude=6, max_latitude=6)
        an_aircraft = aircraft.create(Position(longitude=3, latitude=0), territory)

        an_aircraft.move(Direction.NorthEast)

        assert_that(an_aircraft.current_position())\
            .is_equal_to(Position(longitude=4, latitude=1))

    def test_aircraft_bounces_at_the_territory_southern_border(self):
        territory = Territory(max_longitude=6, max_latitude=6)
        an_aircraft = aircraft.create(Position(longitude=3, latitude=6), territory)

        an_aircraft.move(Direction.South)

        assert_that(an_aircraft.current_position())\
            .is_equal_to(Position(longitude=3, latitude=5))

    def test_aircraft_bounces_at_the_territory_northerneast_border(self):
        territory = Territory(max_longitude=6, max_latitude=6)
        an_aircraft = aircraft.create(Position(longitude=6, latitude=0), territory)

        an_aircraft.move(Direction.NorthEast)

        assert_that(an_aircraft.current_position())\
            .is_equal_to(Position(longitude=5, latitude=1))

    def test_aircraft_bounces_at_the_territory_southernwest_border(self):
        territory = Territory(max_longitude=6, max_latitude=6)
        an_aircraft = aircraft.create(Position(longitude=0, latitude=6), territory)

        an_aircraft.move(Direction.SouthWest)

        assert_that(an_aircraft.current_position())\
            .is_equal_to(Position(longitude=1, latitude=5))

    def test_aircraft_bounces_at_the_territory_southerneast_border(self):
        territory = Territory(max_longitude=6, max_latitude=6)
        an_aircraft = aircraft.create(Position(longitude=6, latitude=6), territory)

        an_aircraft.move(Direction.SouthEast)

        assert_that(an_aircraft.current_position())\
            .is_equal_to(Position(longitude=5, latitude=5))

    def test_aircraft_bounces_at_the_territory_northernwest_border(self):
        territory = Territory(max_longitude=6, max_latitude=6)
        an_aircraft = aircraft.create(Position(longitude=0, latitude=0), territory)

        an_aircraft.move(Direction.NorthEast)

        assert_that(an_aircraft.current_position())\
            .is_equal_to(Position(longitude=1, latitude=1))

    def test_aircraft_bounces_at_the_territory_eastern_border(self):
        an_aircraft = aircraft.create(
            Position(longitude=5, latitude=4),
            Territory(max_longitude=5, max_latitude=5)
        )

        an_aircraft.move(Direction.East)

        assert_that(an_aircraft.current_position()).is_equal_to(Position(longitude=4, latitude=4))

    def test_aircraft_bounces_at_the_territory_western_border(self):
        an_aircraft = aircraft.create(
            Position(longitude=0, latitude=4),
            Territory(max_longitude=5, max_latitude=5)
        )

        an_aircraft.move(Direction.West)

        assert_that(an_aircraft.current_position()).is_equal_to(Position(longitude=1, latitude=4))

    def test_there_could_be_many_aircrafts_in_the_territory(self):
        territory = Territory(max_longitude=6, max_latitude=6)
        aircraft.create(Position(longitude=3, latitude=1), territory)
        aircraft.create(Position(longitude=4, latitude=1), territory)

        assert_that(len(territory.get_flying_objects())).is_equal_to(2)

    def test_aircrafts_disappears_if_collide_with_another_aircraft(self):
        territory = Territory(max_longitude=6, max_latitude=6)
        aircraft.create(Position(longitude=3, latitude=1), territory)
        another_aircraft = aircraft.create(Position(longitude=4, latitude=1), territory)

        another_aircraft.move(Direction.West)

        assert_that(len(territory.get_flying_objects())).is_equal_to(0)
