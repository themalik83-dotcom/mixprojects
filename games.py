from pygame import *


window = display.set_mode((700, 500))
display.set_caption("Football_Mini_Game")
background = transform.scale(image.load("Field.jpg"), (700, 500))


#data gambar sprite
x1 = 100
y1 = 300


x2 = 300
y2 = 300


x3 = 400
y3 = 400


sprite1 = transform.scale(image.load('team.png'), (65, 65))
sprite2 = transform.scale(image.load('enemy.png'), (65, 65))
sprite3 = transform.scale(image.load('enemy.png'), (65, 65))
speed = 5

enemy_speed1 = 6
enemy_side1 = "left"

enemy_speed2 = 6
enemy_side2 = "left"


x4 = 610
y4 = 216
sprite4 = transform.scale(image.load('standing.png'), (67, 67))


finish = False


#game loop
run = True
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('sondtrck.ogg')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

font.init()
game_font = font.Font(None, 70)
win_text = game_font.render('VICTORY!', True, (255, 215, 0))
lose_text = game_font.render('DEFEAT!', True, (180, 0, 0))
money = mixer.Sound('victory.ogg')
kick = mixer.Sound('sound.ogg')
result_text = None

while run:
   window.blit(background,(0, 0))
   window.blit(sprite1, (x1, y1))
   window.blit(sprite4, (x4, y4))
   window.blit(sprite2, (x2, y2))
   window.blit(sprite3, (x3, y3))


   for e in event.get():
       if e.type == QUIT:
           run = False


   keys_pressed = key.get_pressed()


   if keys_pressed[K_LEFT] and x1 > 5:
       x1 -= speed
   if keys_pressed[K_RIGHT] and x1 < 595:
       x1 += speed
   if keys_pressed[K_UP] and y1 > 5:
       y1 -= speed
   if keys_pressed[K_DOWN] and y1 < 395:
       y1 += speed


   if y2 <= 100:
       enemy_side1 = "right"
   if y2 >= 100 - 5:
       enemy_side1 = "left"
   if enemy_side1 == "left":
       y2 -= enemy_speed1
   else:
       y2 += enemy_speed1


   if y3 <= 100:
       enemy_side2 = "right"
   if y3 >= 200 - 85:
       enemy_side2 = "left"
   if enemy_side2 == "left":
       y3 -= enemy_speed2
   else:
       y3 += enemy_speed2

       
#cek event collision (sprite1 vs sprite2/sprite3)
   if not finish:
       if Rect(x1, y1, 100, 100).colliderect(Rect(x2, y2, 100, 100)):
           finish = True
           result_text = lose_text
           kick.play()
       elif Rect(x1, y1, 100, 100).colliderect(Rect(x3, y3, 65, 65)):
           finish = True
           result_text = win_text
           money.play()
   else:
       window.blit(result_text, (200, 200))


   display.update()
   clock.tick(FPS)



