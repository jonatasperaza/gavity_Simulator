import pygame
import math
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Gravidade - Algoritmo de Barnes-Hut")

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Configurações do FPS e gravidade simulada
FPS = 60
G = 0.5

# Classe Body: Representa cada objeto
class Body:
    def __init__(self, x, y, mass, radius, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.mass = mass
        self.radius = radius
        self.color = color

    def update_position(self):
        """Atualiza a posição do corpo baseado em sua velocidade."""
        self.x += self.vx
        self.y += self.vy

        # Permitir wrap-around (teletransporte entre bordas)
        self.x %= WIDTH
        self.y %= HEIGHT

    def apply_gravity(self, other):
        """Aplica a gravidade de outro corpo."""
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx**2 + dy**2) + 1 * 10**-18  # Evita divisão por zero

        # Força gravitacional
        force = G * self.mass * other.mass / (distance**2)

        # Componentes de força
        fx = force * (dx / distance)
        fy = force * (dy / distance)

        # Atualiza velocidades
        self.vx += fx / self.mass
        self.vy += fy / self.mass

    def check_collision(self, other):
        """Verifica colisão com outro corpo."""
        distance = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return distance < (self.radius + other.radius)

    def merge(self, other):
        """Mescla dois corpos em uma colisão."""
        total_mass = self.mass + other.mass
        self.vx = (self.vx * self.mass + other.vx * other.mass) / total_mass
        self.vy = (self.vy * self.mass + other.vy * other.mass) / total_mass
        self.mass = total_mass
        self.radius = int(math.sqrt(self.radius + other.radius + total_mass)) # Ajusta o raio com base na massa
        other.mass = 0

    def draw(self):
        """Desenha o corpo e as forças atuando nele."""
        # Desenha o corpo
        pygame.draw.circle(SCREEN, self.color, (int(self.x), int(self.y)), self.radius)

        # Desenha os vetores de força
        pygame.draw.line(
            SCREEN, RED, (int(self.x), int(self.y)), 
            (int(self.x + self.vx * 10), int(self.y)), 2
        )  # Componente X
        pygame.draw.line(
            SCREEN, GREEN, (int(self.x), int(self.y)), 
            (int(self.x), int(self.y + self.vy * 10)), 2
        )  # Componente Y

# Função principal
def main():
    clock = pygame.time.Clock()
    bodies = [
        Body(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 
             mass=random.uniform(10, 20), radius=random.randint(5, 10), color=WHITE)
        for _ in range(10)
    ]

    selected_position = None
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Armazena posição inicial ao clicar
                selected_position = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Libera corpo com velocidade ao soltar clique
                if selected_position:
                    release_position = pygame.mouse.get_pos()
                    vx = (release_position[0] - selected_position[0]) * 0.1
                    vy = (release_position[1] - selected_position[1]) * 0.1
                    new_body = Body(
                        x=selected_position[0], y=selected_position[1],
                        mass=random.uniform(10, 20), radius=random.randint(5, 10), color=BLUE
                    )
                    new_body.vx = vx
                    new_body.vy = vy
                    bodies.append(new_body)
                    selected_position = None

        # Aplica gravidade e resolve colisões
        for i in range(len(bodies)):
            for j in range(i + 1, len(bodies)):
                if bodies[i].mass > 0 and bodies[j].mass > 0:
                    bodies[i].apply_gravity(bodies[j])
                    bodies[j].apply_gravity(bodies[i])

                    # Verifica colisões
                    if bodies[i].check_collision(bodies[j]):
                        bodies[i].merge(bodies[j])
                        bodies[j].mass = 0  # Marca corpo como "absorvido"

        # Atualiza posições e redesenha corpos
        bodies = [body for body in bodies if body.mass > 0]  # Remove corpos absorvidos
        for body in bodies:
            body.update_position()
            body.draw()

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()