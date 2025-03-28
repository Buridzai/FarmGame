import pygame

# Khởi tạo pygame
pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Nông Trại")

ground_img = pygame.image.load("ground.png")
ground_img = pygame.transform.scale(ground_img, (WIDTH, HEIGHT))

water_img = pygame.image.load("water.png")
water_img = pygame.transform.scale(water_img, (1000, 100))  # Giảm kích thước nước
water_img.set_alpha(10)  # Làm trong suốt nước

character_img = pygame.image.load("character.png")
character_img = pygame.transform.scale(character_img, (32, 32))  # Giảm kích thước nhân vật

plant_stage_0 = pygame.transform.scale(pygame.image.load("0.png"), (32, 32))
plant_stage_1 = pygame.transform.scale(pygame.image.load("1.png"), (32, 32))
plant_stage_2 = pygame.transform.scale(pygame.image.load("2.png"), (32, 32))
plant_stage_3 = pygame.transform.scale(pygame.image.load("3.png"), (32, 32))

BROWN = (139, 69, 19)  # Màu đất
PLOT_SIZE = 40  # Kích thước ô đất

character_x = WIDTH // 2
character_y = HEIGHT // 2
speed = 5  # Tốc độ di chuyển

# Danh sách ô đất đã cuốc và cây trồng
plowed_land = []
planted_trees = {}  
watered_plants = {} 

# Vùng nước (điều chỉnh lại vị trí cho phù hợp)
water_tiles = [(450, 100), (100, 500)]  

def is_in_water(x, y):
    for water_x, water_y in water_tiles:
        if water_x <= x <= water_x + 100 and water_y <= y <= water_y + 100:
            return True
    return False

energy = 100
ENERGY_DECREASE = 5  
ENERGY_RECOVER = 2  


GROWTH_STAGE_1 = 5000  
GROWTH_STAGE_2 = 7000  
GROWTH_STAGE_3 = 10000 


score = 0
font = pygame.font.Font(None, 36)  # Font hiển thị điểm số

# Hệ thống nhiệm vụ
quests = [
    {"task": "Trồng 5 cây", "goal": 5, "progress": 0, "reward": 20},
    {"task": "Thu hoạch 3 cây", "goal": 3, "progress": 0, "reward": 30},
]

def check_quests():
    global score
    for quest in quests:
        if quest["progress"] >= quest["goal"]:
            score += quest["reward"]
            print(f"🏆 Hoàn thành nhiệm vụ: {quest['task']}! +{quest['reward']} điểm")
            quests.remove(quest)

# Vòng lặp game
running = True
while running:
    pygame.time.delay(30)  # Giúp game chạy mượt hơn

    # Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.KEYDOWN:
            pos = (character_x // PLOT_SIZE * PLOT_SIZE, character_y // PLOT_SIZE * PLOT_SIZE)

            if event.key == pygame.K_SPACE:  # Nhấn Space để cuốc đất
                if pos not in plowed_land and not is_in_water(pos[0], pos[1]) and energy > 0:
                    plowed_land.append(pos)
                    energy -= ENERGY_DECREASE

            if event.key == pygame.K_RETURN:  # Nhấn Enter để trồng cây
                if pos in plowed_land and pos not in planted_trees and energy > 0:
                    planted_trees[pos] = pygame.time.get_ticks()
                    watered_plants[pos] = False
                    energy -= ENERGY_DECREASE

            if event.key == pygame.K_x:  # Nhấn X để thu hoạch
                if pos in planted_trees:
                    time_elapsed = pygame.time.get_ticks() - planted_trees[pos]
                    if time_elapsed >= GROWTH_STAGE_3:
                        del planted_trees[pos]
                        del watered_plants[pos]
                        score += 10
                        print(f"🌱 Đã thu hoạch cây! +10 điểm (Tổng điểm: {score})")

            if event.key == pygame.K_c:  # Nhấn C để tưới nước
                if pos in planted_trees:
                    watered_plants[pos] = True

   
    if not any(pygame.key.get_pressed()):
        energy = min(100, energy + ENERGY_RECOVER)

    check_quests()

   # Lấy phím đang nhấn
    keys = pygame.key.get_pressed()
    new_x, new_y = character_x, character_y
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        new_x = max(0, character_x - speed)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        new_x = min(WIDTH - 32, character_x + speed)
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        new_y = max(0, character_y - speed)
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        new_y = min(HEIGHT - 32, character_y + speed)
    
    if not is_in_water(new_x, new_y):
        character_x, character_y = new_x, new_y

    # Hiển thị điểm số và năng lượng
    screen.blit(ground_img, (0, 0))
    for pos in water_tiles:
        screen.blit(water_img, pos)
    for pos in plowed_land:
        pygame.draw.rect(screen, BROWN, (pos[0], pos[1], PLOT_SIZE, PLOT_SIZE))
    for pos, start_time in planted_trees.items():
        time_elapsed = pygame.time.get_ticks() - start_time
        if time_elapsed >= GROWTH_STAGE_3:
            screen.blit(plant_stage_3, (pos[0], pos[1]))
        elif time_elapsed >= GROWTH_STAGE_2:
            screen.blit(plant_stage_2, (pos[0], pos[1]))
        elif time_elapsed >= GROWTH_STAGE_1:
            screen.blit(plant_stage_1, (pos[0], pos[1]))
        else:
            screen.blit(plant_stage_0, (pos[0], pos[1]))
    screen.blit(character_img, (character_x, character_y))
    score_text = font.render(f"Score: {score}  Energy: {energy}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.update()

pygame.quit()
