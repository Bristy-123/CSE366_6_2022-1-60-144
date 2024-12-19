import pygame
from Agent import Agent
from Environment import Environment

# Pygame initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600  # Window size
AGENT_SIZE = 20  # Size of the agent
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Agent-Environment Simulation")

def main():
    # Create environment and agent
    env = Environment(WIDTH, HEIGHT)
    agent = Agent(name="Agent A", environment=env, position=(WIDTH // 2, HEIGHT // 2))

    # Font for displaying agent position and direction
    font = pygame.font.Font(None, 36)

    # Variable to store the last movement direction
    last_direction = ""

    # Main loop
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key presses for movement and update direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            agent.move("up")
            last_direction = "UP"
        elif keys[pygame.K_DOWN]:
            agent.move("down")
            last_direction = "DOWN"
        elif keys[pygame.K_LEFT]:
            agent.move("left")
            last_direction = "LEFT"
        elif keys[pygame.K_RIGHT]:
            agent.move("right")
            last_direction = "RIGHT"

        # Draw agent
        position = agent.get_position()
        pygame.draw.rect(screen, BLUE, (*position, AGENT_SIZE, AGENT_SIZE))

        # Display agent position and last movement direction on new lines
        position_text = font.render(f"Position: {position}", True, BLACK)
        direction_text = font.render(f"Direction: {last_direction}", True, BLACK)
        
        # Display the position and direction at different vertical positions
        screen.blit(position_text, (10, 10))          # Position at the top
        screen.blit(direction_text, (10, 50))         # Slightly below position

        # Update display
        pygame.display.flip()
        clock.tick(30)  # Limit to 30 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
