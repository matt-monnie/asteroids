from circleshape import *  # Import the CircleShape class to inherit position and radius properties for the player
from constants import *     # Import constants like PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, etc.
from shot import *          # Import the Shot class to create shots fired by the player
from pygame.mixer import Sound  # Import Pygame's sound module to play sound effects

class Player(CircleShape):  # Player class inherits from CircleShape (for position and radius)
    def __init__(self, x, y):
        # Initialize the player by calling the superclass constructor to set its position and radius
        super().__init__(x, y, PLAYER_RADIUS)
        
        # Initialize the player's rotation angle and shot timer
        self.rotation = 0  # The initial rotation is 0 degrees
        self.shot_timer = 0  # Timer to control the rate of fire

        # Load the image for the player and store a reference to the original image for later rotation
        self.image = pygame.image.load("images/Blue_Player_Ship_1.png")
        self.original_image = self.image
        self.rect = self.image.get_rect(center = self.position)  # Create a rectangle for the image, centered at the player's position

        # Set up sound channels for shooting and death sound effects
        self.shoot_channel = pygame.mixer.Channel(1)
        self.death_channel = pygame.mixer.Channel(2)

        # Load sound files for shooting and death events
        self.shoot_sound = Sound("sounds/PlayerFire.wav")
        self.death_sound = Sound("sounds/PlayerExplode.wav")

    def draw(self, screen):
        # This method is responsible for drawing the player image on the screen at the player's current position
        screen.blit(self.image, self.rect)

    def rotate(self, dt):
        # This method rotates the player image by adjusting the rotation angle over time
        # PLAYER_TURN_SPEED * dt is the amount to rotate each frame (scaled by delta time)
        self.rotation += (PLAYER_TURN_SPEED * dt)
        
        # Rotate the original player image by the specified angle (counter-clockwise)
        self.image = pygame.transform.rotate(self.original_image, -self.rotation)

        # Update the player's rectangle to account for the rotation and re-center it on the player's position
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt):
        # This method updates the player state based on input and time (delta time)
        self.shot_timer -= dt  # Decrease the shot timer by delta time to handle cooldown

        # Get the current key states (whether keys are being pressed)
        keys = pygame.key.get_pressed()

        # Handle player movement and rotation based on key presses
        if keys[pygame.K_a]:  # Rotate left (counter-clockwise)
            self.rotate(-dt)
        if keys[pygame.K_d]:  # Rotate right (clockwise)
            self.rotate(dt)
        if keys[pygame.K_w]:  # Move forward
            self.move(-dt)
        if keys[pygame.K_s]:  # Move backward
            self.move(dt)
        if keys[pygame.K_SPACE]:  # Fire a shot if the spacebar is pressed
            self.shoot()

    def move(self, dt):
        # This method moves the player based on its current rotation
        # A forward vector is created based on the player's rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # The player's position is updated by moving in the forward direction
        # PLAYER_SPEED * dt scales the movement based on delta time
        self.position += forward * PLAYER_SPEED * dt
        
        # Update the player's rectangle to reflect the new position
        self.rect.center = self.position

    def shoot(self):
        # This method handles shooting a shot
        if self.shot_timer > 0:  # Check if the shot cooldown is active
            return  # If the shot cooldown is active, don't shoot
        
        # Reset the shot timer after firing
        self.shot_timer = PLAYER_SHOOT_COOLDOWN
        
        # Create a new shot at the player's current position and with the player's rotation
        Shot(self.position.x, self.position.y, self.rotation)
        
        # Play the shooting sound effect
        self.shoot_channel.play(self.shoot_sound)

    def death(self):
        # This method handles the player's death and plays the death sound
        if self.death_sound:  # If a death sound is defined, play it
            self.death_channel.play(self.death_sound)
            
            # Wait for the death sound to finish before continuing
            while self.death_channel.get_busy():
                pygame.time.delay(1)  # Wait for 1 millisecond to avoid freezing the game
