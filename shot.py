from circleshape import *  # Import the CircleShape class, presumably to define the shot's shape
from constants import *     # Import constants like SHOT_RADIUS and PLAYER_SHOOT_SPEED

class Shot(CircleShape):  # Shot class inherits from CircleShape (likely to inherit position and radius properties)
    def __init__(self, x, y, rotation):
        # Initialize the shot by calling the superclass constructor to set its position and radius
        super().__init__(x, y, SHOT_RADIUS)

        # Set the velocity of the shot based on the rotation angle passed in, adding 180 to reverse direction
        # The vector (0, 1) represents the "forward" direction, then we rotate it to match the player's rotation
        # and scale it by the PLAYER_SHOOT_SPEED constant to determine how fast it moves.
        self.velocity = pygame.Vector2(0, 1).rotate(rotation + 180) * PLAYER_SHOOT_SPEED
        
        # Load the projectile image to represent the shot
        self.image = pygame.image.load("images/Projectile_1_Blue_Small.png")
        self.original_image = self.image  # Store the original image so it can be rotated later

        # Create a rectangle (rect) for the image, centered at the shot's position
        self.rect = self.image.get_rect(center = self.position)

    def draw(self, screen):
        # Rotate the image according to its velocity (angle of movement)
        # self.velocity.angle_to(pygame.Vector2(0, -1)) gives the angle between the shot's movement direction
        rotated_image = pygame.transform.rotate(self.original_image, self.velocity.angle_to(pygame.Vector2(0, -1)))
        
        # Create a new rect for the rotated image, centered at the shot's current position
        rotated_rect = rotated_image.get_rect(center = self.rect.center)
        
        # Draw the rotated image on the screen at the updated position
        screen.blit(rotated_image, rotated_rect)

    def update(self, dt):
        # Update the shot's position by adding the velocity scaled by delta time (dt) for smooth movement
        self.position += self.velocity * dt
        
        # Update the shot's rect position to match the new position
        self.rect.center = self.position
