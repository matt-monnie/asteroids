import random  # Import random module for random number generation
from circleshape import *  # Import base class CircleShape
from constants import *  # Import constants used in the game
from pygame.mixer import Sound  # Import Sound class for handling sound effects

# Asteroid class, derived from the CircleShape class
class Asteroid(CircleShape):
    
    # Constructor to initialize the Asteroid object
    def __init__(self, x, y, radius):
        # Call the parent (CircleShape) constructor to initialize position, velocity, and radius
        super().__init__(x, y, radius)
        
        # Create a new channel for asteroid sound effects
        self.channel = pygame.mixer.Channel(3)
        # Load the explosion sound for when the asteroid is destroyed or split
        self.sound = Sound("sounds/EnemyExplode.wav")

    # Method to draw the asteroid on the screen
    def draw(self, screen):
        # Draw the asteroid as a white circle with the specified radius at its position
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    # Method to update the asteroid's position based on its velocity
    def update(self, dt):
        # Update the position by moving it in the direction of its velocity
        self.position += self.velocity * dt

    # Method to split the asteroid into smaller asteroids
    def split(self):
        # Play the explosion sound when the asteroid is split
        self.channel.play(self.sound)
        # Remove the current asteroid (destroy it)
        self.kill()
        
        # If the asteroid's radius is too small, don't split further
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # Randomly calculate two angles for spawning the new asteroids
        spawn_angle = random.uniform(20.0, 50.0)
        
        # Rotate the velocity vector by the calculated spawn angles to create two new directions
        spawn_vector1 = self.velocity.rotate(spawn_angle)
        spawn_vector2 = self.velocity.rotate(-spawn_angle)

        # Decrease the radius of the new asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        # Create the first new asteroid with a modified velocity
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = spawn_vector1 * 1.2  # Increase the velocity slightly for the new asteroid

        # Create the second new asteroid with a different velocity
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = spawn_vector2 * 1.2  # Increase the velocity slightly for the new asteroid
