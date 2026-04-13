import pygame
import random

pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Catcher")

# Colors
WHITE = (255, 255, 255)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

# Basket
basket_width, basket_height = 100, 20
basket_x = screen_width // 2
basket_y = screen_height - 40
basket_speed = 7

# Fruits
fruits = [RED, YELLOW, ORANGE]
falling_items = []

# Score
score = 0

# High score
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

clock = pygame.time.Clock()

def create_item():
    return {
        "x": random.randint(0, screen_width - 30),
        "y": 0,
        "color": random.choice(fruits),
        "speed": random.randint(3, 6)
    }

running = True
while running:
    screen.fill(WHITE)

    # Controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT]:
        basket_x += basket_speed

    # Draw basket
    pygame.draw.rect(screen, PURPLE, (basket_x, basket_y, basket_width, basket_height))

    # Spawn items
    if len(falling_items) < 5:
        falling_items.append(create_item())

    # Move items
    for item in falling_items[:]:
        item["y"] += item["speed"]
        pygame.draw.circle(screen, item["color"], (item["x"], item["y"]), 15)

        # Catch check
        if basket_y < item["y"] < basket_y + basket_height and basket_x < item["x"] < basket_x + basket_width:
            score += 10
            falling_items.remove(item)

        # Missed
        elif item["y"] > screen_height:
            falling_items.remove(item)

    # Display score
    font = pygame.font.Font(None, 36)
    screen.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
    screen.blit(font.render(f"High Score: {high_score}", True, BLACK), (10, 40))

    pygame.display.update()
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Save high score
if score > high_score:
    with open("high_score.txt", "w") as f:
        f.write(str(score))

pygame.quit()