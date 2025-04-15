import pygame
import math 
import random

# Gravitational pull visualized in 2d using pygame 
Screen_size = (800, 600)

# Constant 
G = 1

pygame.init()
screen = pygame.display.set_mode(Screen_size)
pygame.display.set_caption("Gravitational Pull Simulation")
clock = pygame.time.Clock()


def draw_particle(screen, pos, color, size):
    pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), size)

def calculate_gravitational_force(m1, m2, r):
    return G * (m1 * m2) / (r ** 2)

def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def calculate_force_vector(p1, p2, m1, m2):
    distance = calculate_distance(p1, p2)

    if distance == 0:
        return (0, 0)
    else:
        force_magnitude = calculate_gravitational_force(m1, m2, distance)
        force_x = force_magnitude * (p2[0] - p1[0]) / distance
        force_y = force_magnitude * (p2[1] - p1[1]) / distance
        return (force_x, force_y)
    
class Particle:
    def __init__(self, x, y, earth_pos):
        self.pos = [x, y]
        self.vel = [0, 0]
        self.mass = 100 # kg

        distance_x = x - earth_pos[0]
        distance_y = y - earth_pos[1]
        distance = math.hypot(distance_x, distance_y)
        speed = 2 # m/s

        self.vel[0] = -distance_y / distance * speed
        self.vel[1] = distance_x / distance * speed

    
def main():
    running = True 

    particles = []
    Particle_size = 5
    num_particles = 20

    earth_pos = (Screen_size[0] // 2, Screen_size[1] // 2)
    earth_mass = 1300  # In kg
    earth_size = 60

    time_step = 0.1

    for particle in range(num_particles):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randint(200, 300)  # spawn particles in a circle around the earth min 150 max 300
        x = earth_pos[0] + math.cos(angle) * radius
        y = earth_pos[1] + math.sin(angle) * radius
        p = Particle(x, y, earth_pos)
        particles.append(p)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        screen.fill((0, 0, 0)) 
        #print(earth_pos)

        draw_particle(screen , earth_pos, (0, 255, 0), earth_size)  # Draw Earth

        for particle in particles:
            # Calculate the gravitational force 
            force_x, force_y = calculate_force_vector(particle.pos, earth_pos, particle.mass, earth_mass)

            # Acceleration 
            acc_x = force_x / particle.mass
            acc_y = force_y / particle.mass

            # Update velocity 
            particle.vel[0] += acc_x * time_step
            particle.vel[1] += acc_y * time_step

            # Update position 
            particle.pos[0] += particle.vel[0] * time_step
            particle.pos[1] += particle.vel[1] * time_step

            draw_particle(screen, particle.pos, (255, 255, 255), Particle_size)
            #print(particle.pos)

        # Update the screen
        pygame.display.flip()
        clock.tick(144)

main()