import numpy as np
import pygame
from agent import Student  # Import the Student class from agent.py


class Environment:
    def __init__(self, num_classes, num_students, num_time_slots):
        """
        Initialize the environment with:
        - num_classes: Total number of classes
        - num_students: Total number of students
        - num_time_slots: Total number of available time slots
        """
        self.num_classes = num_classes
        self.num_students = num_students
        self.num_time_slots = num_time_slots

        # Randomly initialize class durations and priorities
        self.class_durations = np.random.randint(1, 3, size=num_classes)  # 1-2 hours
        self.class_priorities = np.random.randint(1, 6, size=num_classes)  # Priority 1-5

        # Generate students with random availability and preferences
        self.students = self.generate_students()

    def generate_students(self):
        """Generate students with random availability and preferences."""
        students = []
        for i in range(self.num_students):
            # Random availability: 1 means available, 0 means unavailable
            availability = np.random.randint(0, 2, size=self.num_time_slots)
            # Random preferences: Scale 1-5 for each time slot
            preferences = {slot: np.random.randint(1, 6) for slot in range(self.num_time_slots)}
            students.append(Student(id=i, availability=availability, preferences=preferences))
        return students

    def generate_population(self, population_size):
        """
        Generate random initial schedules for the population.
        Each schedule is represented as a list where the index is the class ID,
        and the value is the assigned student ID.
        """
        return [np.random.randint(0, self.num_students, size=self.num_classes) for _ in range(population_size)]

    def draw_schedule(self, screen, font, schedule):
        """
        Visualize the schedule on the Pygame screen.
        - Highlight conflicts and priorities.
        - Display assigned students and their preferences.
        """
        screen.fill((255, 255, 255))  # Background color
        cell_size = 60
        margin_left = 150
        margin_top = 100

        # Draw class labels
        for class_id in range(self.num_classes):
            class_text = font.render(f"Class {class_id + 1}", True, (0, 0, 0))
            screen.blit(class_text, (margin_left - 120, margin_top + class_id * cell_size + 10))

        # Draw time slot labels
        for time_slot in range(self.num_time_slots):
            slot_text = font.render(f"Slot {time_slot + 1}", True, (0, 0, 0))
            screen.blit(slot_text, (margin_left + time_slot * cell_size + 10, margin_top - 30))

        # Draw grid and schedule
        for class_id in range(self.num_classes):
            assigned_student = schedule[class_id]
            for time_slot in range(self.num_time_slots):
                # Determine cell color
                if self.students[assigned_student].availability[time_slot] == 0:
                    color = (255, 0, 0)  # Conflict (student unavailable)
                elif time_slot in self.students[assigned_student].preferences:
                    color = (0, 255, 0)  # Preferred time slot
                else:
                    color = (200, 200, 200)  # Neutral

                # Draw grid cell
                cell_rect = pygame.Rect(
                    margin_left + time_slot * cell_size,
                    margin_top + class_id * cell_size,
                    cell_size,
                    cell_size,
                )
                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # Border

                # Display student ID and class priority
                student_text = font.render(f"S{assigned_student}", True, (0, 0, 0))
                priority_text = font.render(f"P{self.class_priorities[class_id]}", True, (0, 0, 0))
                screen.blit(student_text, (cell_rect.x + 5, cell_rect.y + 5))
                screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 25))