from settings import *
import pygame
from player import Player
from sprites import *
import random
from pytmx.util_pygame import load_pygame
from groups import AllSprites 

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Love Quest")
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        
    
    def setup(self):
        map = load_pygame(join('data','maps','world.tmx'))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width,obj.height)), True, (self.all_sprites, self.collision_sprites))
        
        for x,y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):
                s = CollisionSprite((obj.x, obj.y), obj.image, False, (self.all_sprites, self.collision_sprites))
                if obj.name == 'Princess':
                    princess = s

        enemy_types = ['bat', 'blob', 'skeleton']
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), princess, self.all_sprites, self.collision_sprites)
            elif obj.name == 'Enemy':
                enemy_type = random.choice(enemy_types)
                Enemy((obj.x, obj.y), enemy_type, self.player, self.all_sprites, self.collision_sprites)



    def run(self):
        while self.running:
            dt = self.clock.tick()/1000
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)
            # draw
            self.display_surface.fill('black')
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        pygame.quit()
    
   


if __name__ == '__main__':
    game = Game()
    game.setup()
    game.run()
