import os

import pygame, random
from pygame import FULLSCREEN
from sympy.strategies.core import switch

pygame.init()
pygame.mixer.init()

left_channel = pygame.mixer.Channel(0)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

os.environ["SDL_VIDEO_CENTERED"] = "1"
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
scale_x = screen.get_width() / 1280
scale_y = screen.get_height() / 720

map = pygame.image.load("../Sprites/map.png").convert_alpha()
map = pygame.transform.scale(map, (64 * 20 *scale_x, 36 * 20 * scale_y))

note_1 = pygame.image.load("../Sprites/note.png").convert_alpha()
cursor = pygame.image.load("../Sprites/cursor.png").convert_alpha()
black = pygame.image.load("../Sprites/black.jpg").convert_alpha()
location_to_hit = pygame.image.load("../Sprites/location_to_hit.png").convert_alpha()
location_hit = pygame.image.load("../Sprites/location_hit.png").convert_alpha()
wall_sfx = pygame.mixer.Sound("../SFX/hitwall.mp3")
walk_sfx = pygame.mixer.Sound("../SFX/walking.mp3")

cursor = pygame.transform.scale(cursor, (150 * scale_x, 150 * scale_y))
cx = cursor.get_width()/2
cy = cursor.get_height()/2
font = pygame.font.Font(None, 100)
running = True

mask = pygame.mask.from_surface(map, 0)
mask_2 = pygame.mask.from_surface(cursor, 0)
mask_being_rendered = map

update_runner_array = []

mapX=4
mapY=2
map_layout_main = [
    [0, 1,1,1,3,3,1,1,1,1,1],
    [0, 1,1,2,0,0,2,1,1,1,1],
    [0, 1,1,1,0,0,1,1,1,1,1],
    [0, 2,0,0,0,0,0,0,0,0,1],
    [0, 2,0,0,0,0,1,1,1,2,1],
    [0, 1,1,1,1,0,1,1,1,1,1],
    [0, 1,1,1,0,0,1,1,1,1,1],
    [0, 1,1,1,1,1,1,1,1,1,1],
    [0]
]
map_layout_outside = [
    [0, 1,1,2,2,1],
    [0, 1,0,0,0,1],
    [0, 1,3,0,0,2],
    [0, 1,3,0,0,2],
    [0, 1,0,0,0,2],
    [0, 1,0,0,0,1],
    [0, 1,1,1,1,1],
    [0]
]
map_layout_reception = [
    [0, 1,1,1,1,1],
    [0, 2,0,0,0,3],
    [0, 1,1,2,1,1],
    [0, 1,0,0,1,1],
    [0, 1,1,1,1,1],
    [0]
]
map_layout_janitor = [
    [0, 1,1,1,1],
    [0, 1,1,2,1],
    [0, 1,3,0,1],
    [0, 1,1,1,1],
    [0]
]
map_layout_comms = [
    [0, 1,1,1,1],
    [0, 1,3,0,1],
    [0, 1,1,2,1],
    [0, 1,1,1,1],
    [0]
]
map_layout_main.reverse()

def _check_pos(change_x, change_y):
    new_list = map_layout_main[mapY + change_y]
    return new_list[mapX + change_x]

class RandomObject():
    def __init__(self, note_to_be_used):
        self.count = 0
        self.can_col = True
        self.note = note_to_be_used
        self.this_obj = pygame.Rect(random.randint(100,700), random.randint(100,300), 250, 250)
    def update(self, m_col, is_note):
        col = self.this_obj.colliderect(m_col)
        if not col:
            self.can_col = True
        if self.can_col:
            if col:
                if is_note == 0:
                    self.count += 1
                    print("found")
                    if self.count == 2:
                        update_runner_array.clear()
                        update_runner_array.append(self)
                else:
                    print("NOOO")
                self.can_col = False
    def _get_image(self):
        return self.note

def _update_runner(object_arr):
    for i in object_arr:
        i.update(mouse_rect, object_arr.index(i))

while running:
    screen.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
    proper_pos = (mx - cx, my - cy)
    mouse_rect = pygame.Rect(mx, my, 50, 50)

    _update_runner(update_runner_array)

    if len(update_runner_array) > 1:
        mask_being_rendered = black
        mask = pygame.mask.from_surface(mask_being_rendered, 0)
    if len(update_runner_array) == 1:
        mask_being_rendered = update_runner_array[0]._get_image()
        mask = pygame.mask.from_surface(mask_being_rendered, 0)
        update_runner_array.clear()

    overlap_mask = mask.overlap_mask(mask_2, proper_pos)
    screen.blit(overlap_mask.to_surface(None, mask_being_rendered, None), (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if _check_pos(0, 0) == 2:
                    for i in range(2):
                        objects = RandomObject(note_1)
                        update_runner_array.append(objects)
            match event.key:
                case pygame.K_ESCAPE:
                    running = False
                case pygame.K_w:
                    if _check_pos(0,1) != 1:
                        mapY += 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(1,1)
                case pygame.K_s:
                    if _check_pos(0,-1) != 1:
                        mapY -= 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(0.5,0.5)
                case pygame.K_d:
                    if _check_pos(1,0) != 1:
                        mapX += 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(0,1)
                case pygame.K_a:
                    if _check_pos(-1,0) != 1:
                        mapX -= 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(1,0)
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()