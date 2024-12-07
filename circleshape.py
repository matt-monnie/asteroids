import pygame  # Import Pygame module

# Base class for game objects that are circular shapes (e.g., player, shots, asteroids)
class CircleShape(pygame.sprite.Sprite):
    
    # Constructor to initialize the CircleShape object
    def __init__(self, x, y, radius):
        # Initialize the parent class (Sprite) with containers, if available
        if hasattr(self, "containers"):  # Check if this class has a 'containers' attribute (used for sprite groups)
            super().__init__(self.containers)  # Pass the containers to the Sprite class for management
        else:
            super().__init__()  # Otherwise, just initialize the Sprite class without containers
        
        self.position = pygame.Vector2(x, y)  # Set the initial position as a pygame Vector2 (x, y)
        self.velocity = pygame.Vector2(0, 0)  # Initialize velocity as a zero vector (no movement by default)
        self.radius = radius  # Set the radius of the object (used for collision detection)

    
    # This method is a placeholder for drawing the object on the screen
    # Sub-classes must override this method to specify how they will be drawn
    def draw(self, screen):
        pass  # Nothing happens here. Subclasses should implement this.

    # This method is a placeholder for updating the object's state
    # Sub-classes must override this method to specify how the object updates over time
    def update(self, dt):
        pass  # Nothing happens here. Subclasses should implement this.

    # Collision detection method: Checks if this object collides with another CircleShape
    def collision(self, other):
        # Calculate the distance between the two objects' positions
        # If the distance is less than or equal to the sum of their radii, they are colliding
        return (self.position.distance_to(other.position) <= self.radius + other.radius)
