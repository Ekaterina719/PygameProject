import pygame
import os
import sys
import random

pygame.init()
size = width, height = 750, 300
screen = pygame.display.set_mode(size)
alphabet = ["a.png", "b.png", "c.png", "d.png", "e.png", "f.png", "g.png", "h.png", "i.png", "j.png",
            "k.png", "l.png", "m.png", "n.png", "o.png", "p.png", "q.png", "r.png", "s.png", "t.png",
            "u.png", "v.png", "w.png", "x.png", "y.png", "z.png"]
letters = ["a.png", "b.png", "c.png", "d.png",]
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
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height


class Landing(pygame.sprite.Sprite):
    #name = random.randint(0, len(letters))
    #image = load_image(letters[name])

    def __init__(self, pos):
        name = random.randint(0, len(letters) - 1)
        image = load_image(letters[name])
        super().__init__(all_sprites)
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
            self.kill()


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
    #text_w = text.get_width()
    #text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    screen.blit(text1, (20, 180))
    #pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           #text_w + 20, text_h + 20), 1)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                return True  # начинаем игру
        pygame.display.flip()
        clock.tick(100)


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
        #if key_pressed[pygame.K_a]:
         #   for pt in all_sprites:
          #      if pt.name == "a.png.png":
           #         pt.kill()

    if falling:
        pos = (random.randint(30, 700), 0)
        pt = Landing(pos)
        all_sprites.add(pt)
        falling = False
    t += 1
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(50 - i)
    i -= 0.05
    if t % 80 == 0:
        falling = True
    if t % 240 == 0 and len(letters) != len(alphabet):
        letters.append(alphabet[len(letters)])
        print(letters)
pygame.quit()
