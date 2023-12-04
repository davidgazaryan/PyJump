import pygame
import sys
from random import randint, choice

pygame.init()

game_active = False

screen = pygame.display.set_mode([800,400])

test_font = pygame.font.Font(None,40)
text_surface = test_font.render('PyJump',False,(51,51,51))

bison_image = pygame.image.load('characters/Bison.png').convert_alpha()
bison_image = pygame.transform.scale(bison_image,[90,90])
bison_rectangle = bison_image.get_rect(bottomright= (700,350))

bat_image = pygame.image.load('characters/Bat.png').convert_alpha()
bat_image = pygame.transform.scale(bat_image,(80,80))
bat_rectangle = bat_image.get_rect(bottomright= (700,350))

player_image_1 = pygame.image.load('characters/Mario.png').convert_alpha()
player_image_1 = pygame.transform.scale(player_image_1,[75,75])
player_image_2 = pygame.image.load('characters/Mario1.png').convert_alpha()
player_image_2 = pygame.transform.scale(player_image_2, (75,75))
player_jump = pygame.image.load('characters/Mariojump.png').convert_alpha()
player_jump = pygame.transform.scale(player_jump, (75,75))

player_walk = [player_image_1, player_image_2]
player_index = 0

player_surface = player_walk[player_index]

player_rectangle = player_surface.get_rect(midbottom = (80,350))
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer, 1500)  # Indicates how fast the enemies are spawning and coming towards you, the higher the number the slower

obstacle_rect_list = []


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_image_1 = pygame.image.load('characters/Mario.png').convert_alpha()
        player_image_1 = pygame.transform.scale(player_image_1, [75, 75])
        player_image_2 = pygame.image.load('characters/Mario1.png').convert_alpha()
        player_image_2 = pygame.transform.scale(player_image_2, (75, 75))
        self.player_jump = pygame.image.load('characters/Mariojump.png').convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, (75, 75))
        self.player_walk = [player_image_1, player_image_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect(midbottom=(80, 350))
        self.gravity = 0

    def player_input(self):
        if self.rect.bottom >= 350:
            self.rect.bottom = 350
            self.gravity = 0
        elif self.rect.top <= 0:
            self.rect.top = 0

        self.gravity += 1.5
        self.rect.y += self.gravity

    def apply_gravity(self):
        jump = -150
        self.rect.y += jump

    def animation(self):
        if self.rect.bottom < 300: self.image = self.player_jump
        else:
            self.player_index += 0.7
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.animation()
        self.player_input()

    def restart(self):
        self.rect = self.image.get_rect(midbottom=(80,350))
        self.gravity = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bat':
            bat_image = pygame.image.load('characters/Bat.png').convert_alpha()
            bat_image = pygame.transform.scale(bat_image, (80, 80))
            y_position = 200
            self.image = bat_image
        else:
            bison_image = pygame.image.load('characters/Bison.png').convert_alpha()
            bison_image = pygame.transform.scale(bison_image, [90, 90])
            y_position = 350
            self.image = bison_image

        self.rect = self.image.get_rect(midbottom = (randint(800,1400),y_position))

    def destroy(self,count):

        if -50 < self.rect.x <= 0:
            count += 1
            self.kill()

    def update(self):
        self.destroy(0)
        self.rect.x -= 50


class Background:
    def __init__(self):
        pygame.display.set_caption('PyJump')
        self.score = test_font.render('Score:',False,(51,51,51))
        self.count_score = 0

    def score_text(self):
        score = self.score.get_rect(topright = (760,11))
        screen.blit(self.score,score)

    def score_count(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_r]: self.count_score = 0

        self.count_score += len([obstacle for obstacle in obstacles if obstacle.rect.left <= 0]) #Add 1 for each object leaving screen

        count: str = test_font.render(str(self.count_score),False,(255,255,255))
        score_rect = count.get_rect(midtop=(775,12))
        screen.blit(count,score_rect)

    @staticmethod
    def surfaces(self):
        my_background = pygame.image.load('1624.jpg').convert_alpha()
        my_background = pygame.transform.scale(my_background, [800,400])
        return screen.blit(my_background, [0, 0])

    @staticmethod
    def title(self):
        return screen.blit(text_surface, [345, 10])


def obstacle_collisions():
    global game_active
    if pygame.sprite.spritecollide(player.sprite,obstacles,False):
        obstacles.empty()  # Empties the list of enemies so that game can restart immediately
        game_active = False
    else:
        game_active = True

def player_animation():
    global player_surface, player_index

    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += .7
        if player_index >= len(player_walk): player_index = 0

        player_surface = player_walk[int(player_index)]

def obstacle_movement(obstacle_list):  # Function for spawning enemies
    global my_game
    if obstacle_list:
        for enemy in obstacle_list:
            enemy.x -= 50

            if enemy.y > 250: screen.blit(bison_image, enemy)  # Used to differentiate ground animal from sky animal
            else: screen.blit(bat_image, enemy)

            obstacle_list = [el for el in obstacle_list if el.x > -10]  # Deletes items from list if they get to end of screen

        return obstacle_list

    else: return []

def obstacle_collision(character, obstacle_list):
    global game_active
    for i in obstacle_list:
        if character.colliderect(i):
            return False

    return True


player = pygame.sprite.GroupSingle()
player_sprite = Player()
player.add(player_sprite)

obstacles = pygame.sprite.Group()

clock = pygame.time.Clock()
my_game = Background()

while True:
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        QUIT = pygame.key.get_pressed()
        if QUIT[pygame.K_ESCAPE]:  # If escape is pressed anytime during game, game exits
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_sprite.apply_gravity()

        if event.type == timer and game_active:
            obstacles.add(Obstacle(choice(['bat','bison','bison'])))  # Put bison twice so that more bison spawn than bats statistically speaking

    if game_active:
        Background.surfaces(None)


        my_game.score_text()
        my_game.title(None)

        player.draw(screen)
        player.update()

        obstacles.draw(screen)
        obstacles.update()

        obstacle_collisions()

        my_game.score_count()

        if bison_rectangle.colliderect(50,50,25,50):
            game_active = False


    elif not game_active:
        obstacle_rect_list.clear()  # Clears the list so that game can start right away and enemies start at initial positions
        screen.fill(color='gold')

        score_render = test_font.render(str(my_game.score_count()),False,'white')

        loading_title = pygame.font.SysFont('Comic Sans MS', 60,True,False)
        loading_title = loading_title.render('Jumpman',False,(200,50,50))
        load_screen = pygame.transform.scale(player_image_1,(150,150))
        screen.blits([(load_screen,(320,120)),(loading_title,(280,10))])

        restart = test_font.render('Click r to restart',False,'Black')
        game_quit = pygame.font.Font.render(test_font,'Click q to exit game',False,'Black')
        screen.blits([(restart,(275,350)),(game_quit,(250,300))])

        if key[pygame.K_r]:
            game_active = True

        elif key[pygame.K_q]:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    clock.tick(60)  # While loop should not run faster than 60 times per second
