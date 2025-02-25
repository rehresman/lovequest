from settings import *
from os import walk
import math
from sprites import TextSprite, Entity


class Player(Entity):
    def __init__(self, pos, princess, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.load_images('player')
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)
        self.winner = False
        self.princess = princess
        self.love_music_playing = False
        self.display_surface = groups.display_surface

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 500
        self.collision_sprites = collision_sprites
        self.distance_to_love = 10000

        self.font = pygame.font.Font(join('images','Minecraft.ttf'), 75)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
            

    def move(self, dt):
        self.direction = self.direction.normalize() if self.direction.length() > 0 else self.direction
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

        # love
        self.distance_to_love = math.dist(self.rect.center,self.princess.rect.center)
        if self.distance_to_love < 150 and not self.love_music_playing:
            self.winner = True
    

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if self.hitbox_rect.colliderect(sprite.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def speak(self):
        text = "Princess Annabelle: You found me! It's scary out there.  Maybe we should leave together?"
        TextSprite((0,0), text, self.groups)

    def win(self):
        if self.winner and not self.love_music_playing:
            self.love_music_playing = True
            love_music = pygame.mixer.Sound(join('audio', '8 bit love.wav'))
            love_music.play(-1)
            self.speed = 0
            #self.speak()


    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt, True)
        self.win()
