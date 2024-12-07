import pygame  # Import pygame library for game development
import random  # Import random module for generating random values
from asteroid import Asteroid  # Import the Asteroid class from asteroid.py
from constants import *  # Import constants for the game (such as screen dimensions, spawn rates, etc.)

# AsteroidField class handles the creation of asteroids in the game
class AsteroidField(pygame.sprite.Sprite):
    # Define the edges where asteroids will spawn (the four sides of the screen)
    edges = [
        # Right edge: Asteroids spawn moving left (positive x-axis)
        [
            pygame.Vector2(1, 0),  # Direction vector (1, 0) means moving in the positive x direction
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),  # Spawn position on the left side
        ],
        # Left edge: Asteroids spawn moving right (negative x-axis)
        [
            pygame.Vector2(-1, 0),  # Direction vector (-1, 0) means moving in the negative x direction
            lambda y: pygame.Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),  # Spawn position on the right side
        ],
        # Top edge: Asteroids spawn moving down (positive y-axis)
        [
            pygame.Vector2(0, 1),  # Direction vector (0, 1) means moving in the positive y direction
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),  # Spawn position above the screen
        ],
        # Bottom edge: Asteroids spawn moving up (negative y-axis)
        [
            pygame.Vector2(0, -1),  # Direction vector (0, -1) means moving in the negative y direction
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),  # Spawn position below the screen
        ],
    ]

    # Constructor to initialize the AsteroidField object
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)  # Initialize the sprite using containers from the parent class
        self.spawn_timer = 0.0  # Timer to control asteroid spawning

    # Method to spawn a new asteroid with given radius, position, and velocity
    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)  # Create a new Asteroid object
        asteroid.velocity = velocity  # Set the asteroid's velocity
        # You would likely need to add the asteroid to a group here to manage it (e.g., `self.containers.add(asteroid)`)

    # Update method called each frame to handle asteroid spawning and movement
    def update(self, dt):
        self.spawn_timer += dt  # Increase the spawn timer by the time elapsed since the last frame
        if self.spawn_timer > ASTEROID_SPAWN_RATE:  # Check if it's time to spawn a new asteroid
            self.spawn_timer = 0  # Reset the spawn timer

            # Randomly choose one of the screen edges to spawn the asteroid from
            edge = random.choice(self.edges)

            # Generate a random speed for the asteroid's velocity (between 40 and 100)
            speed = random.randint(40, 100)

            # Calculate the velocity by multiplying the direction vector by the speed
            velocity = edge[0] * speed

            # Apply a small random rotation to the velocity to add variation in direction
            velocity = velocity.rotate(random.randint(-30, 30))

            # Generate the spawn position along the chosen edge (between 0 and 1 for randomness)
            position = edge[1](random.uniform(0, 1))

            # Randomly choose a type of asteroid based on predefined kinds
            kind = random.randint(1, ASTEROID_KINDS)

            # Call the spawn method to create the asteroid with a size and velocity
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
