class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def limit_position(self, position):
        """Keep the agent's position within the environment boundaries without wrapping around."""
        x, y = position
        x = max(0, min(x, self.width - 20))  # Adjusted for agent size
        y = max(0, min(y, self.height - 20))  # Adjusted for agent size
        return [x, y]
