import pygame
import sys


pygame.init()


FPS = 50
r = pygame.image.load("lefte.png")
l = pygame.image.load("righte.png")

class hero():
    def __init__(self, x, y, buff=[]):
        self.x = x
        self.y = y

        self.up_x = x + 50
        self.up_y = y + 100

        self.b = buff
        self.jumping = 0
        self.delta_jump = 0

        self.run = 0
        self.blink_ = 0
        self.energy_ = 100

        self.health_ = 100
        self.velx = 0
        self.vely = 0

        self.attackl = 0
        self.attackr = 0
    
    def delete_all(self, screen, BackGround):
        screen.fill((0, 0, 0))
        screen.blit(BackGround.image, BackGround.rect)
    
    def blink(self, x):
        self.x += x
        self.jumping = 0
    
    def jump(self):
        if self.jumping == 0:
            stop_all()

            sound1.play()
            self.jumping = 1

            self.vely += 70
    
    def go(self, nap):
        self.velx += 6 * nap

    
    def tick(self, screen, BackGround, enemies):
        if self.velx >= 0:
            self.velx -= min(5, self.velx)
        
        if self.velx <= 0:
            self.velx += min(5, -self.velx)
        
        if self.vely >= 0:
            self.vely -= min(10, self.vely)
        
        if self.vely <= 0:
            self.vely += min(10, -self.vely)
        
        if self.vely == 0 and self.y != 0:
            self.y -= 10
            self.up_y -= 10
        
        elif self.vely == 0:
            self.jumping = 0
        self.velx = min(self.velx, 10)
        self.velx = max(self.velx, -10)
        self.x += self.velx
        self.y += self.vely
        self.up_x += self.velx
        self.up_y += self.vely
        self.delete_all(screen, BackGround)
        self.draw(screen, enemies)
        if self.x <= 0:
            self.x = 0
            self.velx = 0
        if self.up_x >= 1200:
            self.x = 1150
            self.up_x = 1200
            self.velx = 0
        self.up_x = self.x + 50
        self.up_y = self.y + 100    
    
    def draw(self, screen, enemies):
        draw(self, left_go, right_go)
        for i in enemies:
            draw(i, lefte_go, righte_go)
        if self.attackl:
            print(1)
        
        if self.attackr:
            draw2(attack_left, char.x - 150, char.y + 75)
        
        if self.attackl:
            draw2(attack_rifgt, char.up_x, char.y + 75)

        screen.blit(pygame.image.load("health" + str(self.health_ // 10 * 10) + '.png'), (10, 10))
    
    def generate(self):
        y = 570 - self.y
        up_y = 570 - self.up_y

        pnt1 = (self.x, y)
        pnt2 = (self.x, up_y)
        pnt3 = (self.up_x, up_y)
        pnt4 = (self.up_x, y)

        pygame.draw.polygon(screen, (255, 255, 255), [pnt1, pnt2, pnt3, pnt4], 2)
        return [pnt1, pnt2, pnt3, pnt4]
    
    def attack(self, enemies):
        #global enemies
        if self.velx == 0:
            return 
        died = []
        if self.velx > 0:
            self.attackl = 1
        if self.velx < 0:
            self.attackr = 1
        for i in range(len(enemies)):
            if self.velx > 0:
                if ((enemies[i].x <= self.up_x + 150 and enemies[i].up_x >= self.x) or 
                   (enemies[i].x <= self.up_x + 150 and enemies[i].up_x >= self.up_x + 150)):
                    died.append(i)
                

            if self.velx < 0:
                if ((enemies[i].x >= self.x - 150 and enemies[i].x <= self.x) or 
                (enemies[i].x >= self.x - 150 and enemies[i].x <= self.x - 150)):
                    died.append(i)
                self.attackr = 1
        for i in died[::-1]:
            del(enemies[i])
        


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class AnimatedSprite():
    def __init__(self, sheet, columns, rows, x, y):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)

        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

        self.rect = self.rect.move(x, y)
        self.sprite = pygame.sprite.Sprite()

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.sprite)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

        self.sprite.image = self.image

        self.sprite.image.set_colorkey((255, 255, 255))

        self.sprite.rect = self.sprite.image.get_rect()
    
    def draw(self, screen, x, y):
        try:
            self.sprite.rect.x = x
            self.sprite.rect.y = 570 - y
            self.sprites.draw(screen)
        except:
            self.update()
            self.sprite.rect.x = x
            self.sprite.rect.y = 570 - y
            self.sprites.draw(screen)


righte_go = AnimatedSprite(r, 4, 1, 100, 50)
lefte_go = AnimatedSprite(l, 4, 1, 100, 50)


class Enemy():
    def __init__(self, x, y, rnd):
        self.x = rnd * 1200
        self.y = 0
        self.up_x = self.x + x
        self.up_y = self.y + y
        self.velx = 0
    
    def move(self):
        global char
        if char.x < self.x:
            self.x -= 5
            self.velx = -5
        else:
            self.velx = 5
            self.x += 5
    
    def attack(self):
        if char.y <= self.up_y + 5 and (char.x <= self.x and char.up_x >= self.x) or ((char.x <= self.up_x and char.up_x >= self.up_x)):
            return True
        return False
        

def stop_all():
    sound1.stop()


def draw(char, left_go, right_go):
    global screen, stop

    if char.velx > 0:
        left_go.draw(screen, char.x, char.up_y)

    elif char.velx < 0:
        right_go.draw(screen, char.x, char.up_y)

    else:
        stop.draw(screen, char.x, char.up_y)


def draw2(name, x, y):
    global screen
    name.draw(screen, x, y)


def start():
    global FC, screen
    BackGround = Background('open.png', [0,0])

    screen.blit(BackGround.image, BackGround.rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    k = event.pos
                    if k[0] > 360 and k[1] > 180 and k[0] < 834 and k[1] < 254:
                        return
                    
                    if k[0] > 360 and k[1] > 373 and k[0] < 834 and k[1] < 439:
                        prepare1()
                        return
            if event.type == pygame.KEYDOWN:

                if event.key == 292:
                    if FC:
                        screen = pygame.display.set_mode((1200, 675))
                        screen.blit(BackGround.image, BackGround.rect)

                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        screen.blit(BackGround.image, BackGround.rect)
                    FC = 1 - FC
        pygame.display.flip()


def prepare1():
    global FC, screen
    BackGround = Background('firstpage.png', [0,0])
    screen.blit(BackGround.image, BackGround.rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    k = event.pos
                    if k[0] > 35 and k[1] > 560 and k[0] < 243 and k[1] < 646:
                        start()
                        return

                    if k[0] > 851 and k[1] > 551 and k[0] < 1048 and k[1] < 646:
                        prepare2()
                        return

            if event.type == pygame.KEYDOWN:
                if event.key == 292:
                    if FC:
                        screen = pygame.display.set_mode((1200, 675))
                        screen.blit(BackGround.image, BackGround.rect)

                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        screen.blit(BackGround.image, BackGround.rect)
                    FC = 1 - FC
        pygame.display.flip()
    return


def prepare2():
    global FC, screen
    BackGround = Background('secondpage.png', [0,0])

    screen.blit(BackGround.image, BackGround.rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    k = event.pos

                    if k[0] > 35 and k[1] > 560 and k[0] < 243 and k[1] < 646:
                        start()
                        return
            if event.type == pygame.KEYDOWN:
                if event.key == 292:
                    if FC:
                        screen = pygame.display.set_mode((1200, 675))
                        screen.blit(BackGround.image, BackGround.rect)
                
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        screen.blit(BackGround.image, BackGround.rect)
                    
                    FC = 1 - FC
                
        pygame.display.flip()

    return


screen = pygame.display.set_mode((1200, 675))
screen.fill((0, 0, 0))

pygame.display.flip()
running = True

FC = False
clock = pygame.time.Clock()

char = hero(0, 0)
pygame.mixer.music.load('track.mp3')

pygame.mixer.music.play()
sound1 = pygame.mixer.Sound('jump.wav')

r = pygame.image.load("left.png")
r.set_colorkey((255, 255, 255))

l = pygame.image.load("right.png")
l.set_colorkey((255, 255, 255))

right_go = AnimatedSprite(r, 4, 1, 100, 50)
left_go = AnimatedSprite(l, 4, 1, 100, 50)

stop = AnimatedSprite(pygame.image.load("stop.png"), 1, 1, 100, 50)
attack_left = AnimatedSprite(pygame.image.load("attackl.png"), 4, 1, 125, 50)
attack_rifgt = AnimatedSprite(pygame.image.load("attackr.png"), 4, 1, 125, 50)
enemies = []


def death():
    global FC, screen
    BackGround = Background('death.png', [0,0])
    screen.blit(BackGround.image, BackGround.rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    k = event.pos
                    if k[0] > 310 and k[1] > 439 and k[0] < 809 and k[1] < 521:
                        kek()
                        return
        pygame.display.flip()
    return


def paused():
    global FC, screen
    BackGround = Background('pause.png', [0,0])
    screen.blit(BackGround.image, BackGround.rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == 292:
                    if FC:
                        screen = pygame.display.set_mode((1200, 675))
                        BackGround = Background('pause.png', [0,0])
                        screen.blit(BackGround.image, BackGround.rect)
                        pygame.display.flip()
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        BackGround = Background('pause.png', [0,0])
                        screen.blit(BackGround.image, BackGround.rect)
                        pygame.display.flip()
                    FC = 1 - FC


def main_():
    global FC
    char.health_ = 100
    char.x = 0
    char.y = 0
    char.velx = 0
    char.vely = 0

    char.up_x = 50
    char.up_y = 100
    left = False
    right = False
    global screen

    BackGround = Background('bg.png', [0,0])
    screen.blit(BackGround.image, BackGround.rect)
    tics = 0
    enemies = []

    enemies.append(Enemy(50, 100, 1))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    char.jump()

                elif event.key == pygame.K_LEFT:
                    left = True
                    right = False

                elif event.key == pygame.K_RIGHT:
                    right = True
                    left = False
                elif event.key == 292:
                    if FC:
                        screen = pygame.display.set_mode((1200, 675))
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    FC = 1 - FC
                elif event.key == pygame.K_ESCAPE:
                    paused()
                elif event.key == 97:
                        char.attack(enemies)
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                elif event.key == pygame.K_RIGHT:
                    right = False
        if right:
            char.go(1)
        if left:
            char.go(-1)
        if tics % 10 == 0:
            if char.velx > 0:
                left_go.update()
            elif char.velx < 0:
                right_go.update()
            for i in enemies:
                if i.attack():
                    char.health_ -= 10
                if i.velx > 0:
                    lefte_go.update()
                else:
                    righte_go.update()
            
            if char.attackl:
                attack_left.update()
                char.attackl += 1
                char.attackl %= 2
            if char.attackr:
                attack_rifgt.update()
                char.attackr += 1
                char.attackr %= 2
        
        if tics % 30 == 0:
            if char.x > 500:
                enemies.append(Enemy(50, 100, 0))
            else:
                enemies.append(Enemy(50, 100, 1))

        if tics % 60 == 0:
            char.health_ += 1
            char.health_ = min(100, char.health_)

        tics += 1
        for i in enemies:
            i.move()

        if(char.health_ <= 0):
            return

        clock.tick(FPS)
        char.tick(screen, BackGround, enemies)
        pygame.display.flip()


def kek():
    while True:
        start()
        main_()
        death()


kek()
pygame.quit()