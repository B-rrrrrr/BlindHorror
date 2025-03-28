import os

import pygame, random
from pygame import FULLSCREEN, Vector2
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
note_1 = pygame.transform.scale(note_1, (205 * 2 * scale_x, 246 * 2 * scale_y))
cursor = pygame.image.load("../Sprites/cursor.png").convert_alpha()
black = pygame.image.load("../Sprites/black.jpg").convert_alpha()
location_to_hit = pygame.image.load("../Sprites/location_to_hit.png").convert_alpha()
location_to_hit = pygame.transform.scale(location_to_hit, (5 * 10 * scale_x, 5 * 10 * scale_y))
location_to_hit.set_colorkey((0,0,0))
location_hit = pygame.image.load("../Sprites/location_hit.png").convert_alpha()
location_hit = pygame.transform.scale(location_hit, (5 * 10 * scale_x, 5 * 10 * scale_y))
location_hit.set_colorkey((0,0,0))
location_areas = []
loc_x = location_to_hit.get_width()/2
loc_y = location_to_hit.get_height()/2
wall_sfx = pygame.mixer.Sound("../SFX/hitwall.mp3")
walk_sfx = pygame.mixer.Sound("../SFX/walking.mp3")

object_sfx = [pygame.mixer.Sound("../SFX/temporaryshit/synth.wav"), pygame.mixer.Sound("../SFX/temporaryshit/explosion.wav"), pygame.mixer.Sound("../SFX/temporaryshit/hitHurt(1).wav"), pygame.mixer.Sound("../SFX/temporaryshit/jump.wav"), pygame.mixer.Sound("../SFX/temporaryshit/pickupCoin.wav"), pygame.mixer.Sound("../SFX/temporaryshit/pickupCoin(1).wav")]

cursor = pygame.transform.scale(cursor, (150 * scale_x, 150 * scale_y))
cx = cursor.get_width()/2
cy = cursor.get_height()/2
font = pygame.font.Font(None, 100)
running = True

mask = pygame.mask.from_surface(map, 0)
mask_2 = pygame.mask.from_surface(cursor, 0)
mask_being_rendered = map
note_position_offset = Vector2(0, 0)
finished_investigating = False

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
    [0, 3,3,3,11,5,0,2,11,1,1,1],
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
        self.currently_investigating = False
        self.mask = pygame.mask.from_surface(self.not_investigated_img, 0)
    def _show_in_pos(self, mouse_mask, properposition):
        if not self.currently_investigating:
            overlap_investigated_mask = self.mask.overlap_mask(mouse_mask, (-self.xPos + properposition[0], -self.yPos + properposition[1]))
            if not self.investigated:
                screen.blit(overlap_investigated_mask.to_surface(None, self.not_investigated_img, None), (self.xPos, self.yPos))
            else:
                screen.blit(overlap_investigated_mask.to_surface(None, self.investigated_img, None), (self.xPos, self.yPos))


for y in map_layout:
    for i, x in enumerate(y):
        if x == 11:
            obj = InvestigateArea((2 + (i * 5)) * 20 * scale_x - loc_x, (38 - (map_layout.index(y) * 5)) * 20 * scale_y - loc_y, location_to_hit, location_hit)
            location_areas.append(obj)

def _check_pos(change_x, change_y):
    if (mapY + change_y) > 0 and (mapY + change_y) < 8 and (mapX + change_x) > 0 and (mapX+change_x) < 12:
        new_list = map_layout[mapY + change_y]
        return new_list[mapX + change_x]
    return 100

class RandomObject():
    def __init__(self, note_to_be_used, object_array, sound_array):
        if object_array != 0:
            ran = random.randint(1, 5)
            self.sound = sound_array[ran]
        else:
            self.sound = sound_array[0]
        self.count = 0
        self.can_col = True
        self.note = note_to_be_used
        self.colliding_with_object = True
        print("NEW")
        while self.colliding_with_object:
            self.this_obj = pygame.Rect(random.uniform(100 * scale_x,1100 * scale_x), random.uniform(50 * scale_y,600 * scale_y), random.uniform(175, 300), random.uniform(175, 300))
            if len(object_array) > 0:
                for i in object_array:
                    self.colliding_with_object = self.this_obj.colliderect(i.this_obj)
                    print(self.colliding_with_object)
                    if self.colliding_with_object:
                        break
            else:
                self.colliding_with_object = False
    def update(self, m_col, is_note):
        col = self.this_obj.colliderect(m_col)
        if not col:
            self.can_col = True
        if self.can_col:
            if col:
                self.sound.play()
                if is_note == 0:
                    self.count += 1
                    if self.count == 2:
                        self.sound.play()
                        update_runner_array.clear()
                        update_runner_array.append(self)
                self.can_col = False
        pygame.draw.rect(screen, (255, 0, 0), self.this_obj)
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

    if len(update_runner_array) > 1:
        mask_being_rendered = black
        mask = pygame.mask.from_surface(mask_being_rendered, 0)
    if len(update_runner_array) == 1:
        mask_being_rendered = update_runner_array[0]._get_image()
        mask = pygame.mask.from_surface(mask_being_rendered, 0)
        note_position_offset = (width / 2 - mask_being_rendered.get_width() / 2, height / 2 - mask_being_rendered.get_height() / 2)
        finished_investigating = True
        update_runner_array.clear()

    overlap_mask = mask.overlap_mask(mask_2, (proper_pos[0] - note_position_offset[0], proper_pos[1] - note_position_offset[1]))
    screen.blit(overlap_mask.to_surface(None, mask_being_rendered, None), note_position_offset)

    for i in location_areas:
        i._show_in_pos(mask_2, proper_pos)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if _check_pos(0, 0) == 2 and finished_investigating:
                    mask_being_rendered = map
                    note_position_offset = (0, 0)
                    mask = pygame.mask.from_surface(mask_being_rendered, 0)
                    finished_investigating = False
                elif _check_pos(0, 0) == 2:
                    for i in range(6):
                        for i in location_areas:
                            i.currently_investigating = True
                        objects = RandomObject(note_1, update_runner_array, object_sfx)
                        update_runner_array.append(objects)
            match event.key:
                case pygame.K_ESCAPE:
                    running = False
                case pygame.K_w:
                    if _check_pos(0,1) != 0:
                        mapY += 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(1,1)
                case pygame.K_s:
                    if _check_pos(0,-1) != 0:
                        mapY -= 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(0.5,0.5)
                case pygame.K_d:
                    if _check_pos(1,0) != 0:
                        mapX += 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(0,1)
                case pygame.K_a:
                    if _check_pos(-1,0) != 0:
                        mapX -= 1
                        walk_sfx.play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(1,0)
        if event.type == pygame.QUIT:
            running = False
    _update_runner(update_runner_array)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()