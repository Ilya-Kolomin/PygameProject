import os
import sys
import pygame
import random

pygame.init()

pygame.key.set_repeat(200, 70)

FPS = 60
WIDTH = 390
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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    maxWidth = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(maxWidth, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                s = ""
                if level[y][max(x-1, 0)] == "#":
                    s+="1"
                else:
                    s+="0"
                if level[min(y+1, len(level) - 1)][x] == "#":
                    s+="1"
                else:
                    s+="0"
                if level[y][min(x+1, len(level[y]) - 1)] == "#":
                    s+="1"
                else:
                    s+="0"
                if level[max(y-1, 0)][x] == "#":
                    s+="1"
                else:
                    s+="0"
                Wall(*wall_sheets[s], x*30, y*30)
            AnimatedSprite(*floor_sheet, x*30, y*30)
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

class Label:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color("white")
        self.font_color = pygame.Color("gray")
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.Font("freesansbold.ttf", self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None


    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)

class Button(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color("blue")
        # при создании кнопка не нажата
        self.pressed = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom), 2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False

def pause():
    gui = GUI()
    b1 = Button((10, 65, 200, 80), "EXIT")
    b2 = Button((10, 10, 260, 50), "CONTINUE")
    gui.add_element(b1)
    gui.add_element(b2)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            gui.get_event(event);
        if b1.pressed:
            while b1.pressed:
                for event in pygame.event.get():
                    gui.get_event(event)
                gui.render(screen)
                gui.update()
                pygame.display.flip()
            terminate()
        if b2.pressed:
            while b2.pressed:
                for event in pygame.event.get():
                    gui.get_event(event)
                gui.render(screen)
                gui.update()
                pygame.display.flip()
            return
        gui.render(screen)
        gui.update()
        pygame.display.flip()

floor_sheet = (load_image("grass_floor.png"), 8, 1)

player_sheets = {"idle_left": (load_image("idle_left.png", -1), 1, 1),
    "idle_right": (load_image("idle_right.png", -1), 1, 1),
    "idle_front": (load_image("rabbit_front.png", -1), 1, 1),
    "left": (load_image("rabbit_walking_left.png", -1), 8, 1),
    "right": (load_image("rabbit_walking_right.png", -1), 8, 1),
    "down": (load_image("rabbit_down.png", -1), 1, 7),
    "up": (load_image("rabbit_up.png", -1), 1, 7)
}
wall_sheets = {
    "0000":(load_image("grass_0000.png", -1), 3, 1),
    "0001":(load_image("grass_0001.png", -1), 3, 1),
    "0010": (load_image("grass_0010.png", -1), 3, 1),
    "0011": (load_image("grass_0011.png", -1), 3, 1),
    "0100": (load_image("grass_0100.png", -1), 3, 1),
    "0101": (load_image("grass_0101.png", -1), 3, 1),
    "0110": (load_image("grass_0110.png", -1), 3, 1),
    "0111": (load_image("grass_0111.png", -1), 3, 1),
    "1000": (load_image("grass_1000.png", -1), 3, 1),
    "1001": (load_image("grass_1001.png", -1), 3, 1),
    "1010": (load_image("grass_1010.png", -1), 3, 1),
    "1011": (load_image("grass_1011.png", -1), 3, 1),
    "1100": (load_image("grass_1100.png", -1), 3, 1),
    "1101": (load_image("grass_1101.png", -1), 3, 1),
    "1110": (load_image("grass_1110.png", -1), 3, 1),
    "1111": (load_image("grass_1111.png", -1), 3, 1)
}

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group = None):
        self.period = 3

        if group != None:
            super().__init__(group, all_sprites)
        else:
            super().__init__(all_sprites)
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
        self.stage = "idle_right"

    def change_stage(self, stage):
        self.stage = stage
        self.cut_sheet(*player_sheets[stage])
        self.cur_frame = 0
    def move_left(self):
        if self.stage!="left":
            self.change_stage("left")
        if self.cur_frame//self.period == 4:
            self.rect.x -= 2
        elif 4 < self.cur_frame//self.period < 7:
            self.rect.x -= 4
        if pygame.sprite.spritecollideany(self, walls_group):
            self.rect.x += 4
    def move_right(self):
        if self.stage!="right":
            self.change_stage("right")
        if self.cur_frame//self.period == 4:
            self.rect.x += 2
        elif 4 < self.cur_frame//self.period < 7:
            self.rect.x += 4
        if pygame.sprite.spritecollideany(self, walls_group):
            self.rect.x -= 4
    def move_idle(self):
        if self.stage=="right":
            self.change_stage("idle_right")
        elif self.stage=="left":
            self.change_stage("idle_left")
        elif self.stage=="down":
            self.change_stage("idle_front")
        elif self.stage=="up":
            self.change_stage("idle_left")
    def move_down(self):
        if self.stage!="down":
            self.change_stage("down")
        if self.cur_frame//self.period == 5:
            self.rect.y += 2
        elif 2 < self.cur_frame//self.period < 5:
            self.rect.y += 3
        if pygame.sprite.spritecollideany(self, walls_group):
            self.rect.y -= 3
    def move_up(self):
        if self.stage!="up":
            self.change_stage("up")
        if self.cur_frame//self.period == 3:
            self.rect.y -= 2
        elif 3 < self.cur_frame//self.period < 6:
            self.rect.y -= 3
        if pygame.sprite.spritecollideany(self, walls_group):
            self.rect.y += 3

class Wall(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(sheet, columns, rows, x, y, group=walls_group)
        self.period = random.randrange(14, 20)

player = Player(*player_sheets["idle_right"], 30, 30)
generate_level(load_level("levelex.txt"))
# Wall(*wall_sheets["1111"], 0, 0)
# Wall(*wall_sheets["1011"], 30, 0)
# Wall(*wall_sheets["1111"], 60, 0)
# Wall(*wall_sheets["1101"], 0, 30)
# Wall(*wall_sheets["1111"], 0, 60)
# Wall(*wall_sheets["1110"], 30, 60)
# Wall(*wall_sheets["1111"], 60, 60)
# Wall(*wall_sheets["0111"], 60, 30)
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_LEFT:
                 player.move_left()
                #player.rect.x -= 2
                #if player.stage != "left":
                #    player.change_stage("left")
             if event.key == pygame.K_RIGHT:
                 player.move_right()
                #player.rect.x += 2
                #if player.stage != "right":
                #    player.change_stage("right")
             if event.key == pygame.K_UP:
                 player.move_up()
             #    player.move_left()
                 #if player.stage != "idle":
                 #   player.change_stage("idle")
             #    player.rect.y -= STEP
             if event.key == pygame.K_DOWN:
                 player.move_down()
             if event.key == pygame.K_ESCAPE:
                 pause()
        else:
            #if player.stage != "idle":
            #    player.change_stage("idle")
            player.move_idle()


    #camera.update(player)

    #for sprite in all_sprites:
    #    camera.apply(sprite)

    screen.fill(pygame.Color(0, 0, 0))
    all_sprites.draw(screen)
    player_group.draw(screen)
    walls_group.draw(screen)
    for i in all_sprites:
        i.update()
    #player.update()
    pygame.display.flip()

    clock.tick(FPS)

terminate()