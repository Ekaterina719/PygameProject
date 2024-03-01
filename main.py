import pygame
import os
import sys
import random
from pygame import mixer


pygame.init()
size = width, height = 1536, 800
score = 0
start_time = pygame.time.get_ticks()
time_hms = 0, 0, 0
mixer.init()
fullname1 = os.path.join('data', 'fon_music.wav')
fullname2 = os.path.join('data', 'pop_sound.wav')
fullname3 = os.path.join('data', 'ydar_sound.wav')
fullname4 = os.path.join('data', 'end_sound.wav')
fon_sound = mixer.Sound(fullname1)
pop_sound = mixer.Sound(fullname2)
ydar_sound = mixer.Sound(fullname3)
end_sound = mixer.Sound(fullname4)
fon_sound.set_volume(0.8)
pop_sound.set_volume(0.2)
ydar_sound.set_volume(0.7)
end_sound.set_volume(0.5)
new_letter_t = 240
new_fall_t = 80
uvel_skoroct = 0.05
nach_tick = 5
screen = pygame.display.set_mode(size)
on_board = []
bobom = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png']
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
         "o.png": 111,
         "p.png": 112,
         "q.png": 113,
         "r.png": 114,
         "s.png": 115,
         "t.png": 116,
         "u.png": 117,
         "v.png": 118,
         "w.png": 119,
         "x.png": 120,
         "y.png": 121,
         "z.png": 122,
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
    image = pygame.transform.scale(image, (1536, 800))

    def __init__(self):
        super().__init__(all_sprites)
        self.name = "mountain.png"
        self.score = 0
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = height
        self.boom = 0

    def rscore(self):
        return self.score

    def new_sc(self):
        self.score = 0


class Landing(pygame.sprite.Sprite):

    def __init__(self, pos):
        global on_board
        sp = [item for item in letters if item not in on_board]
        if not sp:
            sp = letters
        name = random.randint(0, len(sp) - 1)
        on_board.append(sp[name])
        image = load_image(sp[name])
        super().__init__(all_sprites)
        self.score = 0
        self.name = sp[name]
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.boom = 0

    def update(self):
        global on_board
        if self.rect.y < 700:
            self.rect = self.rect.move(0, 1)
        else:
            self.score -= 1
            ydar_sound.play()
            on_board.remove(self.name)
            self.boom = 1

    def rscore(self):
        return self.score

    def new_sc(self):
        self.score = 0

    def booom(self):
        global bobom
        if self.boom <= 9:
            new_im = load_image(bobom[self.boom - 1])
            self.image = new_im
            self.boom += 1
        else:
            self.boom = 0
            self.kill()


def terminate():
    pygame.quit()
    sys.exit()


def rules():
    global screen
    image = load_image("nach_fon.png")
    image = pygame.transform.scale(image, (1536, 800))
    screen.blit(image, (0, 0))
    font = pygame.font.Font(None, 60)
    text = font.render("Правила игры", True, (0, 0, 0))
    text_x = width // 2 - text.get_width() // 2
    screen.blit(text, (text_x, 100))

    font = pygame.font.Font(None, 40)
    text1 = font.render(
        'Буквы медленно падают вниз. Задача — нажать нужную букву на клавиатуре, пока она не “разбилась”.',
        True, (0, 0, 0))
    text_xx = width // 2 - text1.get_width() // 2
    screen.blit(text1, (text_xx, 170))

    text2 = font.render(
        'Очки прибавляются за правильные ответы и отнимаются за неправильные нажатия клавиш и пропуски букв.',
        True, (0, 0, 0))
    text_xx = width // 2 - text2.get_width() // 2
    screen.blit(text2, (text_xx, 220))

    text3 = font.render(
        'Постепенно скорость падения букв и их количество на экране увеличивается.',
        True, (0, 0, 0))
    text_xx = width // 2 - text3.get_width() // 2
    screen.blit(text3, (text_xx, 270))

    text4 = font.render(
        'Игра заканчивается, когда счетчик становится отрицательным.',
        True, (0, 0, 0))
    text_xx = width // 2 - text4.get_width() // 2
    screen.blit(text4, (text_xx, 320))

    font = pygame.font.Font(None, 50)
    back = font.render("Вернуться", True, (255, 255, 255))
    back_w = back.get_width()
    back_h = back.get_height()
    screen.blit(back, (50, 690))
    pygame.draw.rect(screen, (255, 255, 255), (45, 685,
                                               back_w + 10, back_h + 10), 1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 45 <= event.pos[0] <= back_w + 55 and 685 <= event.pos[1] <= back_h + 695:
                    draw()
                    return True
        pygame.display.flip()
        clock.tick(100)


def draw():
    global screen
    global start_time
    global alphabet
    global letters
    global new_letter_t
    global new_fall_t
    global uvel_skoroct
    global nach_tick

    image = load_image("nach_fon.png")
    image = pygame.transform.scale(image, (1536, 800))
    screen.blit(image, (0, 0))

    font = pygame.font.Font(None, 80)
    nname = font.render('Игра "FALLETS"', True, (0, 0, 0))
    text_x = width // 2 - nname.get_width() // 2
    screen.blit(nname, (text_x, 100))

    font = pygame.font.Font(None, 40)
    text = font.render("Привет!", True, (0, 0, 0))
    text1 = font.render("Эта игра поможет тебе запомнить местонахождение букв на клавиатуре", True, (0, 0, 0))
    text_x = width // 2 - text.get_width() // 2
    text_xx = width // 2 - text1.get_width() // 2
    screen.blit(text, (text_x, 200))
    screen.blit(text1, (text_xx, 250))

    font = pygame.font.Font(None, 60)
    menu = font.render("Выбор уровня", True, (255, 255, 255))
    screen.blit(menu, (40, 430))

    font = pygame.font.Font(None, 40)
    choise_1 = font.render("Легкий", True, (255, 255, 255))
    choise_1_w = choise_1.get_width()
    choise_1_h = choise_1.get_height()
    screen.blit(choise_1, (50, 510))
    pygame.draw.rect(screen, (255, 255, 255), (45, 505,
                                               choise_1_w + 10, choise_1_h + 10), 1)
    choise_2 = font.render("Обычный", True, (255, 255, 255))
    choise_2_w = choise_2.get_width()
    choise_2_h = choise_2.get_height()
    screen.blit(choise_2, (50, 570))
    pygame.draw.rect(screen, (255, 255, 255), (45, 565,
                                               choise_2_w + 10, choise_2_h + 10), 1)
    choise_3 = font.render("Сложный", True, (255, 255, 255))
    choise_3_w = choise_3.get_width()
    choise_3_h = choise_3.get_height()
    screen.blit(choise_3, (50, 630))
    pygame.draw.rect(screen, (255, 255, 255), (45, 625,
                                               choise_3_w + 10, choise_3_h + 10), 1)
    font = pygame.font.Font(None, 50)
    rrule = font.render("Правила игры", True, (255, 255, 255))
    rrule_w = rrule.get_width()
    rrule_h = rrule.get_height()
    screen.blit(rrule, (50, 690))
    pygame.draw.rect(screen, (255, 255, 255), (45, 685,
                                               rrule_w + 10, rrule_h + 10), 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if 45 <= event.pos[0] <= choise_1_w + 55 and 505 <= event.pos[1] <= choise_1_h + 515:
                    fon_sound.play(-1)
                    start_time = pygame.time.get_ticks()
                    alphabet = ["d.png", "k.png", "f.png", "j.png", "l.png", "s.png", "g.png", "h.png", "i.png",
                                "r.png", "o.png", "e.png"]
                    letters = ["d.png", "k.png", "f.png", "j.png"]
                    new_letter_t = 280
                    new_fall_t = 100
                    uvel_skoroct = 0.04
                    nach_tick = 50
                    return True
                elif 45 <= event.pos[0] <= choise_2_w + 55 and 565 <= event.pos[1] <= choise_2_h + 575:
                    fon_sound.play(-1)
                    start_time = pygame.time.get_ticks()
                    alphabet = ["a.png", "b.png", "c.png", "d.png", "e.png", "f.png", "g.png", "h.png", "i.png",
                                "j.png", "k.png", "m.png", "n.png", "o.png", "r.png", "s.png", "t.png"]
                    letters = ["a.png", "b.png", "c.png", "d.png"]
                    new_letter_t = 260
                    new_fall_t = 90
                    uvel_skoroct = 0.05
                    nach_tick = 60
                    return True
                elif 45 <= event.pos[0] <= choise_3_w + 55 and 625 <= event.pos[1] <= choise_3_h + 635:
                    fon_sound.play(-1)
                    start_time = pygame.time.get_ticks()
                    alphabet = ["a.png", "b.png", "c.png", "d.png", "e.png", "f.png", "g.png", "h.png", "i.png",
                                "j.png", "k.png", "l.png", "m.png", "n.png", "o.png", "p.png", "q.png", "r.png",
                                "s.png", "t.png", "u.png", "v.png", "w.png", "x.png", "y.png", "z.png"]
                    letters = ["a.png", "b.png", "c.png", "d.png", "e.png", "f.png", "g.png", "h.png"]
                    new_letter_t = 240
                    new_fall_t = 80
                    uvel_skoroct = 0.06
                    nach_tick = 70
                    return True
                elif 45 <= event.pos[0] <= rrule_w + 55 and 685 <= event.pos[1] <= rrule_h + 695:
                    rules()
                    return True
        pygame.display.flip()
        clock.tick(100)


def print_score():
    global score
    global time_hms
    global letters
    global i
    global t
    global on_board
    if score == -1:
        end_sound.play()
        fon_sound.stop()
        score = 0
        i = 0
        t = 0
        on_board = []
        letters = ["a.png", "b.png", "c.png", "d.png"]
        for pt in all_sprites:
            if pt.name != "mountain.png":
                pt.kill()
        end()
    else:
        font = pygame.font.Font(None, 50)
        text_sc = font.render(f'счет: {score}', True, (0, 0, 0))
        screen.blit(text_sc, (10, 10))

        time_ms = pygame.time.get_ticks() - start_time
        new_hms = (time_ms // (1000 * 60 * 60)) % 24, (time_ms // (1000 * 60)) % 60, (time_ms // 1000) % 60
        time_hms = new_hms
        text_tic = font.render(f'время: {time_hms[1]:02d}:{time_hms[2]:02d}', True, (0, 0, 0))
        screen.blit(text_tic, (200, 10))


def end():
    global time_hms

    image = load_image("end_fon.png")
    image = pygame.transform.scale(image, (1536, 800))
    screen.blit(image, (0, 0))
    font = pygame.font.Font(None, 40)
    text = font.render("К сожалению, ты проиграл", True, (0, 0, 0))
    res_text = font.render(f"Ты продержался {time_hms[1]} минут и {time_hms[2]} секунд.", True, (0, 0, 0))
    text1 = font.render("Нажми пробел что бы попробовать снова", True, (0, 0, 0))
    screen.blit(text, (100, 600))
    screen.blit(res_text, (100, 650))
    screen.blit(text1, (100, 700))
    time_hms = 0, 0, 0
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminate()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                for pt in all_sprites:
                    pt.new_sc()
                draw()
                return True
        pygame.display.flip()
        clock.tick(100)


pygame.display.set_caption('Игра')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
mountain = Mountain()
i = 0
t = 0
right_pressed = False
falling = True
draw()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key_pressed = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            for pt in all_sprites:
                if event.key == check[pt.name]:
                    pop_sound.play()
                    if pt.name in on_board:
                        on_board.remove(pt.name)
                    pt.boom = 1
                    score += 1
                    right_pressed = True
            if not right_pressed:
                score -= 1
            right_pressed = False

    if falling:
        pos = (random.randint(30, 1450), 0)
        pt = Landing(pos)
        all_sprites.add(pt)
        falling = False
    t += 1
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    for pt in all_sprites:
        if pt.boom > 0:
            pt.booom()
        else:
            pt.update()
            score += pt.rscore()
    print_score()
    i += uvel_skoroct
    if t % new_fall_t == 0:
        falling = True
    if t % new_letter_t == 0 and len(letters) != len(alphabet):
        letters.append(alphabet[len(letters)])
    clock.tick(nach_tick + i)
    pygame.display.flip()
pygame.quit()
