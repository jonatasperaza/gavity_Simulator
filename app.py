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
THETA = 0.5  # Critério de precisão do Barnes-Hut (quanto maior, menos preciso mas mais rápido)

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
        self.radius = int(math.sqrt(self.radius + other.radius + total_mass))  # Ajusta o raio com base na massa
        other.mass = 0  # Define a massa do outro corpo como 0

    def draw(self):
        """Desenha o corpo e as forças atuando nele."""
        # Desenha o corpo
        pygame.draw.circle(SCREEN, self.color, (int(self.x), int(self.y)), self.radius)

        # Desenha os vetores de força
        pygame.draw.line(
            SCREEN, RED, (int(self.x), int(self.y)),
            (int(self.x + self.vx * 10), int(self.y)), 2  # Componente X
        )
        pygame.draw.line(
            SCREEN, GREEN, (int(self.x), int(self.y)),
            (int(self.x), int(self.y + self.vy * 10)), 2  # Componente Y
        )

# Classe QuadTree: Para dividir o espaço e usar o algoritmo de Barnes-Hut
class QuadTree:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bodies = []
        self.divided = False
        self.mass = 0
        self.center_of_mass = (0, 0)

    def insert(self, body):
        if not self.in_boundary(body):
            return False

        if len(self.bodies) < 4:
            self.bodies.append(body)
            self.mass += body.mass
            self.center_of_mass = ((self.center_of_mass[0] * (self.mass - body.mass) + body.x * body.mass) / self.mass,
                                   (self.center_of_mass[1] * (self.mass - body.mass) + body.y * body.mass) / self.mass)
            return True

        if not self.divided:
            self.subdivide()

        if self.nw.insert(body) or self.ne.insert(body) or self.sw.insert(body) or self.se.insert(body):
            return True
        return False

    def subdivide(self):
        half_width = self.width / 2
        half_height = self.height / 2
        self.nw = QuadTree(self.x, self.y, half_width, half_height)
        self.ne = QuadTree(self.x + half_width, self.y, half_width, half_height)
        self.sw = QuadTree(self.x, self.y + half_height, half_width, half_height)
        self.se = QuadTree(self.x + half_width, self.y + half_height, half_width, half_height)
        self.divided = True

    def in_boundary(self, body):
        return self.x <= body.x < self.x + self.width and self.y <= body.y < self.y + self.height

    def calculate_gravity(self, body, theta):
        """Calcula a força gravitacional com o Algoritmo de Barnes-Hut"""

        # Se for uma folha e não tem corpos, retorna a força gravitacional como 0
        if not self.divided:
            total_fx, total_fy = 0, 0
            for b in self.bodies:
                if b != body:
                    dx = b.x - body.x
                    dy = b.y - body.y
                    distance = math.sqrt(dx**2 + dy**2) + 1e-18  # Evita divisão por zero

                    force = G * b.mass * body.mass / (distance**2)

                    fx = force * (dx / distance)
                    fy = force * (dy / distance)

                    total_fx += fx
                    total_fy += fy

            return total_fx, total_fy

        else:
            # Se a massa total dividida for grande o suficiente para não fazer a iteração recursiva
            dx = self.center_of_mass[0] - body.x
            dy = self.center_of_mass[1] - body.y
            distance = math.sqrt(dx**2 + dy**2) + 1e-18

            # Verifica se o quadrante é suficientemente distante para aplicar uma aproximação
            if (self.width / distance) < theta:
                force = G * self.mass * body.mass / (distance**2)

                fx = force * (dx / distance)
                fy = force * (dy / distance)

                return fx, fy
            else:
                # Chama recursivamente para todos os quadrantes divididos
                total_fx, total_fy = 0, 0
                fx, fy = self.nw.calculate_gravity(body, theta)
                total_fx += fx
                total_fy += fy

                fx, fy = self.ne.calculate_gravity(body, theta)
                total_fx += fx
                total_fy += fy

                fx, fy = self.sw.calculate_gravity(body, theta)
                total_fx += fx
                total_fy += fy

                fx, fy = self.se.calculate_gravity(body, theta)
                total_fx += fx
                total_fy += fy

                return total_fx, total_fy
    

# Função principal
def main():
    clock = pygame.time.Clock()
    bodies = [
        Body(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100), 
             mass=random.uniform(10, 20), radius=random.randint(5, 10), color=WHITE)
        for _ in range(10)
    ]
    
    # Inicializa o quadtree
    quadtree = QuadTree(0, 0, WIDTH, HEIGHT)
    for body in bodies:
        quadtree.insert(body)

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

        # Calcula gravidade e aplica
        for body in bodies:
            quadtree = QuadTree(0, 0, WIDTH, HEIGHT)  # reinicia a árvore para cada atualização
            for other_body in bodies:
                if other_body != body:
                    quadtree.insert(other_body)
            fx, fy = quadtree.calculate_gravity(body, THETA)
            body.vx += fx / body.mass
            body.vy += fy / body.mass

        # Verifica colisões e mescla os corpos
        for i, body in enumerate(bodies):
            for j in range(i + 1, len(bodies)):
                other_body = bodies[j]
                if body.check_collision(other_body):
                    body.merge(other_body)

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
