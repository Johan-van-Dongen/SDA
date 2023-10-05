import pygame
import random
import math
import abc

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shape Clicker")

# Font for displaying area
font = pygame.font.Font(None, 36)

# Shape base class
class Shape(metaclass=abc.ABCMeta):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    @abc.abstractmethod
    def draw(self, surface):
        pass

    @abc.abstractmethod
    def get_type(self):
        pass

    @abc.abstractmethod
    def get_area(self):
        pass

    @abc.abstractmethod
    def clicked_inside(self, click_x, click_y):
        pass

class Square(Shape):
    def __init__(self, x, y, color, side_length):
        super().__init__(x, y, color)
        self.side_length = side_length

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.side_length, self.side_length))

    def get_type(self):
        return "Square"

    def get_area(self):
        return self.side_length ** 2

    def clicked_inside(self, click_x, click_y):
        return self.x <= click_x <= self.x + self.side_length and self.y <= click_y <= self.y + self.side_length

class Circle(Shape):
    def __init__(self, x, y, color, radius):
        super().__init__(x, y, color)
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def get_type(self):
        return "Circle"

    def get_area(self):
        return math.pi * self.radius ** 2

    def clicked_inside(self, click_x, click_y):
        distance = math.sqrt((self.x - click_x) ** 2 + (self.y - click_y) ** 2)
        return distance <= self.radius

class Triangle(Shape):
    def __init__(self, x, y, color, side_length):
        super().__init__(x, y, color)
        self.side_length = side_length

    def draw(self, surface):
        height = (math.sqrt(3) / 2) * self.side_length
        points = [(self.x, self.y + height), (self.x + self.side_length, self.y + height),
                  (self.x + self.side_length / 2, self.y)]
        pygame.draw.polygon(surface, self.color, points)

    def get_type(self):
        return "Triangle"

    def get_area(self):
        return (math.sqrt(3) / 4) * self.side_length ** 2

    def clicked_inside(self, click_x, click_y):
        height = (math.sqrt(3) / 2) * self.side_length
        p0 = (self.x, self.y + height)
        p1 = (self.x + self.side_length, self.y + height)
        p2 = (self.x + self.side_length / 2, self.y)

        v0 = (p2[0] - p0[0], p2[1] - p0[1])
        v1 = (p1[0] - p0[0], p1[1] - p0[1])
        v2 = (click_x - p0[0], click_y - p0[1])

        dot00 = v0[0] * v0[0] + v0[1] * v0[1]
        dot01 = v0[0] * v1[0] + v0[1] * v1[1]
        dot02 = v0[0] * v2[0] + v0[1] * v2[1]
        dot11 = v1[0] * v1[0] + v1[1] * v1[1]
        dot12 = v1[0] * v2[0] + v1[1] * v2[1]

        inv_denom = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom

        return (u >= 0) and (v >= 0) and (u + v <= 1)

# Main loop
shapes = []

for _ in range(10):
    x = random.randint(0, WINDOW_WIDTH)
    y = random.randint(0, WINDOW_HEIGHT)
    color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    shape_type = random.choice(["Square", "Circle", "Triangle"])
    
    if shape_type == "Square":
        shape = Square(x, y, color, random.randint(20, 100))
    elif shape_type == "Circle":
        shape = Circle(x, y, color, random.randint(10, 50))
    elif shape_type == "Triangle":
        shape = Triangle(x, y, color, random.randint(20, 100))
    
    shapes.append(shape)

clicked_shape = None  # Stores the clicked shape

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click_x, click_y = pygame.mouse.get_pos()
            for shape in shapes:
                if shape.clicked_inside(click_x, click_y):
                    clicked_shape = shape  # Store the clicked shape
                    break
            else:
                clicked_shape = None  # Reset if no shape is clicked

    screen.fill((255, 255, 255))
    for shape in shapes:
        shape.draw(screen)

    if clicked_shape:
        area_text = f"Area: {clicked_shape.get_area():.2f}"
        text_surface = font.render(area_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))

    pygame.display.update()
    pygame.time.Clock().tick(FPS)

pygame.quit()
