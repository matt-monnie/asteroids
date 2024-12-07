import pygame  # Import the pygame library for game development
import sys  # Import the sys library to handle system-specific parameters (e.g., for exiting the game)
import os  # Import the os library for working with file paths
from constants import *  # Import constants (such as screen dimensions, player stats, etc.)
from player import *  # Import the Player class from player.py
from asteroid import *  # Import the Asteroid class from asteroid.py
from asteroidfield import *  # Import the AsteroidField class from asteroidfield.py
from pygame.mixer import Sound  # Import Sound class from pygame.mixer for handling sounds

running = False  # Variable to track whether the game is running

# Function to handle background music playback
def play_background_music(background_music, channel):
    current_index = 0  # Start with the first song

    # Function to play the next sound in the list
    def play_next_sound():
        nonlocal current_index
        channel.play(background_music[current_index])  # Play the current song
        current_index = (current_index + 1) % len(background_music)  # Cycle through the music list

    channel.set_endevent(pygame.USEREVENT)  # Set an event to trigger when the sound ends
    play_next_sound()  # Play the first sound immediately

    running = True  # Indicate that the game is running

# Main game loop
def main():
    pygame.init()  # Initialize all the pygame modules
    pygame.font.init()  # Initialize pygame's font module
    pygame.mixer.init()  # Initialize pygame's sound mixer

    font = pygame.font.SysFont("Arial", 30)  # Create a font for rendering text (score, etc.)

    # Load background music files
    sound1 = Sound("sounds/SongA.wav")
    sound2 = Sound("sounds/SongB.wav")
    sound3 = Sound("sounds/SongC.wav")
    background_music = [sound1, sound2, sound3]  # List of music tracks

    channel = pygame.mixer.Channel(0)  # Create a channel for background music

    # Set up the game screen (width and height from constants)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load and scale the background image
    backdrop = pygame.image.load(os.path.join('images', 'A_CompleteSpaceBackground.png'))
    backdrop = pygame.transform.scale(backdrop, (SCREEN_WIDTH, SCREEN_HEIGHT))
    backdropbox = screen.get_rect()  # Get the rect (bounding box) for the backdrop (for positioning)

    score = 0  # Initialize score
    # Load the background image for the score box
    score_background_image = pygame.image.load(os.path.join('images', 'list_box.png'))
    score_background_image = pygame.transform.scale(score_background_image, (200, 50))

    # Create sprite groups for managing different types of objects
    updatable = pygame.sprite.Group()  # Group for objects that need to be updated each frame
    drawable = pygame.sprite.Group()  # Group for objects that need to be drawn each frame
    asteroids = pygame.sprite.Group()  # Group for asteroids
    shots = pygame.sprite.Group()  # Group for shots

    # Set up the containers for Asteroid and AsteroidField classes
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()  # Create an AsteroidField object

    # Set up the containers for Player and Shot classes
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Create the player at the center of the screen

    game_clock = pygame.time.Clock()  # Create a clock to control the game's frame rate
    dt = 0  # Delta time (time between frames)

    play_background_music(background_music, channel)  # Start playing background music

    while(True):
        # Clear the screen by drawing the background
        screen.blit(backdrop, (0,0))

        # Render the score as text
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))

        # Position for the score text
        text_rect = score_text.get_rect(center=(110,35))

        # Draw the background image for the score box (places it behind the score text)
        screen.blit(score_background_image, (10,10))

        # Draw the score text on top of the score box image
        screen.blit(score_text, text_rect)

        # Update all updatable objects (e.g., player, asteroids, shots)
        for obj in updatable:
            obj.update(dt)

        # Check for collisions between the player and asteroids
        for asteroid in asteroids:
            if asteroid.collision(player):  # If the player collides with an asteroid
                player.death()  # Call the death method on the player
                print("Game over!")  # Print game over message
                sys.exit()  # Exit the game

            # Check for collisions between shots and asteroids
            for shot in shots:
                if asteroid.collision(shot):  # If a shot hits an asteroid
                    score += 1  # Increase the score
                    shot.kill()  # Remove the shot
                    asteroid.split()  # Split the asteroid into smaller pieces

        # Draw all drawable objects (e.g., player, asteroids, shots)
        for obj in drawable:
            obj.draw(screen)

        # Handle all events (e.g., quit the game, music end event)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the window is closed
                running = False  # Stop the game
                return  # Exit the main loop
            elif event.type == pygame.USEREVENT:  # If background music ends
                pass  # You can add behavior here if needed

        # Update the display to show the new frame
        pygame.display.flip()

        # Get the time delta (time elapsed since the last frame) and regulate the game to run at 60 FPS
        dt = game_clock.tick(60) / 1000  # dt is the time elapsed since the last frame (in seconds)

# Run the main game loop if this script is executed directly
if __name__ == "__main__":
    main()
