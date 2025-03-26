import os

import pygame, random
from pygame import FULLSCREEN
from sympy.strategies.core import switch
from wx.propgrid import NullProperty

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
map = pygame.transform.scale(map, (64 * 20 * scale_x, 36 * 20 * scale_y))

note_1 = pygame.image.load("../Sprites/note.png").convert_alpha()
cursor = pygame.image.load("../Sprites/cursor.png").convert_alpha()
black = pygame.image.load("../Sprites/black.jpg").convert_alpha()
location_to_hit = pygame.image.load("../Sprites/location_to_hit.png").convert_alpha()
location_to_hit = pygame.transform.scale(location_to_hit, (5 * 10 * scale_x, 5 * 10 * scale_y))
location_hit = pygame.image.load("../Sprites/location_hit.png").convert_alpha()
location_hit = pygame.transform.scale(location_hit, (5 * 10 * scale_x, 5 * 10 * scale_y))
location_areas = []
loc_x = location_to_hit.get_width()/2
loc_y = location_to_hit.get_height()/2
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

mapX=6
mapY=1
map_layout = [
    [0, 11,0,0,11,6,3,3,9,9,9,11],
    [0, 11,0,0,0,0,0,0,0,0,0,0],
    [0, 3,3,3,11,7,0,0,9,9,9,11],
    [0, 11,3,3,0,0,0,0,0,0,0,0],
    [0, 11,3,3,0,0,0,0,2,1,1,1],
    [0, 3,3,3,4,4,11,0,2,1,1,1],
    [0, 3,3,3,11,5,0,0,11,1,1,1],
    [0]
]

map_layout.reverse()
class InvestigateArea():
    def __init__(self, xPos, yPos, not_investigated, investigated):
        self.xPos = xPos
        self.yPos = yPos
        self.not_investigated_img = not_investigated
        self.investigated_img = investigated
        self.investigated = False
        self.mask = pygame.mask.from_surface(self.not_investigated_img, 0)
    def _show_in_pos(self, mouse_mask, properposition):
        overlaped_mask = self.mask.overlap_mask(mouse_mask, (-self.xPos + properposition[0], -self.yPos + properposition[1]))
        screen.blit(overlaped_mask.to_surface(None, self.not_investigated_img, None),(self.xPos,self.yPos))

for y in map_layout:
    for i, x in enumerate(y):
        if x == 11:
            location_areas.append(InvestigateArea((2 + (i * 5)) * 20 * scale_x - loc_x, (38 - (map_layout.index(y) * 5)) * 20 * scale_y - loc_y, location_to_hit, location_hit))

def _check_pos(change_x, change_y):
    if (mapY + change_y) > 0 and (mapY + change_y) < 8 and (mapX + change_x) > 0 and (mapX+change_x) < 12:
        new_list = map_layout[mapY + change_y]
        return new_list[mapX + change_x]
    return 100

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
    for i in location_areas:
        i._show_in_pos(mask, proper_pos)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if _check_pos(0, 0) == 2:
                    for i in range(2):
                        objects = RandomObject(note_1)
                        update_runner_array.append(objects)
            match event.key:
                case pygame.K_SPACE:
                    print(mx, my)
                case pygame.K_ESCAPE:
                    running = False
                case pygame.K_w:
                    if _check_pos(0,1) == 0:
                        mapY += 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(1,1)
                case pygame.K_s:
                    if _check_pos(0,-1) == 0:
                        mapY -= 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(0.5,0.5)
                case pygame.K_d:
                    if _check_pos(1,0) == 0:
                        mapX += 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(0,1)
                case pygame.K_a:
                    if _check_pos(-1,0) == 0:
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