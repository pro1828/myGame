import pygame
import time
import random
from pygame.locals import *

pygame.init()

display_width = 800
display_height = 600

block_height = 117
block_width = 67

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 160, 160)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
red = (200, 0, 0)
green = (0, 150, 0)


block_color = (53, 115, 255)

colors = (blue, green, red)

car_width = 85
car_height = 150

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('igrushka')
clock = pygame.time.Clock()

crash_sound = pygame.mixer.Sound('explosion.wav')
engine_start = pygame.mixer.Sound('engine.wav')

carImg = pygame.image.load('carr1.png')
crashImg = pygame.image.load('crash.png')
bluecar = pygame.image.load('bluecar.png')
redcar = pygame.image.load('redcar.png')
yellowcar = pygame.image.load('yellowcar.png')
greencar = pygame.image.load('greencar.png')
purplecar = pygame.image.load('purplecar.png')
orangecar = pygame.image.load('orangecar.png')
background = pygame.image.load('background.png')

cars = [bluecar, redcar, yellowcar, greencar, purplecar, orangecar]

intro = True
pause = False

gameIcon = pygame.image.load('icon.png')
pygame.display.set_icon(gameIcon)


class Coordinates:
    def __init__(self):
        self.enemies = []
        self.speed = 6
        self.dodged = 0

    def create_enemy(self):
        x_coor = random.randint(0, display_width - block_width)
        y_coor = -200
        coor = [x_coor, y_coor, random.choice(cars)]
        check = 0
        if len(self.enemies) == 0:
            self.enemies.append(coor)
        else:
            for i in self.enemies:
                if abs(x_coor - i[0]) < block_width + car_width + 30 and abs(y_coor - i[1]) < block_height + 20:
                    check = 1
            if check == 0:
                self.enemies.append(coor)

    def enemy_move(self):
        for i in self.enemies:
            if len(self.enemies) > 0:
                if i[1] > display_height+50:
                    del self.enemies[self.enemies.index(i)]
                    self.dodged += 1
                else:
                    i[1] += self.speed
        return self.enemies

    def get_dodged(self):
        return self.dodged

    def get_speed(self):
        return self.speed


def draw_car(carx, cary, car_color):
    gameDisplay.blit(car_color, (carx, cary))


def car(a, b, img):
    gameDisplay.blit(img, (a, b))


def text_objects(text, font):
    textSurface = font.render(text, True, blue)
    return textSurface, textSurface.get_rect()


def blocks_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Dodged: {}'.format(count), True, white)
    gameDisplay.blit(text, (0, 0))


def text_display(text):
    font = pygame.font.SysFont('freesanbold.ttf', 25)
    text = font.render(text, True, white)
    gameDisplay.blit(text, (0, 20))


def quitgame():
    pygame.quit()
    quit()


def button(msg, msg_size, x_, y_, w, h, ic, ac, enlarg, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x_ + w > mouse[0] > x_ and y_ + h > mouse[1] > y_:
        pygame.draw.rect(gameDisplay, ac, (x_-enlarg/2, y_-enlarg/2, w + enlarg, h + enlarg))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x_, y_, w, h))

    smallText = pygame.font.SysFont('freesansbold.tff', msg_size)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x_ + w/2), (y_ + h/2))
    gameDisplay.blit(textSurf, textRect)


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()


def paused():
    pygame.mixer.music.pause()

    pause = True

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)

        largeText = pygame.font.SysFont('comicsansms', 115)
        TextSurf, TextRect = text_objects('Paused', largeText)
        TextRect.center = ((display_width / 2), 100)
        gameDisplay.blit(TextSurf, TextRect)

        pygame.draw.rect(gameDisplay, blue, (340, 200, 50, 150))
        pygame.draw.rect(gameDisplay, blue, (410, 200, 50, 150))

        button('Resume', 35, 150, 450, 100, 50, green, bright_green, 10, game_loop)
        button('Quit', 35, 550, 450, 100, 50, red, bright_red, 10, quitgame)
        pygame.display.update()
        clock.tick(15)


def introscreen():
    pix_ar = pygame.PixelArray(gameDisplay)
    for a in range(800):
        for b in range(600):
            pix_ar[a][b] = random.choice(colors)


def game_intro():
    i = 0
    fading = 0

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

        gameDisplay.blit(background, (0, 0))

        if i > 254:
            fading = 1
        elif i == 0:
            fading = 0
        if fading == 0:
            i = i + 1
        elif fading == 1:
            i = i - 1
        light_color = (i, i, i)
        pygame.draw.polygon(gameDisplay, light_color, ((164, 351), (165, 351), (184, 351), (184, 361), (165, 362)))
        pygame.draw.polygon(gameDisplay, light_color, ((346, 352), (347, 351), (370, 351), (371, 363), (346, 363)))
        pygame.draw.circle(gameDisplay, light_color, (115, 60), 7)
        pygame.draw.circle(gameDisplay, light_color, (218, 77), 7)
        pygame.draw.circle(gameDisplay, light_color, (309, 91), 7)
        pygame.draw.circle(gameDisplay, light_color, (390, 104), 7)
        pygame.draw.circle(gameDisplay, light_color, (464, 117), 7)
        pygame.draw.circle(gameDisplay, light_color, (531, 128), 7)

        largeText = pygame.font.SysFont('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Racing game", largeText)
        TextRect.center = ((display_width / 2), 150)
        gameDisplay.blit(TextSurf, TextRect)

        button('Start', 35, 150, 450, 100, 50, green, bright_green, 10, game_loop)
        button('Quit', 35, 550, 450, 100, 50, red, bright_red, 10, quitgame)

        pygame.display.update()
        clock.tick(60)


def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    car(x, y, crashImg)
    message_display('You Crashed')


def game_loop():
    pygame.mixer.music.load('soundtrack1.mp3')
    pygame.mixer.music.play(-1)

    global x
    x = (display_width * 0.45)
    global y
    y = (display_height * 0.7)

    coors = Coordinates()

    x_change = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -8
                if event.key == pygame.K_RIGHT:
                    x_change = 8
                if event.key == pygame.K_p:
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill((0, 50, 50))

        probability = random.randint(1, 50)
        if probability == 1:
            coors.create_enemy()

        coors_list = coors.enemy_move()

        for i in range(len(coors_list)):
            x_coord = coors_list[i][0]
            y_coord = coors_list[i][1]
            car_image = coors_list[i][2]
            draw_car(x_coord, y_coord, car_image)

        car(x, y, carImg)

        if x > (display_width - car_width) or x < 0:
            crash()

        for i in range(len(coors_list)):
            if ((y - coors_list[i][1]) > 0 and abs(y - coors_list[i][1]) < block_height) or \
                    ((y - coors_list[i][1]) < 0 and abs(y - coors_list[i][1]) < car_height):
                if (x - coors_list[i][0]) < 0 and abs(x - coors_list[i][0]) < car_width:
                    crash()
                if (x - coors_list[i][0]) >= 0 and abs(x - coors_list[i][0]) < block_width:
                    crash()

        """blocks_dodged(coors.get_dodged)"""
        text_display('Speed: {}'.format(round(coors.get_speed(), 1)))
        dodged = coors.get_dodged()
        blocks_dodged(dodged)

        pygame.display.update()
        clock.tick(80)


game_intro()
game_loop()
pygame.quit()
quit()
