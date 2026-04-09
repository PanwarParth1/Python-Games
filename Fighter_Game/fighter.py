import pygame 
import os
pygame.font.init()
pygame.mixer.init()


WIDTH , HEIGHT = 1920,1080
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fighter Game")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','sound1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','sound2.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicseans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

FPS = 60
VEL = 10
BULLET_VEL = 50
MAX_BULLETS = 5

PLAYER_WIDTH , PLAYER_HEIGHT = 70 , 70

LEFT_HIT = pygame.USEREVENT + 1
RIGHT_HIT = pygame.USEREVENT + 2

LEFT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets','player1.png'))
LEFT_PLAYER = pygame.transform.rotate(
    pygame.transform.scale(LEFT_PLAYER_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT)),63)

RIGHT_PLAYER_IMAGE = pygame.image.load(os.path.join('Assets','player2.png'))
RIGHT_PLAYER = pygame.transform.rotate(
    pygame.transform.scale(RIGHT_PLAYER_IMAGE,(PLAYER_WIDTH,PLAYER_HEIGHT)),90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','background.jpg')),(WIDTH,HEIGHT))


def draw_window(right,left,right_bullets,left_bullets,left_player_health,right_player_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    right_player_health_text = HEALTH_FONT.render("Health: " + str(right_player_health),1,WHITE)
    left_player_health_text = HEALTH_FONT.render("Health: " + str(left_player_health),1,WHITE)

    WIN.blit(right_player_health_text,(WIDTH - right_player_health_text.get_width() - 10,10))
    WIN.blit(left_player_health_text,(10,10))

    WIN.blit(LEFT_PLAYER,(left.x,left.y))
    WIN.blit(RIGHT_PLAYER,(right.x,right.y))

    for bullet in right_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in left_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()

def left_movement(keys_pressed,left):
    if keys_pressed[pygame.K_a] and left.x - VEL > 0:
        left.x -= VEL 
    if keys_pressed[pygame.K_d] and left.x + VEL + left.width < BORDER.x:
        left.x += VEL
    if keys_pressed[pygame.K_w] and left.y - VEL > 0:
        left.y -= VEL
    if keys_pressed[pygame.K_s] and left.y + VEL + left.height < HEIGHT:
        left.y += VEL

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2,
                        HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)
    

def right_movement(keys_pressed,right):
    if keys_pressed[pygame.K_UP] and right.y - VEL > 0:
        right.y -= VEL
    if keys_pressed[pygame.K_DOWN] and right.y + VEL + right.height < HEIGHT:
        right.y += VEL
    if keys_pressed[pygame.K_RIGHT] and right.x + VEL + right.width < WIDTH:
        right.x += VEL
    if keys_pressed[pygame.K_LEFT] and right.x - VEL > BORDER.x + BORDER.width:
        right.x -= VEL


def handle_bullets(left_bullets,right_bullets,left,right):

    for bullet in left_bullets[:]:
        bullet.x += BULLET_VEL

        if right.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIGHT_HIT))
            left_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            left_bullets.remove(bullet)


    for bullet in right_bullets[:]:
        bullet.x -= BULLET_VEL

        if left.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LEFT_HIT))
            right_bullets.remove(bullet)

        elif bullet.x < 0:
            right_bullets.remove(bullet)


def main():
    right = pygame.Rect(700,200,PLAYER_WIDTH,PLAYER_HEIGHT)
    left = pygame.Rect(100,200,PLAYER_WIDTH,PLAYER_HEIGHT)

    left_bullets = []
    right_bullets = []
    
    right_player_health = 10
    left_player_health = 10

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LCTRL and len(left_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        left.x + left.width,
                        left.y + left.height//2 - 2,
                        10,5)
                    left_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(right_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        right.x,
                        right.y + right.height//2 - 2,
                        10,5)
                    right_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RIGHT_HIT:
                left_player_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == LEFT_HIT:
                right_player_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""

        if right_player_health <= 0:
            winner_text = "Right player win!"

        if left_player_health <= 0:
            winner_text = "Left player Win!"

        if winner_text != "":
            draw_winner(winner_text)
            run = False

        keys_pressed = pygame.key.get_pressed()
        left_movement(keys_pressed,left)
        right_movement(keys_pressed,right)

        handle_bullets(left_bullets,right_bullets,left,right)

        draw_window(right,left,right_bullets,left_bullets,right_player_health,left_player_health)

    main()


if __name__ == "__main__":
    main()