import pygame, random, math, sys

pygame.init()
WIDTH, HEIGHT = 1000, 650
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✈️ VIP Climate Flight")

# Font
font = pygame.font.SysFont("arial", 26, True)
big_font = pygame.font.SysFont("arial", 48, True)

# Màu
WHITE = (255, 255, 255)
BLUE1 = (120, 170, 255)
BLUE2 = (10, 40, 100)
RED = (255, 80, 80)
YELLOW = (255, 255, 100)
GREEN = (80, 255, 100)

# Background gradient
def draw_background():
    for y in range(HEIGHT):
        r = BLUE1[0] + (BLUE2[0] - BLUE1[0]) * (y / HEIGHT)
        g = BLUE1[1] + (BLUE2[1] - BLUE1[1]) * (y / HEIGHT)
        b = BLUE1[2] + (BLUE2[2] - BLUE1[2]) * (y / HEIGHT)
        pygame.draw.line(win, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

# Danh sách thành phố thật
cities = [
    {"name": "Tokyo", "pos": (880, 260), "weather": "sunny"},
    {"name": "Seoul", "pos": (830, 240), "weather": "sunny"},
    {"name": "Hanoi", "pos": (780, 310), "weather": "rainy"},
    {"name": "Singapore", "pos": (750, 400), "weather": "sunny"},
    {"name": "Dubai", "pos": (640, 320), "weather": "sunny"},
    {"name": "Moscow", "pos": (620, 180), "weather": "snowy"},
    {"name": "London", "pos": (500, 200), "weather": "rainy"},
    {"name": "Paris", "pos": (510, 250), "weather": "sunny"},
    {"name": "Rome", "pos": (530, 280), "weather": "sunny"},  # VIP CITY
    {"name": "New York", "pos": (250, 300), "weather": "rainy"},
    {"name": "Toronto", "pos": (230, 270), "weather": "snowy"},
    {"name": "Sydney", "pos": (880, 500), "weather": "sunny"}
]

vip_city = "Rome"
fuel = 15
visited = []
flight_stage = 0
game_over = False
message = ""

# Máy bay
plane_img = pygame.Surface((30, 20), pygame.SRCALPHA)
pygame.draw.polygon(plane_img, YELLOW, [(0, 10), (30, 5), (30, 15)])
plane_pos = list(random.choice(cities)["pos"])
current_city = None

def draw_fuel_bar():
    pygame.draw.rect(win, WHITE, (20, 20, 200, 20), 2)
    pygame.draw.rect(win, GREEN if fuel > 4 else RED, (22, 22, (fuel / 15) * 196, 16))

def draw_text():
    if current_city:
        txt = font.render(f"City: {current_city['name']} | Weather: {current_city['weather']} | Fuel: {fuel}", True, WHITE)
        win.blit(txt, (20, 60))
    if message:
        msg = big_font.render(message, True, YELLOW)
        win.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 550))

def distance(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])

def fly_to_city(target):
    global plane_pos, fuel, message, flight_stage, current_city, visited
    start = plane_pos[:]
    end = target["pos"]
    steps = 60
    message = ""

    # Trừ fuel
    loss = 3
    if target["weather"] == "rainy":
        loss += 1
    elif target["weather"] == "snowy" and random.random() < 0.3:
        loss += 2
    fuel -= loss
    if fuel <= 0:
        fuel = 0
        return "out"

    # Animation bay
    for i in range(steps + 1):
        t = i / steps
        plane_pos[0] = start[0] + (end[0] - start[0]) * t
        plane_pos[1] = start[1] + (end[1] - start[1]) * t
        draw_background()
        for c in cities:
            color = GREEN if c["name"] == vip_city else WHITE
            pygame.draw.circle(win, color, c["pos"], 6)
        win.blit(plane_img, plane_pos)
        draw_fuel_bar()
        draw_text()
        pygame.display.update()
        pygame.time.delay(15)

    # Đến thành phố
    current_city = target
    visited.append(target["name"])
    flight_stage += 1

    # Check điều kiện
    if current_city["name"] == vip_city:
        if flight_stage >= 4:
            message = f"🏆 You reached {vip_city}! Perfect climate found!"
            return "win"
        else:
            message = "Too early! Keep flying..."
            return "early"
    return "ok"

# City đầu tiên
current_city = random.choice(cities)
plane_pos = list(current_city["pos"])
visited.append(current_city["name"])

# Vòng lặp chính
run = True
next_options = random.sample([c for c in cities if c != current_city], 3)

while run:
    draw_background()
    for c in cities:
        color = GREEN if c["name"] == vip_city else WHITE
        pygame.draw.circle(win, color, c["pos"], 6)
    win.blit(plane_img, plane_pos)
    draw_fuel_bar()
    draw_text()

    # Lựa chọn thành phố
    if not game_over:
        for i, opt in enumerate(next_options):
            txt = font.render(f"[{i+1}] {opt['name']} ({opt['weather']})", True, WHITE)
            win.blit(txt, (20, 120 + i * 40))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if not game_over:
        for i in range(3):
            if keys[pygame.K_1 + i]:
                result = fly_to_city(next_options[i])
                if result == "win":
                    game_over = True
                elif result == "out":
                    message = "💀 Out of fuel!"
                    game_over = True
                else:
                    next_options = random.sample(
                        [c for c in cities if c["name"] not in visited],
                        3 if len(cities) - len(visited) >= 3 else len(cities) - len(visited)
                    )
                pygame.time.wait(200)
                break
