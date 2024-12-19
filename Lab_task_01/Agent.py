class Agent:
    def __init__(self, name, environment, position=(0, 0), speed=5):
        self.name = name
        self.environment = environment
        self.position = list(position)  # Initial position (x, y)
        self.speed = speed  # Movement speed of the agent

    def move(self, direction):
        """Move the agent in the specified direction."""
        if direction == "up":
            self.position[1] -= self.speed
        elif direction == "down":
            self.position[1] += self.speed
        elif direction == "left":
            self.position[0] -= self.speed
        elif direction == "right":
            self.position[0] += self.speed
        # Ensure position stays within environment boundaries
        self.position = self.environment.limit_position(self.position)

    def get_position(self):
        return self.position