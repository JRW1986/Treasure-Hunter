import pygame, sys
from settings import *
from level import Level
from overworld import Overworld
from ui import UI
from score import Score

class Game:
    def __init__(self):

        # game attributes
        self.max_level = 0
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0
        
        # audio
        self.level_bg_music = pygame.mixer.Sound('audio/level_music.wav')
        self.overworld_bg_music = pygame.mixer.Sound('audio/overworld_music.wav')

        # overworld creation
        self.start = self.menu()
        self.status = 'start'
        self.overworld_bg_music.play(loops = -1)
        

        # user interface
        self.ui = UI(screen)

    def menu(self):
         start_menu = pygame.image.load('graphics/decoration/start.png').convert_alpha()
         start_menu = pygame.transform.scale(start_menu,(screen_width,screen_height))
         screen.blit(start_menu,(0,0))
         if pygame.key.get_pressed()[pygame.K_RETURN]:
                self.overworld_bg_music.stop()
                self.create_overworld(0,0)
              
    def game_over(self):
         game_over_menu = pygame.image.load('graphics/decoration/game-over.png').convert_alpha()
         game_over_menu = pygame.transform.scale(game_over_menu,(screen_width,screen_height))
         screen.blit(game_over_menu,(0,0))
         if pygame.key.get_pressed()[pygame.K_RETURN]:
              self.level_bg_music.stop()
              self.create_overworld(0,0)
              

    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)
        self.level_bg_music.set_volume(0.2)
        
    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        
    def change_coins(self,amount):
         self.coins += amount    

    def change_health(self,amount):
         self.cur_health += amount

    def check_game_over(self):
         if self.cur_health <= 0:
              self.high_score()
              self.game_over()
              self.status = 'game_over'
              self.cur_health = 100
              self.coins = 0
              self.max_level = 0
              self.level_bg_music.stop()
              self.overworld_bg_music.play(loops = -1)

    def high_score(self):
            with open('high_score.txt','r') as file:
                high_score = int(file.read())
            if self.coins > high_score:
                with open('high_score.txt','w') as file:
                    file.write(str(self.coins))

    def run(self):
        if self.status == 'start':
            self.menu()
        elif self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'game_over':
            self.game_over()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health,self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()
            

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('grey')
	game.run()
	
	pygame.display.update()
	clock.tick(60)