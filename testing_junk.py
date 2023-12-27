import pygame
import numpy as np
import random



# Global variables
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (50, 168, 82)
FPS = 60
PLANT_ENERGY = 100
ANIMAL_ENERGY = 150
REPRODUCE_ENERGY = 200
EAT_ENERGY_GAIN = 50
ANIMAL_SIZE = 5
PLANT_SIZE = 2
FONT_COLOR = (255, 255, 255)

# Entity classes
class Plant:
    def __init__(self, x, y):
        self.pos = np.array([x, y])
        self.energy = PLANT_ENERGY

    def draw(self, window):
        pygame.draw.circle(window, (0, 128, 0), self.pos.astype(int), PLANT_SIZE)

class Animal:
    def __init__(self, x, y, speed):
        self.pos = np.array([x, y], dtype=float)
        self.energy = ANIMAL_ENERGY
        self.speed = speed

    def move_towards(self, target_pos):
        direction = target_pos - self.pos
        distance = np.linalg.norm(direction)
        if distance != 0:
            direction = direction / distance  # Normalize
            self.pos += direction * self.speed

        self.pos = np.clip(self.pos, [0, 0], [WIDTH, HEIGHT])

    def move(self, target=None):
        if target:
            self.move_towards(target.pos)
        else:
            random_direction = np.random.rand(2) * 2 - 1  # Vector with direction -1 to 1
            self.move_towards(self.pos + random_direction * self.speed)
        self.energy -= 1

    def detect_food(self, food_list, sight_distance):
        if not food_list:
            return None
        positions = np.array([food.pos for food in food_list])
        distances = np.linalg.norm(positions - self.pos, axis=1)
        closest_idx = np.argmin(distances)
        if distances[closest_idx] < sight_distance:
            return food_list[closest_idx]
        return None

    def eat(self, food_list):
        if not food_list:
            return
        distances = np.linalg.norm(np.array([food.pos for food in food_list]) - self.pos, axis=1)
        collision = np.where(distances < 10)[0]
        if collision.size > 0:
            self.energy += EAT_ENERGY_GAIN
            del food_list[collision[0]]

    def reproduce(self):
        if self.energy >= REPRODUCE_ENERGY:
            self.energy /= 2
            return type(self)(self.pos[0], self.pos[1], self.speed)
        return None

    def draw(self, window):
        pass  # Define in subclasses

    def draw_energy_bar(self, window):
        bar_width = 10
        bar_height = 2
        fill = (self.energy / ANIMAL_ENERGY) * bar_width
        outline_rect = pygame.Rect(self.pos[0] - bar_width // 2, self.pos[1] + 8, bar_width, bar_height)
        fill_rect = pygame.Rect(self.pos[0] - bar_width // 2, self.pos[1] + 8, fill, bar_height)
        pygame.draw.rect(window, (255, 0, 0), fill_rect)
        pygame.draw.rect(window, (0, 0, 0), outline_rect, 1)

class Herbivore(Animal):
    def draw(self, window):
        pygame.draw.circle(window, (200, 200, 200), self.pos.astype(int), ANIMAL_SIZE)
        self.draw_energy_bar(window)

class Carnivore(Animal):
    def draw(self, window):
        pygame.draw.circle(window, (139, 0, 0), self.pos.astype(int), ANIMAL_SIZE)
        self.draw_energy_bar(window)

def regrow_plants(plants, chance):
    if random.random() < chance:
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        plants.append(Plant(x, y))

def draw_text(window, text, position, font_size=24):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, FONT_COLOR)
    window.blit(text_surface, position)

def start_menu():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ecosystem Simulation - Start Menu")
    clock = pygame.time.Clock()

    # Default values
    num_herbivores = 50
    num_carnivores = 25
    num_plants = 300
    plant_growth_rate = 0.05

    input_active = False
    current_input = ""
    input_type = None

    running = True
    while running:
        window.fill(BG_COLOR)
        draw_text(window, "Press 1 to set the number of herbivores: " + str(num_herbivores), (50, 50))
        draw_text(window, "Press 2 to set the number of carnivores: " + str(num_carnivores), (50, 100))
        draw_text(window, "Press 3 to set the number of plants: " + str(num_plants), (50, 150))
        draw_text(window, "Press 4 to set the plant growth rate: " + str(plant_growth_rate), (50, 200))
        draw_text(window, "Press Enter to start simulation", (50, 250))

        if input_active:
            draw_text(window, "Enter value for " + input_type + ":", (50, 300))
            draw_text(window, current_input, (50, 350), font_size=32)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return None  # User closed the window

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_active:
                        # Process input
                        if input_type == "herbivores":
                            num_herbivores = int(current_input)
                        elif input_type == "carnivores":
                            num_carnivores = int(current_input)
                        elif input_type == "plants":
                            num_plants = int(current_input)
                        elif input_type == "growth rate":
                            plant_growth_rate = float(current_input)
                        input_active = False
                        current_input = ""
                    else:
                        # Start the simulation
                        pygame.quit()
                        return num_herbivores, num_carnivores, num_plants, plant_growth_rate

                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                    else:
                        current_input += event.unicode

                # Activate input for specific settings
                if event.key == pygame.K_1:
                    input_active = True
                    input_type = "herbivores"
                elif event.key == pygame.K_2:
                    input_active = True
                    input_type = "carnivores"
                elif event.key == pygame.K_3:
                    input_active = True
                    input_type = "plants"
                elif event.key == pygame.K_4:
                    input_active = True
                    input_type = "growth rate"

        pygame.display.flip()
        clock.tick(FPS)

def main():
    settings = start_menu()
    if settings is None:
        return  # User closed the window

    num_herbivores, num_carnivores, num_plants, plant_growth_rate = settings

    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ecosystem Simulation")
    clock = pygame.time.Clock()

    plants = [Plant(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num_plants)]
    herbivores = [Herbivore(random.randint(0, WIDTH), random.randint(0, HEIGHT), 2) for _ in range(num_herbivores)]
    carnivores = [Carnivore(random.randint(0, WIDTH), random.randint(0, HEIGHT), 2) for _ in range(num_carnivores)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.fill(BG_COLOR)
        regrow_plants(plants, plant_growth_rate)

        for plant in plants:
            plant.draw(window)

        for herbivore in herbivores[:]:
            food_target = herbivore.detect_food(plants, 150)
            herbivore.move(food_target)
            herbivore.eat(plants)
            child = herbivore.reproduce()
            if child:
                herbivores.append(child)
            if herbivore.energy <= 0:
                herbivores.remove(herbivore)
            else:
                herbivore.draw(window)

        for carnivore in carnivores[:]:
            food_target = carnivore.detect_food(herbivores, 150)
            carnivore.move(food_target)
            carnivore.eat(herbivores)
            child = carnivore.reproduce()
            if child:
                carnivores.append(child)
            if carnivore.energy <= 0:
                carnivores.remove(carnivore)
            else:
                carnivore.draw(window)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
