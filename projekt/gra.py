import pygame, os, sys, random, time

pygame.init()


###    Grafika    ###
# Grafika i skalowanie botów
bot_lvl_1_image = pygame.image.load(os.path.join('graph','bot_lvl_1.png'))
bot_lvl_2_image = pygame.image.load(os.path.join('graph','bot_lvl_2.png'))
bot_lvl_3_image = pygame.image.load(os.path.join('graph','bot_lvl_3.png'))
bot_lvl_4_image = pygame.image.load(os.path.join('graph','bot_lvl_4.png'))
bot_lvl_5_image = pygame.image.load(os.path.join('graph','bot_lvl_5.png'))
bot_lvl_6_image = pygame.image.load(os.path.join('graph','bot_lvl_6.png'))

bot_lvl_1_image = pygame.transform.scale(bot_lvl_1_image,(100,100))
bot_lvl_2_image = pygame.transform.scale(bot_lvl_2_image,(100,100))
bot_lvl_3_image = pygame.transform.scale(bot_lvl_3_image,(100,100))
bot_lvl_4_image = pygame.transform.scale(bot_lvl_4_image,(100,100))
bot_lvl_5_image = pygame.transform.scale(bot_lvl_5_image,(100,100))
bot_lvl_6_image = pygame.transform.scale(bot_lvl_6_image,(100,100))

# Grafika i skalowanie pocisków
bullet_2_image = pygame.image.load(os.path.join('graph','bullet_2.png'))
bullet_2_image = pygame.transform.scale(bullet_2_image, (25,25))

# Grafika i skalowanie gracza
player_image = pygame.image.load(os.path.join('graph','player.png'))
player_image = pygame.transform.scale(player_image,(100,100))

# Grafika i skalowanie tła
background_image = pygame.image.load(os.path.join('graph','background.png'))
#...

###    VIDEO    ###
screen_x = 1100
screen_y = 800
player_x = screen_x/2 -50
player_y = screen_y-120

screen = pygame.display.set_mode((screen_x,screen_y))

#  Zegar i FPS
FPS = 120
clock = pygame.time.Clock()

# Pociski
bullets = []
bullet_speed = -6
click = False

# boty
bots = []
lvl = 1
bot_speed = 0.75

# gracz
player_health = 3
player_speed = 5

# punkty i pieniadze
score = 0
money = 0

score_bot = 0
money_bot = 0

# dzwieki
bullet_sound = pygame.mixer.Sound("shot.wav")
bot_sound = pygame.mixer.Sound("bot.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
win_sound = pygame.mixer.Sound("win.wav")

# Czcionki i text
font_big = pygame.font.Font("mrsmonster.ttf",150)
font = pygame.font.Font("mrsmonster.ttf",30)

game_over_txt = font_big.render("GAME OVER", False, (255,255,255))
win_txt = font_big.render("YOU WIN", False, (255,255,255))
money_txt = font.render("MONEY = " + str(money), False, (255,255,255))
score_txt = font.render("score = " + str(score), False, (255,255,255))
health_txt = font.render("HEALTH = "+str(player_health), False, (255,255,255))

mid_rect = game_over_txt.get_rect(center = (screen_x/2,screen_y/2))
score_rect = score_txt.get_rect(center = (100,100))
money_rect = money_txt.get_rect(center = (100,125))
health_rect = money_txt.get_rect(center = (100,75))

class Bot(pygame.Rect):
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.h = 100
        self.w = 100
        self.img = img

    def move(self):
        self.y += bot_speed

    def draw(self):
        screen.blit(self.img,(self.x,self.y))

class Bullet(pygame.Rect):
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.h = 100
        self.w = 100
        self.img = img

    def move(self):
        self.y += bullet_speed

    def draw(self):
        screen.blit(self.img,(self.x,self.y))

class Player(pygame.Rect):
    def __init__(self,x,y,img):
        self.x = player_x
        self.y = player_y
        self.h = 100
        self.w = 100
        self.img = img

    def draw(self):
        screen.blit(self.img,(self.x,self.y))


run = True

    # Tworzenie botów
def bot_spawn():
    for i in range(20):
        bot = Bot(random.randint(20, screen_x-100), random.randint(-2000 ,-60),bot_lvl_1_image )
        bots.append(bot)



while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit(0)



    # gracz

    player = Player(player_x, player_y,player_image)

#   Poruszanie gracza

    if pygame.key.get_pressed()[pygame.K_d]:
        player_x += player_speed
    if pygame.key.get_pressed()[pygame.K_a]:
        player_x += -player_speed
    if pygame.key.get_pressed()[pygame.K_w]:
        player_y += -player_speed
    if pygame.key.get_pressed()[pygame.K_s]:
        player_y += player_speed

#   kolizja gracza z botami, utrata HP

    for bot in bots:
        if bot.colliderect(player):
            bots.remove(bot)
            player_health -= 1
            if player_health == 0:
                #run = False
                bot_speed = 0
                game_over_sound.play(1)
            print(player_health)
            bot_sound.play()
            break

# kolizja gracza z granicami mapy

    if player_x <= 2:
        player_x = 2
    elif player_x >= screen_x-100:
        player_x = screen_x-100
    if player_y <= 2:
        player_y = 2
    elif player_y >= screen_y-100:
        player_y = screen_y-100



    # Boty

#   generowanie botów i poziomy
    if len(bots) == 0:
        bot_spawn()
        lvl += 1
        bot_speed += 1
        bot_lvl_1_image = locals()["bot_lvl_" + str(lvl) + "_image"]
        if lvl == 6:
            run = False
            win_sound.play()

#   usuwanie botów po wyjściu za mapę

    for bot in bots:
        bot.move()
        if bot.y > screen_y:
            bots.remove(bot)
            player_health -= 1



    # Strzelanie

#   tworzenie pocisków

    if pygame.key.get_pressed()[pygame.K_SPACE] and not click:
        bullet = Bullet(player_x+38, player_y, bullet_2_image)
        bullets.append(bullet)
        bullet_sound.play()
        click = True

#   ograniczenie strzelania serią

    if event.type == pygame.KEYUP:
        click = False

#   usuwanie pocisków lecących poza obszar mapy

    for bullet in bullets:
        bullet.move()
        if bullet.y < 0:
            bullets.remove(bullet)

#   kolizja pocisków z botami

    for bullet in bullets:
        for bot in bots:
            if bot.colliderect(bullet):
                bots.remove(bot)
                bullets.remove(bullet)
                score += 10 * lvl
                money += 2 * lvl
                bot_sound.play()
                break



    # wyświetlanie
    money_txt = font.render("MONEY = " + str(money), False, (255,255,255))
    score_txt = font.render("SCORE = " + str(score), False, (255,255,255))
    health_txt = font.render("HEALTH = "+str(player_health), False, (255,255,255))
    
    screen.fill((0, 0, 0))
    screen.blit(background_image,(0,0))
    screen.blit(score_txt, score_rect)
    screen.blit(money_txt, money_rect)
    screen.blit(health_txt, health_rect)

    if player_health == 0:
        screen.blit(game_over_txt, mid_rect)
        bot_speed = 0
    if lvl == 6 :
        screen.blit(win_txt, mid_rect)
    for bot in bots:
        bot.draw()
    for bullet in bullets:
        bullet.draw()

    player.draw()
    pygame.display.update()

    # FPS
    clock.tick(FPS)