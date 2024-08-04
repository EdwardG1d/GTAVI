import pgzrun
from random import choice, randint
import pygame

pygame.init()
pygame.mixer.music.load("sounds/sound1.wav")
pygame.mixer.music.play(-1)  # -1 означает, что музыка будет играть бесконечно мейби)

collision_sound = pygame.mixer.Sound("sounds/sound2.wav")

TITLE = 'SPACE SURVIVAL'
WIDTH = 550
HEIGHT = 861

# Загрузка изображений!!!
bg = Actor('bg_space.png')
astronaut = Actor('astronaut2')  # Начальное изображение???
ship = Actor('ship')
astronaut.pos = (451, 748)
ship.pos = (450, 80)

coordinates = [(80, 63), (288, 176), (90, 258), (428, 293),
               (219, 388), (80, 528), (358, 541), (195, 691)]
obstacles = []

class Explosion:
    def __init__(self, x, y):
        # Кадры анимации
        self.frames = [Actor(f'exp/{i}.png') for i in range(1, 8)]
        for frame in self.frames:
            frame.pos = (x, y)
        self.current_frame = 0
        self.frame_delay = 0.1
        self.elapsed_time = 0
        self.finished = False

    def update(self, dt):
        if not self.finished:
            self.elapsed_time += dt
            if self.elapsed_time >= self.frame_delay:
                self.elapsed_time = 0
                self.current_frame += 1
                if self.current_frame >= len(self.frames):
                    self.finished = True
                else:
                    self.frames[self.current_frame].pos = (self.frames[0].x, self.frames[0].y)

    def draw(self):
        if not self.finished:
            self.frames[self.current_frame].draw()

# Инициализация анимации астронавта тут
astronaut.animation_frames = [pygame.image.load(f'images/astronaut{i}.png') for i in range(2, 9)]
astronaut.current_frame = 0
astronaut.frame_delay = 0.1
astronaut.elapsed_time = 0

for coordinate in coordinates:
    img = choice(['asteroid1', 'asteroid2'])
    obj = Actor(img)
    obj.pos = coordinate
    obj.angle = randint(0, 360)
    obj.speed_x = choice([-0.2, 0.2])
    obj.speed_y = choice([-0.2, 0.2])
    obj.rotation_speed = choice([-1, 1])
    obj.explosion = None  # Взрыв БУМ
    obstacles.append(obj)

x, y = 0, 0
game_over = False
win = False
menu = True
sound_on = True

buttons = {
    "start": Rect((WIDTH // 2 - 100, HEIGHT // 2 - 100), (200, 50)),
    "toggle_sound": Rect((WIDTH // 2 - 100, HEIGHT // 2), (200, 50)),
    "exit": Rect((WIDTH // 2 - 100, HEIGHT // 2 + 100), (200, 50))
}

def draw():
    bg.draw()
    if menu:
        draw_menu()
    else:
        if game_over:
            screen.draw.text(f'GAME OVER', center=(WIDTH//2, HEIGHT//2), color='red', fontsize=100)
            return
        if win:
            screen.draw.text(f'ПОБЕДА!', center=(WIDTH//2, HEIGHT//2), color='green', fontsize=100)
            return
        draw_actor(astronaut)
        ship.draw()
        for obstacle in obstacles:
            obstacle.draw()
            if obstacle.explosion:
                obstacle.explosion.draw()

def draw_menu():
    screen.draw.text('SPACE SURVIVAL', center=(WIDTH // 2, HEIGHT // 4), color='white', fontsize=60)
    screen.draw.filled_rect(buttons["start"], 'green')
    screen.draw.text("Начать игру", center=buttons["start"].center, color='white', fontsize=40)
    screen.draw.filled_rect(buttons["toggle_sound"], 'blue')
    sound_text = "Выкл звуки" if sound_on else "Вкл звуки"
    screen.draw.text(sound_text, center=buttons["toggle_sound"].center, color='white', fontsize=40)
    screen.draw.filled_rect(buttons["exit"], 'red')
    screen.draw.text("Выход", center=buttons["exit"].center, color='white', fontsize=40)

def draw_actor(actor):
    image = actor.animation_frames[actor.current_frame]
    rect = image.get_rect(center=actor.pos)
    screen.surface.blit(image, rect)

def update(dt):
    global game_over, win
    if not menu:
        astronaut.elapsed_time += dt
        if astronaut.elapsed_time >= astronaut.frame_delay:
            astronaut.elapsed_time = 0
            astronaut.current_frame += 1
            if astronaut.current_frame >= len(astronaut.animation_frames):
                astronaut.current_frame = 0


        astronaut.x += x
        astronaut.y += y
        if astronaut.left < 0:
            astronaut.left = 0
        if astronaut.right > WIDTH:
            astronaut.right = WIDTH
        if astronaut.top < 0:
            astronaut.top = 0
        if astronaut.bottom > HEIGHT:
            astronaut.bottom = HEIGHT
        if astronaut.collidelist(obstacles) != -1:
            game_over = True
            collision_sound.play()  
        if astronaut.colliderect(ship):
            win = True

        for obstacle in obstacles:
            obstacle.x += obstacle.speed_x
            obstacle.y += obstacle.speed_y
            obstacle.angle += obstacle.rotation_speed

            
            if obstacle.left < 0 or obstacle.right > WIDTH:
                obstacle.speed_x = -obstacle.speed_x
                collision_sound.play()  # Проигрывание звука при столкновении с экраном типа
                if not obstacle.explosion:
                    obstacle.explosion = Explosion(obstacle.x, obstacle.y)
            if obstacle.top < 0 or obstacle.bottom > HEIGHT:
                obstacle.speed_y = -obstacle.speed_y
                collision_sound.play()  
                if not obstacle.explosion:
                    obstacle.explosion = Explosion(obstacle.x, obstacle.y)

            if obstacle.explosion:
                obstacle.explosion.update(dt)

def on_mouse_down(button, pos):
    global menu, sound_on
    if menu:
        if buttons["start"].collidepoint(pos):
            menu = False
        elif buttons["toggle_sound"].collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()
        elif buttons["exit"].collidepoint(pos):
            exit()

def on_key_down(key):
    global x, y
    if not menu:
        if key == keys.DOWN:
            y = 0.5
        if key == keys.UP:
            y = -0.5
        if key == keys.LEFT:
            x = -0.5
        if key == keys.RIGHT:
            x = 0.5

def on_key_up(key):
    global x, y
    if not menu:
        if key == keys.DOWN or key == keys.UP:
            y = 0
        if key == keys.LEFT or key == keys.RIGHT:
            x = 0

pgzrun.go()









