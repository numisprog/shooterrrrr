from pygame import *
from random import *
win = display.set_mode((700, 500))
display.set_caption("Шутер")
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
fps = 60
score = 0
mixer.init()
font.init()
font1 = font.SysFont('Arial', 60)
font2 = font.SysFont('Arial', 25)
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound("fire.ogg")
class GameSprite(sprite.Sprite):
    def __init__(self, player_speed, player_x, player_y, player_image, w, h):
        sprite.Sprite.__init__(self)
        self.speed = player_speed
        self.w = w
        self.h = h
        self.image = transform.scale(image.load(player_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - self.w:
            self.rect.x += self.speed
    def fire(self):
        bullet1 = Bullet(10, self.rect.centerx, self.rect.y, "bullet.png", 10, 20)
        bullets.add(bullet1)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
player1 = Player(5, 10, 410, "rocket.png", 50, 90)
bullets = sprite.Group()
enemys = sprite.Group()
for i in range(5):
    enemy1 = Enemy(4, randint(0, 650), 0, "ufo.png", 70, 50)
    enemys.add(enemy1)
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire.play()
                player1.fire()
    if not(finish):
        sprites_list = sprite.groupcollide(enemys, bullets, True, True)
        for sprite1 in sprites_list:
            score += 1
            enemy1 = Enemy(4, randint(0, 650), 0, "ufo.png", 70, 50)
            enemys.add(enemy1)
        clock.tick(fps)
        display.update()
        win.blit(bg, (0, 0))
        player1.reset()
        player1.update()
        enemys.update()
        enemys.draw(win)
        bullets.draw(win)
        bullets.update()
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        text_score = font2.render("Счет:" + str(score), 1, (255, 255, 255))
        win.blit(text_lose, (0, 0))
        win.blit(text_score, (0, 20))
        if score >= 10:
            goodfinish = font1.render("Win!!!", 1, (255, 0 ,0))
            win.blit(goodfinish, (300, 220))
            finish = True
        if lost >= 3:
            badfinish = font1.render("Lose...", 1, (255, 0, 0))
            win.blit(badfinish, (300, 220))
            finish = True
    display.update()