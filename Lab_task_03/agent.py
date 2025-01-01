import numpy as np

class Student:
    def __init__(self, id, availability, preferences):
        """
        Initialize a student with:
        - id: Unique identifier
        - availability: List of available time slots (binary array)
        - preferences: Dictionary of preferred time slots with priorities
        - schedule: The assigned schedule for the student
        """
        self.id = id
        self.availability = availability
        self.preferences = preferences
        self.schedule = []

    def assign_class(self, class_id, time_slot):
        """Assign a class to the student at a specific time slot."""
        if self.availability[time_slot] == 1:
            self.schedule.append((class_id, time_slot))

    def clear_schedule(self):
        """Clear the student's schedule."""
        self.schedule = []
