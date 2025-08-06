import pygame
import time
import os

### Variables
game_title = "Epic ping-pong game - Made by Mikail"
pygame.init()
scene_lebar = 640
scene_tinggi = 480
scene = pygame.display.set_mode((scene_lebar,scene_tinggi))
pygame.display.set_caption(game_title)
FPS = pygame.time.Clock()

# Colors
col_fg = (165, 165, 165)
col_yellow = (245, 241, 59)
col_red = (210, 63, 61)
col_green = (65, 255, 125)

# Sound
bgm_file = "./audio/infinite_looping_maze.ogg"
bgm = pygame.mixer.init()
bgm = pygame.mixer.music.load(bgm_file)
bgm = pygame.mixer.music.play()
bgm = pygame.mixer.music.set_volume(0.5)

bg_file = pygame.image.load("./sprites/bg.png")
background = pygame.transform.scale(bg_file,(682,495))

### Functions
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
          tombol = pygame.key.get_pressed()
          if tombol[pygame.K_w] and self.rect.y > 0:
               self.rect.y -= self.speed

          if tombol[pygame.K_s] and self.rect.y < scene_tinggi-self.ukuran_y:
               self.rect.y += self.speed
     def moveManual_2(self):
          tombol = pygame.key.get_pressed()
          if tombol[pygame.K_UP] and self.rect.y > 0:
               self.rect.y -= self.speed

          if tombol[pygame.K_DOWN] and self.rect.y < scene_tinggi-self.ukuran_y:
               self.rect.y += self.speed

# class ball
     # def move automatically and bounce off

### Building objects

ball_img = "./sprites/ball.png"
player1_img = "./sprites/mabel.png"
player2_img = "./sprites/alice.png"
player_speed = 6
                                   #25, 99
player1 = Player(player1_img,10,10,64,66,player_speed)
player2 = Player(player2_img,scene_lebar-74,scene_tinggi-76,64,66,player_speed)
ball = GameSprite(ball_img,scene_lebar/2-30,200,60,60,player_speed)


### Fonts


### Runnning
game_run = True # if false then the game will quit
game_selesai = False # if win or lose
while game_run:
     # Quitting the game
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               print('[Info] Game exited')
               game_run = False

     # Quiting game with a keybind
     if pygame.key.get_pressed()[pygame.K_q]:
          print('[Info] Game exited')
          game_run = False

     # Launching some stuff
     if game_selesai != True:
          scene.blit(background,(-20,0))
          ball.show()
          player1.show()
          player2.show()
          player1.moveManual_1()
          player2.moveManual_2()

          # Able to move stuff
          FPS.tick(60)

          pygame.display.update() 
