import os
import sys
import pygame

pygame.init()

pygame.key.set_repeat(200, 70)

FPS = 50
WIDTH = 400
HEIGHT = 300
STEP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


# def load_level(filename):
#     filename = "data/" + filename
#     # читаем уровень, убирая символы перевода строки
#     with open(filename, 'r') as mapFile:
#         level_map = [line.strip() for line in mapFile]
#
#     # и подсчитываем максимальную длину
#     maxWidth = max(map(len, level_map))
#
#     # дополняем каждую строку пустыми клетками ('.')
#     return list(map(lambda x: x.ljust(maxWidth, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            pass
        #TO DO
    #return player, x, y

def terminate():
    pygame.quit()
    sys.exit()


def startScreen():
    # introText = ["ЗАСТАВКА", "",
    #              "Правила игры",
    #              "Если в правилах несколько строк,",
    #              "приходится выводить их построчно"]
    #
    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    # font = pygame.font.Font(None, 30)
    # textCoord = 50
    # for line in introText:
    #     stringRendered = font.render(line, 1, pygame.Color('black'))
    #     introRect = stringRendered.get_rect()
    #     textCoord += 10
    #     introRect.top = textCoord
    #     introRect.x = 10
    #     textCoord += introRect.height
    #     screen.blit(stringRendered, introRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


player_sheets = {"idle": (load_image("idle_left.png", -1), 1, 1),
    "left": (load_image("rabbit_walking_left.png", -1), 7, 1),
    "right": (load_image("rabbit_walking_right.png", -1), 7, 1)
}
wall_sheets = {
    "0000":(load_image("grass_0000.png", -1), 3, 1),
	"1011":(load_image("grass_1011.png", -1), 3, 1)
}

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group = None):
        self.period = 2
        super().__init__(group, all_sprites)
        self.frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.frames = []
        #self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % (len(self.frames)*self.period)
        self.image = self.frames[self.cur_frame//self.period]


class Player(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y, group=player_group)
        self.stage = "idle"

    def change_stage(self, stage):
        self.stage = stage
        self.cut_sheet(*player_sheets[stage])
        self.cur_frame = 0


class Wall(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y, group=walls_group)
        self.period = 8

player = Player(*player_sheets["idle"], 50, 50)
Wall(*wall_sheets["1011"], 0, 0)
Wall(*wall_sheets["1011"], 30, 0)
Wall(*wall_sheets["1011"], 60, 0)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_LEFT:
             #    player.rect.x -= STEP
                if player.stage != "left":
                    player.change_stage("left")
             if event.key == pygame.K_RIGHT:
             #    player.rect.x += STEP
                if player.stage != "right":
                    player.change_stage("right")
             if event.key == pygame.K_UP:
                 if player.stage != "idle":
                    player.change_stage("idle")
             #    player.rect.y -= STEP
             #if event.key == pygame.K_DOWN:
             #    player.rect.y += STEP
        else:
            if player.stage != "idle":
                player.change_stage("idle")


    #camera.update(player)

    #for sprite in all_sprites:
    #    camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    #tiles_group.draw(screen)
    player_group.draw(screen)
    walls_group.draw(screen)
    for i in walls_group:
        i.update()
    player.update()
    pygame.display.flip()

    clock.tick(FPS)

terminate()