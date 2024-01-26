import pygame
import os
import sys
import random

pygame.init()
size = width, height = 750, 300
score = 0
miss = 0
screen = pygame.display.set_mode(size)
alphabet = ["a.png", "b.png", "c.png", "d.png", "e.png", "f.png", "g.png", "h.png", "i.png", "j.png",
            "k.png", "l.png", "m.png", "n.png", "o.png", "p.png", "q.png", "r.png", "s.png", "t.png",
            "u.png", "v.png", "w.png", "x.png", "y.png", "z.png"]
letters = ["a.png", "b.png", "c.png", "d.png"]
check = {"a.png": 97,
         "b.png": 98,
         "c.png": 99,
         "d.png": 100,
         "e.png": 101,
         "f.png": 102,
         "g.png": 103,
         "h.png": 104,
         "i.png": 105,
         "j.png": 106,
         "k.png": 107,
         "l.png": 108,
         "m.png": 109,
         "n.png": 110,
         "o.png": 112,
         "p.png": 113,
         "q.png": 114,
         "r.png": 115,
         "s.png": 116,
         "t.png": 117,
         "u.png": 118,
         "v.png": 119,
         "w.png": 120,
         "x.png": 121,
         "y.png": 122,
         "z.png": 123,
         "mountain.png": ''}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.name = "mountain.png"
        self.score = 0
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


    def rscore(self):
        return self.score


    def new_sc(self):
        self.score = 0


class Landing(pygame.sprite.Sprite):
    #name = random.randint(0, len(letters))
    #image = load_image(letters[name])

    def __init__(self, pos):
        name = random.randint(0, len(letters) - 1)
        image = load_image(letters[name])
        super().__init__(all_sprites)
        self.score = 0
        self.name = letters[name]
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


    def update(self):
        if self.rect.y < 300:
            self.rect = self.rect.move(0, 1)
        else:
            self.score -= 1
            self.kill()


    def rscore(self):
        return self.score


    def new_sc(self):
        self.score = 0


def terminate():
    pygame.quit()
    sys.exit()


def draw(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text = font.render("Привет!", True, (100, 255, 100))
    text1 = font.render("Эта игра поможет тебе запомнить местонахождение букв на клавиатуре", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    screen.blit(text1, (20, 180))

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return True
        pygame.display.flip()
        clock.tick(100)


def print_score():
    global score
    global letters
    global i
    global t
    if score == -1:
        score = 0
        i = 0
        t = 0
        letters = ["a.png", "b.png", "c.png", "d.png"]
        for pt in all_sprites:
            if pt.name != "mountain.png":
                pt.kill()
        end()
    else:
        font = pygame.font.Font(None, 30)
        text = font.render(f'счет: {score}', True, (0, 0, 0))
        screen.blit(text, (10, 10))


def end():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text = font.render("К сожалению, ты проиграл", True, (100, 255, 100))
    text1 = font.render("Нажми пробел что бы попробовать снова", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))
    screen.blit(text1, (20, 180))
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                for pt in all_sprites:
                    pt.new_sc()
                draw(screen)
                return True
        pygame.display.flip()
        clock.tick(100)

if miss == 10:
    end(screen)

pygame.display.set_caption('Высадка десанта')
clock = pygame.time.Clock()
screen.fill((0, 0, 0))

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
mountain = Mountain()
i = 0
t = 0
falling = True
draw(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key_pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            #print(event.key)
            for pt in all_sprites:
                if event.key == check[pt.name]:
                    pt.kill()
                    score += 1

    if falling:
        pos = (random.randint(30, 700), 0)
        pt = Landing(pos)
        all_sprites.add(pt)
        falling = False
    t += 1
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    #all_sprites.update()
    for pt in all_sprites:
        pt.update()
        score += pt.rscore()
    print_score()
    i -= 0.05
    if t % 80 == 0:
        falling = True
    if t % 240 == 0 and len(letters) != len(alphabet):
        letters.append(alphabet[len(letters)])
        #print(letters)
    clock.tick(50 - i)
    pygame.display.flip()
pygame.quit()
