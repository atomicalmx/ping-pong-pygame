import pygame, time, os, random

### Variables ###
game_title = "Epic Ping-Pong Game - Mikail @atomicalmx"
pygame.init()
scene_lebar = 640
scene_tinggi = 480
scene = pygame.display.set_mode((scene_lebar,scene_tinggi))
pygame.display.set_caption(game_title)
FPS = pygame.time.Clock()
p1_point = 0
p2_point = 0
p1_win = False
p2_win = False
score_to_win = 3
rct = pygame.sprite.collide_rect
player1_img = "./sprites/mabel.png"
player2_img = "./sprites/alice.png"
player_speed = 3
ball_img = "./sprites/ball.png"
bg_file = pygame.image.load("./sprites/grasshd.jpg")
background = pygame.transform.scale(bg_file,(640,480))

# Colors
col_fg = (255, 255, 255)
col_yellow = (245, 241, 59)
col_red = (190, 33, 33)
col_green = (65, 255, 125)

# Sound
ba_sfx_file = "./audio/ba.wav"
goal_sfx_file = "./audio/goy.wav"
lose_sfx_file = "./audio/lose_game.wav"
win_sfx_file = "./audio/win_game.wav"
win_bgm_file = "./audio/endgame.ogg"
bgm_file = "./audio/infinite_looping_maze.ogg"
bgm = pygame.mixer.init()
bgm = pygame.mixer.music.load(bgm_file)
bgm = pygame.mixer.music.play()
bgm = pygame.mixer.music.set_volume(0.5)
goal_sfx = pygame.mixer.Sound(goal_sfx_file)
lose_sfx = pygame.mixer.Sound(lose_sfx_file)
win_sfx = pygame.mixer.Sound(win_sfx_file)
ba_sfx = pygame.mixer.Sound(ba_sfx_file)

### Functions ###
class GameSprite(pygame.sprite.Sprite):
     def  __init__(self, image, x, y, ukuran_x, ukuran_y, speed):
          super().__init__()
          self.ukuran_x = ukuran_x
          self.ukuran_y = ukuran_y
          self.image = pygame.transform.scale(pygame.image.load(image),(ukuran_x, ukuran_y))
          self.rect = self.image.get_rect()
          self.rect.x = x
          self.rect.y = y
          self.speed = speed
     def show(self):
          scene.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
     def moveManual_1(self):
          buttonPress = pygame.key.get_pressed()
          self.image = pygame.transform.scale(pygame.image.load("./sprites/mabel.png"),(self.ukuran_x, self.ukuran_y))
          if buttonPress[pygame.K_w] and self.rect.y > 0:
               self.image = pygame.transform.scale(pygame.image.load("./sprites/mabel_down.png"),(self.ukuran_x, self.ukuran_y))
               self.rect.y -= self.speed
          if buttonPress[pygame.K_s] and self.rect.y < scene_tinggi-self.ukuran_y:
               self.image = pygame.transform.scale(pygame.image.load("./sprites/mabel_up.png"),(self.ukuran_x, self.ukuran_y))
               self.rect.y += self.speed

     def moveManual_2(self):
          buttonPress = pygame.key.get_pressed()
          self.image = pygame.transform.scale(pygame.image.load("./sprites/alice.png"),(self.ukuran_x, self.ukuran_y))
          if buttonPress[pygame.K_UP] and self.rect.y > 0:
               self.image = pygame.transform.scale(pygame.image.load("./sprites/alice_down.png"),(self.ukuran_x, self.ukuran_y))
               self.rect.y -= self.speed
          if buttonPress[pygame.K_DOWN] and self.rect.y < scene_tinggi-self.ukuran_y:
               self.image = pygame.transform.scale(pygame.image.load("./sprites/alice_up.png"),(self.ukuran_x, self.ukuran_y))
               self.rect.y += self.speed

     def moveAI(self):
          global ballfag
          numbers = [10,20,30,40,50,60,70,80,90,100,1+200]
          if self.rect.y <= ballfag.rect.y - random.choice(numbers):
               self.arah = "up"
          if self.rect.y >= ballfag.rect.y - random.choice(numbers):
               self.arah = "down"

          if self.arah == "up":
               self.rect.y += self.speed
          if self.arah == "down":
               self.rect.y -= self.speed
               
class Ball(GameSprite):
     arah = ""
     arahbounce = ""
     lmao = ["up", "down"]
     def moveAuto(self, start, end, player1, player2): # Left to right loop back
          global rct
          if self.rect.x <= start:
               self.arah = "right"
          if self.rect.x >= end:
               self.arah = "left"

          elif rct(self, player1): # Player bounce the ball
               self.arah = "right"
               ba_sfx.play()
               if self.rect.y <= scene_tinggi/2:
                    self.arahbounce = "up"
               if self.rect.y >= scene_tinggi/2:
                    self.arahbounce = "down"
          elif rct(self, player2): 
               self.arah = "left"
               ba_sfx.play()
               if self.rect.y <= scene_tinggi/2:
                    self.arahbounce = random.choice(self.lmao)
               if self.rect.y >= scene_tinggi/2:
                    self.arahbounce = random.choice(self.lmao)

          if self.rect.y <= 0: # Bounce with the wall
               self.arahbounce = "down"
          if self.rect.y >= scene_tinggi - self.ukuran_y:
               self.arahbounce = "up"

          if self.arah == "right": 
               self.rect.x += self.speed
          if self.arah == "left":
               self.rect.x -= self.speed
          if self.arahbounce == "down":
               self.rect.y += self.speed
          if self.arahbounce == "up":
               self.rect.y -= self.speed
     def throwBall(self, p1,p2):
          global player1, player2
          if p1 == "p1":
               self.arah = "left"
               self.rect.x = player2.rect.x-self.ukuran_x
               self.rect.y = player2.rect.y

          if p2 == "p2":
               self.arah = "right"
               self.rect.x = player1.rect.x+self.ukuran_x
               self.rect.y = player1.rect.y


          if self.arah == "right": 
               self.rect.x += self.speed
          if self.arah == "left":
               self.rect.x -= self.speed

### Building objects ###
player1 = Player(player1_img,24,26,64,66,player_speed)
player2 = Player(player2_img,scene_lebar-84,scene_tinggi-86,64,66,player_speed)
ballfag = Ball(ball_img,0,scene_tinggi/2-44,44,44,player_speed+3)
score_bg = GameSprite("./sprites/score_bg.png",scene_lebar/2-45,0,90,53,0)

### Fonts ###
game_font = "./fonts/font.ttf"
pygame.font.init()
panel_file = pygame.image.load("./sprites/panel.png")
panel = pygame.transform.scale(panel_file,(640,100))

# Win/Lose text
win = pygame.font.Font(game_font, 80).render('PLAYER 1 WIN', True,col_yellow)
lose = pygame.font.Font(game_font, 80).render('PLAYER 2 WIN', True,col_red)

# Score text
seph = pygame.font.Font(game_font, 22).render(":", True,col_fg)
info_1_txt = pygame.font.Font(game_font, 22).render("P1", True,col_yellow)
info_2_txt = pygame.font.Font(game_font, 22).render("P2", True,col_red)
p1_txt = pygame.font.Font(game_font, 22).render(str(p1_point), True,col_fg)
p2_txt = pygame.font.Font(game_font, 22).render(str(p2_point), True,col_fg)

notif_txt = pygame.font.Font(game_font, 22).render("Game is finished. Press Q to exit", True,col_fg)

### Runnning ###
game_run = True # If false then the game will quits
game_finish = False # If true then the game will be froze. For WIN/LOSE stuff
print("\nGame is started!")
while game_run:
     # Quitting the game
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               print('[Info] Game exited')
               game_run = False

     # Quiting game with a "Q" keybind 
     if pygame.key.get_pressed()[pygame.K_q]:
          print('[Info] Game exited')
          game_run = False

     # Launching some stuff
     scene.blit(background,(0,0))
     score_bg.show()
     # Launch fonts
     scene.blit(p1_txt,(scene_lebar/2-24,30))
     scene.blit(p2_txt,(scene_lebar/2+14,30))
     scene.blit(info_1_txt,(scene_lebar/2-31,5))
     scene.blit(info_2_txt,(scene_lebar/2+11,5))
     scene.blit(seph,(scene_lebar/2-2,5))

     # Define WIN/LOSE
     if p1_point == 3:
          p1_win = True
          ballfag.rect.x = -200
          ballfag.rect.y = -200
          winico = GameSprite("./sprites/win.png",30,player1.rect.y-50,46,46,0)
          loseico = GameSprite("./sprites/dead.png",scene_lebar-76,player2.rect.y-50,46,46,0)
          winico.show()
          loseico.show()
     if p2_point == 3:
          p2_win = True
          ballfag.rect.x = -200
          ballfag.rect.y = -200
          winico = GameSprite("./sprites/win.png",scene_lebar-76,player2.rect.y-50,46,46,0)
          loseico = GameSprite("./sprites/dead.png",30,player1.rect.y-50,46,46,0)
          winico.show()
          loseico.show()
     
     if game_finish != True:
          buttonPress = pygame.key.get_pressed()

          # Launch objects
          ballfag.show()
          player1.show()
          player2.show()
          player1.moveManual_1()
          player2.moveManual_2()
          # player2.moveAI()
          ballfag.moveAuto(0, scene_lebar-ballfag.ukuran_x, player1, player2)

          # P1 hits P2
          if ballfag.rect.x >= scene_lebar-ballfag.ukuran_x:
               p1_point += 1
               p1_txt = pygame.font.Font(game_font, 22).render(str(p1_point), True,col_green)
               goal_sfx.play()
               # ballfag.rect.x = scene_lebar/2-ballfag.ukuran_x
               # ballfag.rect.y = scene_tinggi/2-ballfag.ukuran_y
               ballfag.throwBall("p1", "p1")

          # P2 hits P1
          if ballfag.rect.x <= 0: 
               p2_point += 1
               p2_txt = pygame.font.Font(game_font, 22).render(str(p2_point), True,col_green)
               goal_sfx.play()
               ballfag.throwBall("p2", "p2")
               
          # Define the point colors
          if p1_point == p2_point:
               p1_txt = pygame.font.Font(game_font, 22).render(str(p1_point), True,col_fg)
               p2_txt = pygame.font.Font(game_font, 22).render(str(p2_point), True,col_fg)
          if p1_point >= p2_point:
               p2_txt = pygame.font.Font(game_font, 22).render(str(p2_point), True,col_fg)
          if p1_point <= p2_point:
               p1_txt = pygame.font.Font(game_font, 22).render(str(p1_point), True,col_fg)

          # WIN/LOSE. In this case I'm gonna use player 1 so..
          # If P1 win, P2 loses.
          if p1_win == True:
               scene.blit(panel,(0,190))
               scene.blit(win,(60,205))
               bgm = pygame.mixer.music.stop()
               win_bgm = pygame.mixer.init()
               win_bgm = pygame.mixer.music.load(win_bgm_file)
               win_bgm = pygame.mixer.music.play()
               win_bgm = pygame.mixer.music.set_volume(0.5)
               win_sfx.play()
               scene.blit(notif_txt,(scene_lebar/2-135,scene_tinggi-30))
               game_finish = True

          # If P1 lose, P2 wins
          if p2_win == True:
               scene.blit(panel,(0,190))
               scene.blit(lose,(60,205))
               bgm = pygame.mixer.music.stop()
               win_bgm = pygame.mixer.init()
               win_bgm = pygame.mixer.music.load(win_bgm_file)
               win_bgm = pygame.mixer.music.play()
               win_bgm = pygame.mixer.music.set_volume(0.5)
               lose_sfx.play()
               scene.blit(notif_txt,(scene_lebar/2-135,scene_tinggi-30))
               game_finish = True

          # Important. Makes the game able to move stuff
          FPS.tick(60)
          pygame.display.update()
