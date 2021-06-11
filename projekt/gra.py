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
atack_speed = 30
bullets_timer = atack_speed
bullet_speed = -6


# boty
bots = []
lvl = 1
bot_speed = 0.5

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
money_rect = money_txt.get_rect(center = (100,130))
health_rect = money_txt.get_rect(center = (100,70))

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

    # Tworzenie botów
def bot_spawn():

    for i in range(20):
        bot = Bot(random.randint(20, screen_x-100), random.randint(-2000 ,-60),bot_lvl_1_image )
        bots.append(bot)

    # MENU
def text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)

def options():
    while True:
        screen.fill((0, 0, 0))
        text('CONTROLS :', font, (255,255,255), screen, screen_x/2 -70, 70)  
        text('A - move left ', font, (255,255,255), screen, screen_x/4 , 130)  
        text('D - move right ', font, (255,255,255), screen, screen_x/4 , 190)  
        text('S - move down ', font, (255,255,255), screen, screen_x/4 , 250)  
        text('W - move up', font, (255,255,255), screen, screen_x/4 , 310)  
        text('SPACE - shoot', font, (255,255,255), screen, screen_x/4 , 370)
        text('B - shop', font, (255,255,255), screen, screen_x/4 , 430)    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()


        pygame.display.update()

def shop():
    global player_speed
    global atack_speed
    global player_health
    global money

    while True:
        click = False
        mx, my = pygame.mouse.get_pos()
        
        screen.fill((0, 0, 0))

        text('SHOP', font, (150,155,255), screen, screen_x/2 -50, 70)
        text('UPDATE FIRE SPEED - 150', font, (0,255,0), screen, screen_x/2 -150, 210)
        text('UPDATE PLAYER SPEED - 80', font, (0,255,0), screen, screen_x/2 -150, 360)
        text('UPDATE PLAYER HEALTH - 200', font, (0,255,0), screen, screen_x/2 -150, 510)
        text('EXIT', font, (0,255,0), screen, screen_x/2 -25, 660)

        button_1 = pygame.Rect(452 ,250, 200, 50)
        button_2 = pygame.Rect(452 ,400, 200, 50)
        button_3 = pygame.Rect(452 ,550, 200, 50)
        button_4 = pygame.Rect(452 ,700, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if button_1.collidepoint((mx,my)) and click == True and money >= 150:
            atack_speed = 15
            money -= 150
        if button_2.collidepoint((mx,my)) and click == True and money >= 80:
            player_speed += 2
            money -= 80
        if button_3.collidepoint((mx,my)) and click == True and money >= 200:
            player_health += 1
            money -= 200
        if button_4.collidepoint((mx,my)) and click == True:
            game()

        pygame.draw.rect(screen, (250, 100, 100), button_1)
        pygame.draw.rect(screen, (250, 100, 100), button_2)
        pygame.draw.rect(screen, (250, 100, 100), button_3)
        pygame.draw.rect(screen, (250, 100, 100), button_4)


        pygame.display.update()    

def main_menu():
    while True:
        click = False
        mx, my = pygame.mouse.get_pos()
        
        screen.fill((0, 0, 0))
        text('ASHBRINGER AWAITS', font, (150,155,255), screen, screen_x/2 -125, 70)
        text('START', font, (0,255,0), screen, screen_x/2 -33, 210)
        text('OPTIONS', font, (0,255,0), screen, screen_x/2 -50, 360)
        text('EXIT', font, (0,255,0), screen, screen_x/2 -25, 510)

        button_1 = pygame.Rect(452 ,250, 200, 50)
        button_2 = pygame.Rect(452 ,400, 200, 50)
        button_3 = pygame.Rect(452 ,550, 200, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        if button_1.collidepoint((mx,my)) and click == True:
            game()
        if button_2.collidepoint((mx,my)) and click == True:
            options()
        if button_3.collidepoint((mx,my)) and click == True:
            sys.exit(0)

        pygame.draw.rect(screen, (250, 100, 100), button_1)
        pygame.draw.rect(screen, (250, 100, 100), button_2)
        pygame.draw.rect(screen, (250, 100, 100), button_3)


        pygame.display.update()

def game():

    run = True
    global player_x
    global player_y
    global screen_x
    global screen_y
    global screen
    global lvl
    global bots
    global bot_speed
    global money
    global score
    global player_health
    global click
    global bot_lvl_1_image
    global bot_lvl_2_image
    global bot_lvl_3_image
    global bot_lvl_4_image
    global bot_lvl_5_image
    global bot_lvl_6_image
    global bullets_timer
    global atack_speed
    global player_speed



    while run:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_menu()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                shop()
            



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
        if len(bots) == 0 and lvl != 6:
            bot_spawn()
            lvl += 1
            bot_speed += 0.7
            bot_lvl_1_image = globals()["bot_lvl_" + str(lvl) + "_image"]
            # if lvl == 7:
            #     run = False
            #     win_sound.play()

    #   usuwanie botów po wyjściu za mapę

        for bot in bots:
            bot.move()
            if bot.y > screen_y:
                bots.remove(bot)
                player_health -= 1



        # Strzelanie

    #   tworzenie pocisków
        if (bullets_timer < atack_speed):
            bullets_timer += 1
        if pygame.key.get_pressed()[pygame.K_SPACE] and bullets_timer >= atack_speed:
            bullet = Bullet(player_x+38, player_y, bullet_2_image)
            bullets.append(bullet)
            bullets_timer = 0
            bullet_sound.play()

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
            player_speed = 0
            atack_speed = 10000000000
        if lvl == 6 and bots == 0 :
            screen.blit(win_txt, mid_rect)
            win_sound.play()
        for bot in bots:
            bot.draw()
        for bullet in bullets:
            bullet.draw()

        player.draw()
        pygame.display.update()

        # FPS
        clock.tick(FPS)
main_menu()