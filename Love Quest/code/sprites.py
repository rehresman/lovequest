from settings import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.invisible = False
        self.frames = {'down': [], 'up': [], 'right': [], 'left': []}
        self.state, self.frame_index = 'down', 0

    def load_images(self, target):
        for state in self.frames:
            img_folder = join(BASE_DIR, 'images')
            for folder_path, sub_folders, file_names in walk(join(img_folder, target, state)):
                    if file_names:
                        for file_name in sorted(file_names, key=lambda x: int(x.split('.')[0])):
                            full_path = join(folder_path, file_name)
                            print(full_path)
                            surf = pygame.image.load(full_path).convert_alpha()
                            self.frames[state].append(surf)

    def animate(self, dt, directional = False, always_running = False):
        # get state
        if directional:
            if self.direction.x > 0: self.state = 'right'
            if self.direction.x < 0: self.state = 'left'
            if self.direction.y > 0: self.state = 'down' 
            if self.direction.y < 0: self.state = 'up'
        # animate
        if always_running or self.direction.magnitude() > 0:
            self.frame_index += 5 * dt
        else:
            self.frame_index = 2 * int(self.frame_index / 2)
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
            


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True
        self.invisible = False
 
class TextSprite(pygame.sprite.Sprite):
    def __init__(self, pos, text, groups):
        super().__init__()(groups)
        self.text = text
        self.text_surf = self.font.render(self.text, True, (240,240,240))
        self.text_rect = self.text_surf.get_frect(midtop = pos)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, invisible, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.invisible = invisible

class Enemy(Entity):
    def __init__(self, pos, type, player, groups, collision_sprites):
        super().__init__(groups)
        self.type = type
        self.player = player
        self.image = pygame.image.load(join(BASE_DIR, 'images', 'enemies', self.type, 'down', '0.png')).convert_alpha()
        self.load_images(join(BASE_DIR, 'images','enemies', self.type))
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)
        self.collision_sprites = collision_sprites
        self.invisible = False
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 100
        self.moving = True

    def move(self, dt):
        if self.moving and not self.player.winner:
            self.direction = pygame.math.Vector2(self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)
            self.direction = self.direction.normalize()
            self.hitbox_rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            self.hitbox_rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
            self.rect.center = self.hitbox_rect.center
            if self.hitbox_rect.colliderect(self.player.hitbox_rect):
                pygame.quit()

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if sprite.rect.centerx > self.hitbox_rect.centerx:
                        self.hitbox_rect.right = sprite.rect.left
                    else:
                        self.hitbox_rect.left = sprite.rect.right
                    if hasattr(sprite, 'ground'):
                        if sprite.ground:
                            if sprite.rect.centery > self.hitbox_rect.centery:
                                self.hitbox_rect.bottom = sprite.rect.top
                            else:
                                self.hitbox_rect.top = sprite.rect.bottom
                    break

        elif direction == 'vertical':
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(self.hitbox_rect):
                    if sprite.rect.centery > self.hitbox_rect.centery:
                        self.hitbox_rect.bottom = sprite.rect.top
                    else:
                        self.hitbox_rect.top = sprite.rect.bottom
                    break
    

    def update(self, dt):
        self.move(dt)
        self.animate(dt, False, True)