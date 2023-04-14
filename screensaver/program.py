import random
import sys

# Skeleton by chatGPT
import pygame
from pygame import Rect

import aircraft
from screensaver.direction import Direction
from screensaver.position import Position
from screensaver.territory import Territory

# Initialize screensaver
territory = Territory(max_longitude=40, max_latitude=30)

# Initialize Pygame
pygame.init()

# Set up the Pygame window
aircraft_size = 20
window_size = (
    territory.max_longitude * aircraft_size,
    territory.max_latitude * aircraft_size
)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Screensaver with aircrafts")

# Create the moving objects
object_color = (0, 0, 255)
object_size = (aircraft_size, aircraft_size)
for i in range(10):
    random_position = Position(
        longitude=random.randint(0, territory.max_longitude),
        latitude=random.randint(0, territory.max_latitude)
    )
    random_aircraft = aircraft.create(
        random_position,
        territory,
        random.choice(list(Direction))
    )
    territory.register(random_aircraft)

# Move the objects
while True and len(territory.get_flying_objects()) > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((255, 255, 255))
    for aircraft in territory.get_flying_objects():
        aircraft.move()
        rect = Rect(
            aircraft.current_position().longitude * aircraft_size,
            aircraft.current_position().latitude * aircraft_size,
            aircraft_size,
            aircraft_size
        )
        pygame.draw.rect(screen, object_color, rect)
    pygame.display.update()
    pygame.display.set_caption("Screensaver with " + str(len(territory.get_flying_objects())) + " aircrafts")
    pygame.time.wait(100)
