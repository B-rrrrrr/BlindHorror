import os
import socket

import pygame
import random
from pygame import Vector2

pygame.init()
pygame.mixer.init()

os.environ["SDL_VIDEO_CENTERED"] = "1"
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
scale_x = screen.get_width() / 1280
scale_y = screen.get_height() / 720

slider_body = pygame.image.load("../Sprites/slider.png").convert_alpha()
slider_knob = pygame.image.load("../Sprites/slider_knob.png").convert_alpha()
speaker_symbol = pygame.image.load("../Sprites/speaker_symbol.png").convert_alpha()
speaker_symbol = pygame.transform.scale(speaker_symbol, (50 * 2 * scale_x, 50 * 2 * scale_y))
start_button = pygame.image.load("../Sprites/start_button.png").convert_alpha()
quit_button = pygame.image.load("../Sprites/quit_button.png").convert_alpha()
start_button = pygame.transform.scale(start_button, (200 * 2 * scale_x, 100 * 2 * scale_y))
quit_button = pygame.transform.scale(quit_button, (200 * 2 * scale_x, 100 * 2 * scale_y))
title = pygame.image.load("../Sprites/title.png").convert_alpha()
title = pygame.transform.scale(title, (200 * 3 * scale_x, 100 * 3 * scale_y))
intro_page = pygame.image.load("../Sprites/intropaper.png").convert_alpha()
intro_page = pygame.transform.scale(intro_page, (intro_page.get_width() * scale_x, intro_page.get_height() * scale_y))
black = pygame.image.load("../Sprites/black.png").convert_alpha()

location_to_hit = pygame.image.load("../Sprites/location_to_hit.png").convert_alpha()
location_to_hit = pygame.transform.scale(location_to_hit, (5 * 10 * scale_x, 5 * 10 * scale_y))
location_to_hit.set_colorkey((0,0,0))
location_hit = pygame.image.load("../Sprites/location_hit.png").convert_alpha()
location_hit = pygame.transform.scale(location_hit, (5 * 10 * scale_x, 5 * 10 * scale_y))
location_hit.set_colorkey((0,0,0))
location_areas = []
loc_x = location_to_hit.get_width()/2
loc_y = location_to_hit.get_height()/2

wall_sfx = pygame.mixer.Sound("../SFX/walls_sfx/00_main_area_wall.mp3")
walk_sfx = pygame.mixer.Sound("../SFX/walking_sfx/00_walking_normal.mp3")
locked_door_sfx = pygame.mixer.Sound("../SFX/Doors/locked_sfx/00_main_area_door_locked.mp3")
open_door_sfx = pygame.mixer.Sound("../SFX/Doors/open_sfx/00_main_area_door_open.mp3")
picture = pygame.mixer.Sound("../SFX/picture_take.mp3")
silence = pygame.mixer.Sound("../SFX/silence.mp3")
map_rustling = pygame.mixer.Sound("../SFX/map_rustling.mp3")
man_getting_killed = pygame.mixer.Sound("../SFX/guy_is_murdered.mp3")
elevator_flicker = pygame.mixer.Sound("../SFX/Background SFX/elevator_flickering.mp3")
dying_man = pygame.mixer.Sound("../SFX/Background SFX/staff_area_dying_man.mp3")
comms_log = pygame.mixer.Sound("../SFX/Background SFX/comms_voice_message.mp3")
fountain = pygame.mixer.Sound("../SFX/Background SFX/garden_fountain.mp3")
door_broken = pygame.mixer.Sound("../SFX/extra scary sfx/janitor_door_breaks.mp3")
fell_down = False
picture_taken = False
break_glass = False
lost_map = False
comms_log_not_heard = True
man_can_be_murdered = False
locked_door = False
open_door = False
man_not_murdered = True
volume = 1
volume_level = 1
left_channel = pygame.mixer.Channel(0)
background_channel = pygame.mixer.Channel(1)
break_in_not_happen = True
door_broke = False
break_in_channel = pygame.mixer.Channel(5)

monster_mono = pygame.mixer.Sound("../SFX/final_sequence_mono_monster.mp3")
monster_stereo = pygame.mixer.Sound("../SFX/final_sequence_stereo_monster.mp3")
jumpscare_time = False
jumpscare_can_commence = False
jump_1 = pygame.image.load("../Sprites/jumpscare_1.png").convert_alpha()
jump_1 = pygame.transform.scale(jump_1, (1280 * scale_x, 36 * 20 * scale_y))
jump_2 = pygame.image.load("../Sprites/jumpscare_2.png").convert_alpha()
jump_2 = pygame.transform.scale(jump_2, (1280 * scale_x, 36 * 20 * scale_y))
jump_3 = pygame.image.load("../Sprites/jumpscare_3.png").convert_alpha()
jump_3 = pygame.transform.scale(jump_3, (1280 * scale_x, 36 * 20 * scale_y))
jump_4 = pygame.image.load("../Sprites/jumpscare_4.png").convert_alpha()
jump_4 = pygame.transform.scale(jump_4, (1280 * scale_x, 36 * 20 * scale_y))

pygame.mouse.set_visible(False)
cursor = pygame.image.load("../Sprites/cursor.png").convert_alpha()
cursor = pygame.transform.scale(cursor, (150 * scale_x, 150 * scale_y))
cx = cursor.get_width()/2
cy = cursor.get_height()/2
font = pygame.font.Font(None, 100)
text = font.render(socket.gethostname(), True, (0,0,0), (205,205,205)).convert_alpha()
text_rect = text.get_rect()
running = True

currently_investigation = False
END_MUSIC = pygame.USEREVENT + 1
PICTURE_TAKEN = pygame.USEREVENT + 2
menu_mask_array = [start_button, quit_button, title]
menu_pos_array = [(0 * scale_x, 200 * scale_y), (700 * scale_x, 500 * scale_y), (500 * scale_x, 50 * scale_y), (width/2, height / 2)]
note_position_offset = Vector2(0, 0)
finished_investigating = False
currently_investigating = False

update_runner_array = []

map = pygame.image.load("../Sprites/map.png").convert_alpha()
map = pygame.transform.scale(map, (64 * 20 * scale_x, 36 * 20 * scale_y))
mask_being_rendered = map
mask = pygame.mask.from_surface(map, 0)
mask_2 = pygame.mask.from_surface(cursor, 0)
mapX = 10
mapY = 5
current_layer = 9
future_position = [0, 0]
map_layout = [
    [0, 16,26,26,26,26,26,26,26,26,26,26,26,26],
    [0, 4,4,26,26,26,26,26,26,26,26,26,26,26],
    [0, 4,4,30,5,5,15,6,2,2,20,21,22,19],
    [0, 4,4,30,5,5,5,5,0,0,10,27,27,27],
    [0, 26,26,3,3,3,17,8,0,0,9,9,9,18],
    [0, 26,26,13,3,3,0,0,0,0,0,0,0,0],
    [0, 26,26,13,3,3,0,0,0,0,12,25,25,1],
    [0, 26,26,3,3,3,2,2,2,11,2,25,1,1],
    [0, 26,26,3,3,3,14,4,0,0,2,1,1,1],
    [0]
]
door_layout = [
    [0, 0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0, 0,0,0,1,1,0,0,0,0,0,0,0,0],
    [0, 0,0,0,1,1,0,0,0,0,0,0,0,0,0],
    [0, 0,0,70,70,0,0,60,0,0,100,100,100,110,0],
    [0, 0,0,70,70,1000,30,1000,1000,1000,1000,100,100,110,0],
    [0, 0,0,0,0,30,30,80,0,0,90,0,0,0,0],
    [0, 0,0,0,0,30,30,0,0,0,0,0,0,10,0],
    [0, 0,0,0,0,30,30,0,0,0,0,0,0,10,0],
    [0, 0,0,0,0,40,40,50,0,0,0,0,0,0,0],
    [0, 0,0,0,0,0,0,50,0,0,20,20,0,0,0],
    [0, 0,0,0,0,0,0,0,1,0,0,0,0,0,0]
]
floor_layout = [
    [0, 9,26,26,26,26,26,26,26,26,26,26,26,26],
    [0, 9,9,26,26,26,26,26,26,26,26,26,26,26],
    [0, 9,7,7,0,0,6,6,2,2,12,12,12,13],
    [0, 8,7,7,0,0,0,0,0,0,0,0,0,0],
    [0, 26,26,3,3,3,10,10,0,0,11,11,11,11],
    [0, 26,26,3,3,3,0,0,0,0,0,0,0,0],
    [0, 26,26,3,3,3,0,0,0,0,2,1,1,1],
    [0, 26,26,3,3,3,4,4,4,0,2,1,1,1],
    [0, 26,26,3,3,3,5,5,0,0,2,1,1,1],
    [0]
]

object_sfx = []
final_invest_sfx = []
final_invest_sprites = []
walk_sfx_array = []
wall_sfx_array = []
door_open_array = []
door_locked_array = []
scary_sfx_array = []
ambience_array = []
investigation_arrays = [
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    []
]

for i in os.scandir("../Sprites/Investigation"):
    final_invest_sprites.append(os.path.basename(i))
for i in os.scandir("../SFX/walking_sfx"):
    walk_sfx_array.append(os.path.basename(i))
for i in os.scandir("../SFX/walls_sfx"):
    wall_sfx_array.append(os.path.basename(i))
for i in os.scandir("../SFX/Doors/open_sfx"):
    door_open_array.append(os.path.basename(i))
for i in os.scandir("../SFX/Doors/locked_sfx"):
    door_locked_array.append(os.path.basename(i))
for i in os.scandir("../SFX/final_invests"):
    final_invest_sfx.append(os.path.basename(i))
for i in os.scandir("../SFX/scary_sfx"):
    sound = "../SFX/scary_sfx/" + os.path.basename(i)
    scary_sfx_array.append(pygame.mixer.Sound(sound))
for i in os.scandir("../SFX/Ambience"):
    ambience_array.append("../SFX/Ambience/" + os.path.basename(i))
for i in os.scandir("../SFX/Investigation_SFX"):
    sound = "../SFX/Investigation_SFX/" + os.path.basename(i) + "/"
    match os.path.basename(i):
        case "00_reception":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[0].append(pygame.mixer.Sound(new_sound))
        case "01_kitchen":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[1].append(pygame.mixer.Sound(new_sound))
        case "02_fountain":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[2].append(pygame.mixer.Sound(new_sound))
        case "03_staff_room":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[3].append(pygame.mixer.Sound(new_sound))
        case "04_comms_room":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[4].append(pygame.mixer.Sound(new_sound))
        case "05_operation_room":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[5].append(pygame.mixer.Sound(new_sound))
        case "06_nothingness_room":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[6].append(pygame.mixer.Sound(new_sound))
        case "07-08-09_room":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[7].append(pygame.mixer.Sound(new_sound))
        case "10_final_room":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[8].append(pygame.mixer.Sound(new_sound))

map_layout.reverse()
door_layout.reverse()
floor_layout.reverse()
final_invest_sprites.sort()
walk_sfx_array.sort()
wall_sfx_array.sort()
door_open_array.sort()
door_locked_array.sort()
final_invest_sfx.sort()
ambience_array.sort()

for i in final_invest_sprites:
    invest_sprite = pygame.image.load("../Sprites/Investigation/" + i).convert_alpha()
    #invest_sprite = pygame.transform.scale(invest_sprite, (invest_sprite.get_width() * 2 * scale_x, invest_sprite.get_height() * 2 * scale_y))
    pos = final_invest_sprites.index(i)
    final_invest_sprites.remove(i)
    final_invest_sprites.insert(pos, invest_sprite)
for i in walk_sfx_array:
    sound = "../SFX/walking_sfx/" + i
    pos = walk_sfx_array.index(i)
    walk_sfx_array.remove(i)
    walk_sfx_array.insert(pos, pygame.mixer.Sound(sound))
for i in wall_sfx_array:
    sound = "../SFX/walls_sfx/" + i
    pos = wall_sfx_array.index(i)
    wall_sfx_array.remove(i)
    wall_sfx_array.insert(pos, pygame.mixer.Sound(sound))
for i in door_open_array:
    sound = "../SFX/Doors/open_sfx/" + i
    pos = door_open_array.index(i)
    door_open_array.remove(i)
    door_open_array.insert(pos, pygame.mixer.Sound(sound))
for i in door_locked_array:
    sound = "../SFX/Doors/locked_sfx/" + i
    pos = door_locked_array.index(i)
    door_locked_array.remove(i)
    door_locked_array.insert(pos, pygame.mixer.Sound(sound))
for i in final_invest_sfx:
    sound = "../SFX/final_invests/" + i
    pos = final_invest_sfx.index(i)
    final_invest_sfx.remove(i)
    final_invest_sfx.insert(pos, pygame.mixer.Sound(sound))

menu = True
tutorial = False
click = False
def _menu(mask_array, pos_array, mouse_mask, proper_pos, is_clicked):
    for i in mask_array:
        mask = pygame.mask.from_surface(i, 0)
        position = pos_array[mask_array.index(i)]
        button_rect = pygame.Rect(position[0], position[1], i.get_width(), i.get_height())
        overlapping_mask = mask.overlap_mask(mouse_mask, (proper_pos[0] - position[0], proper_pos[1] - position[1]))
        screen.blit(overlapping_mask.to_surface(None, i, None), position)
        if button_rect.collidepoint(proper_pos[0], proper_pos[1]) and is_clicked:
            return mask_array.index(i)
def _tutorial(mask_array, pos_array, mouse_mask, proper_pos, is_clicked):
    for i in mask_array:
        mask = pygame.mask.from_surface(i, 0)
        position = pos_array[mask_array.index(i)]
        button_rect = pygame.Rect(position[0], position[1], i.get_width(), i.get_height())
        overlapping_mask = mask.overlap_mask(mouse_mask, (proper_pos[0] - position[0], proper_pos[1] - position[1]))
        screen.blit(overlapping_mask.to_surface(None, i, None), position)
        if button_rect.collidepoint(proper_pos[0], proper_pos[1]) and is_clicked:
            return mask_array.index(i)
class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int, slider_body, slider_knob,
                 speaker) -> None:
        self.pos = pos
        self.size = size

        self.speaker = speaker
        self.speaker_mask = pygame.mask.from_surface(self.speaker, 0)
        self.slider_body = slider_body
        self.slider_body_mask = pygame.mask.from_surface(self.slider_body, 0)
        self.slider_knob = slider_knob
        self.slider_knob_mask = pygame.mask.from_surface(self.slider_knob, 0)
        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val  # <- percentage

        self.offset = self.initial_val - 5
        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10,
                                       self.size[1])
        self.speaker_pos = (self.slider_left_pos - 200, self.slider_top_pos - 25)
        self.slider_body_pos = (self.slider_left_pos, self.slider_top_pos)
        self.slider_knob_pos = (self.slider_left_pos + self.offset, self.slider_top_pos + 20)

    def move_slider(self, mouse_pos):
        pos = mouse_pos[0]
        if pos < self.slider_left_pos:
            pos = self.slider_left_pos
        if pos > self.slider_right_pos:
            pos = self.slider_right_pos
        self.offset = pos - 350
        self.slider_knob_pos = (self.slider_left_pos + self.offset, self.slider_top_pos + 20)

    def render(self, app, mouse_mask, proper_pos):
        overlapping_mask_speaker = self.speaker_mask.overlap_mask(mouse_mask, (
        proper_pos[0] - self.speaker_pos[0], proper_pos[1] - self.speaker_pos[1]))
        screen.blit(overlapping_mask_speaker.to_surface(None, self.speaker, None), self.speaker_pos)
        overlapping_mask_slider_body = self.slider_body_mask.overlap_mask(mouse_mask, (
        proper_pos[0] - self.slider_body_pos[0], proper_pos[1] - self.slider_body_pos[1]))
        screen.blit(overlapping_mask_slider_body.to_surface(None, self.slider_body, None), self.slider_body_pos)
        overlapping_mask_slider_knob = self.slider_knob_mask.overlap_mask(mouse_mask, (
            proper_pos[0] - self.slider_knob_pos[0], proper_pos[1] - self.slider_knob_pos[1]))
        screen.blit(overlapping_mask_slider_knob.to_surface(None, self.slider_knob, None), self.slider_knob_pos)

    def get_value(self):
        value = self.slider_knob_pos[0] * scale_x / self.button_rect.centerx - 0.9
        if value < 0.1:
            value = 0
        elif value > 0.85:
            value = 0.9
        return value
slider = Slider((285 * scale_x,600 * scale_y), (150 * scale_x,200 * scale_y), 0.5, 0, 100, slider_body, slider_knob, speaker_symbol)

name = "nothing"

class InvestigateArea():
    def __init__(self, xPos, yPos, not_investigated, investigated, num):
        self.which_am_i = num
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
    def _have_i_been_investigated(self):
        if self.investigated:
            return True
        return False
class RandomObject():
    def __init__(self, note_to_be_used, object_array, sound_array, which_invest, final_invest_sfx):
        if len(object_array) == 0:
            self.sound = final_invest_sfx[which_invest - 11]
        else:
            self.sound = sound_array[len(object_array) - 1]
        self.count = 0
        self.can_col = True
        self.note = note_to_be_used[which_invest - 11]
        self.colliding_with_object = True
        while self.colliding_with_object:
            self.this_obj = pygame.Rect(random.uniform(100 * scale_x,1100 * scale_x), random.uniform(50 * scale_y,600 * scale_y), random.uniform(175, 300), random.uniform(175, 300))
            if len(object_array) > 0:
                for i in object_array:
                    self.colliding_with_object = self.this_obj.colliderect(i.this_obj)
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
                self.sound.set_volume(volume_level)
                if is_note == 0:
                    self.count += 1
                    if self.count == 2:
                        self.sound.play()
                        self.sound.set_volume(volume_level)
                        update_runner_array.clear()
                        update_runner_array.append(self)
                self.can_col = False
        #pygame.draw.rect(screen, (255, 0, 0), self.this_obj)
    def _get_image(self):
        return self.note
def _update_runner(object_arr):
    for i in object_arr:
        i.update(mouse_rect, object_arr.index(i))
def _check_investigate_area(current_num, investigate_num):
    question = current_num
    answer = investigate_num
    if investigate_num > current_num:
        question = investigate_num
        answer = current_num
    match question:
        case 11:
            if answer == 0:
                return True
        case 12:
            if answer == 2:
                return True
        case 13:
            if answer == 1:
                return True
        case 14:
            if answer == 3:
                return True
        case 15:
            if answer == 3:
                return True
        case 16:
            if answer == 3:
                return True
        case 17:
            if answer == 3:
                return True
        case 18:
            if answer == 9:
                return  True
    return False
def _finished_investigating(current_num, map_layout, this_thing, door_layout):
    #verändert Nummern in map_layout, sodass Orte ereichbar werden
    match this_thing.which_am_i:
        case 11:
            #00_reception
            pass
        case 12:
            for y in map_layout:
                for i, x in enumerate(y):
                    if y[i] == 3:
                        y[i] = 1
                    elif y[i] == 4:
                        y[i] = 3
            for y in door_layout:
                for i, x in enumerate(y):
                    if y[i] == 1:
                        y[i] = 0
                    elif y[i] == 2:
                        y[i] = 1
        case 13:
            #02_fountain
            pass
        case 14:
            for y in map_layout:
                for i, x in enumerate(y):
                    if y[i] == 5:
                        y[i] = 2
                    elif x == 6:
                        y[i] = 3
                for y in door_layout:
                    for i, x in enumerate(y):
                        if y[i] == 1:
                            y[i] = 0
                        elif y[i] == 3:
                            y[i] = 1
        case 15:
            for y in map_layout:
                for i, x in enumerate(y):
                    if y[i] == 7:
                        y[i] = 3
                for y in door_layout:
                    for i, x in enumerate(y):
                        if y[i] == 1:
                            y[i] = 0
        case 16:
            for y in map_layout:
                for i, x in enumerate(y):
                    if y[i] == 8:
                        y[i] = 3
                for y in door_layout:
                    for i, x in enumerate(y):
                        if y[i] == 5:
                            y[i] = 0
        case 17:
            #teleported into other room
            pass
        case 18:
            # skelleton
            pass
        case 19:
            #final
            pass
        case 20:
            pass
        case 21:
            pass
        case 22:
            pass

for y in map_layout:
    for i, x in enumerate(y):
        if x > 10 and x < 20 or x == 30:
            obj = InvestigateArea((-8 + (i * 5)) * 20 * scale_x - loc_x, (38 - (map_layout.index(y) * 5)) * 20 * scale_y - loc_y, location_to_hit, location_hit, x)
            location_areas.append(obj)
    for i, x in enumerate(y):
        if y[i] == 30:
            y[i] = 7
def _wall_checker(c_layer, future_layer, door_sfx):
    if c_layer >= 20:
        match c_layer:
            case 20:
                if future_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    door_sfx.set_volume(volume_level)
                    return True
            case 21:
                if future_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    door_sfx.set_volume(volume_level)
                    return True
            case 22:
                if future_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    door_sfx.set_volume(volume_level)
                    return True
            case 25:
                if future_layer == 1:
                    return True
            case 27:
                if future_layer == 10 or future_layer >= 19 and future_layer <= 22:
                    door_sfx.play()
                    door_sfx.set_volume(volume_level)
                    return True
    elif future_layer >= 20:
        match future_layer:
            case 20:
                if c_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    door_sfx.set_volume(volume_level)
                    return True
            case 21:
                if c_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    door_sfx.set_volume(volume_level)
                    return True
            case 22:
                if c_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    door_sfx.set_volume(volume_level)
                    return True
            case 25:
                if c_layer == 1:
                    return  True
            case 27:
                if c_layer == 10 or future_layer >= 20 and future_layer <= 22:
                    return True
    return False
def _door(new_layer_num):
    return  new_layer_num
def _check_pos(change_x, change_y):
    if (mapY + change_y) > 0 and (mapY + change_y) < 10 and (mapX + change_x) > 0 and (mapX+change_x) < 14:
        new_list = map_layout[mapY + change_y]
        return new_list[mapX + change_x]
    return 100
def _check_door(x, y, num_to_check, current_pos):
    new_list = door_layout[y]
    current_pos_list = door_layout[current_pos[1]]
    door_to_check = current_pos_list[current_pos[0]]
    match new_list[x]:
        case 1:
            if door_to_check == 0:
                return True, 1
        case 30:
            if door_to_check == 0 and num_to_check == 3 or door_to_check == 1000 and num_to_check == 3:
                return True, 3
        case 60:
            if door_to_check == 1000 and num_to_check == 6:
                return True, 6
        case 70:
            if door_to_check == 1000 and num_to_check == 7:
                return True, 7
        case 80:
            if door_to_check == 1000 and num_to_check == 8:
                return True, 8
        case 90:
            if door_to_check == 1000 and num_to_check == 9:
                return True, 9
        case 1000:
            if door_to_check == 0 and num_to_check == 10 or door_to_check == 1000 and num_to_check == 10 or door_to_check == 0 and num_to_check == 5 or door_to_check == 1000 and num_to_check == 5:
                return  True, 0
    dc = door_to_check
    nc = num_to_check
    door_to_check = nc
    num_to_check = dc
    match new_list[x]:
        case 1:
            if door_to_check == 0:
                return True, 1
        case 30:
            if door_to_check == 0 and num_to_check == 3 or door_to_check == 1000 and num_to_check == 3:
                return True, 3
        case 60:
            if door_to_check == 1000 and num_to_check == 6:
                return True, 6
        case 70:
            if door_to_check == 1000 and num_to_check == 7:
                return True, 7
        case 80:
            if door_to_check == 1000 and num_to_check == 8:
                return True, 8
        case 90:
            if door_to_check == 1000 and num_to_check == 9:
                return True, 9
        case 1000:
            if door_to_check == 0 and num_to_check == 10 or door_to_check == 1000 and num_to_check == 10 or door_to_check == 0 and num_to_check == 5 or door_to_check == 1000 and num_to_check == 5:
                return True, 0
    return False

def _jumpscare(note_pos_offset, jumpscare_time, menu):
    num = pygame.mixer.music.get_pos()
    delay = int(num/100)
    #je nach wie lange Sound gespielt wird verändert sich was gezeigt wird
    if delay < 50:
        delay = 50
    if num > 26000:
        screen.blit(jump_4, note_pos_offset)
    elif num > 16000:
        screen.blit(jump_3, note_pos_offset)
    elif num > 500:
        pygame.time.delay(delay)
        screen.blit(jump_1, note_pos_offset)
        pygame.display.flip()
        pygame.time.delay(delay)
        screen.blit(jump_2, note_pos_offset)
    else:
        screen.blit(black, note_pos_offset)

class _positional_audio():
    def __init__(self, channel):
        self.fade_in = True
        self.channel = channel
    def _update(self, pos_x, pos_y, mapX, mapY, audio, can_be_played):
        change_right_ear = abs(pos_x - mapX)
        change_left_ear = abs(pos_y - mapY)
        equal = False
        if pos_x - mapX > 0:
            left = False
        elif mapX - pos_x > 0:
            left = True
        else:
            equal = True
        match change_right_ear:
            case 0:
                right_ear = 1
            case 1:
                right_ear = 0.75
            case 2:
                right_ear = 0.5
            case 3:
                right_ear = 0.25
            case _:
                right_ear = 0
        match change_left_ear:
            case 0:
                left_ear = 1
            case 1:
                left_ear = 0.75
            case 2:
                left_ear = 0.5
            case 3:
                left_ear = 0.25
            case _:
                left_ear = 0
        if left_ear == 0 or right_ear == 0:
            left_ear = 0
            right_ear = 0

        if self.channel == break_in_channel and not self.channel.get_busy():
            break_in_channel.play(audio)

        if not pygame.mixer.Channel(1).get_busy() and can_be_played:
            if self.fade_in:
                pygame.mixer.Channel(1).play(audio, 0,0, 1600)
                self.fade_in = False
            else:
                self.channel.play(audio)
        elif audio != self.channel.get_sound():
            self.channel.fadeout(1600)
            self.fade_in = True
        if not equal:
            if left_ear > right_ear and not left or left_ear < right_ear and left:
                self.channel.set_volume(right_ear * volume_level, left_ear * volume_level)
            else:
                self.channel.set_volume(left_ear * volume_level, right_ear * volume_level)
        else:
            if right_ear < left_ear:
                self.channel.set_volume(right_ear * volume_level, right_ear * volume_level)
            else:
                self.channel.set_volume(left_ear * volume_level, left_ear * volume_level)
pos_audio = _positional_audio(background_channel)
pos_audio_2 = _positional_audio(break_in_channel)
def _check_sounds(x, y, current_position, door_past, walk_sfx_array, wall_sfx_array, door_open_array, door_locked_array):
    new_list = floor_layout[y]
    door_list = door_layout[y]
    door_num = int(door_list[x]/10)
    wall_num_update = 0
    object_sfx_number = 0
    name = "nothing"
    door_lock_update = 0
    match new_list[x]:
        case 0:
            object_sfx_number = 0
            name = "main"
        case 2:
            object_sfx_number = 1
        case 3:
            object_sfx_number = 2
            name = "garden"
        case 5:
            object_sfx_number = 3
            name = "staff_area"
        case 6:
            object_sfx_number = 4
            name = "comms_log"
        case 7:
            name = "break_in"
        case 8:
            wall_num_update = 1
        case 9:
            object_sfx_number = 5
            wall_num_update = 2
        case 10:
            object_sfx_number = 6
        case 11:
            object_sfx_number = 6
        case 12:
            object_sfx_number = 7
        case 13:
            name = "final"
            object_sfx_number = 8
    if new_list[x] == 8:
        wall_num_update = 1
    elif new_list[x] >= 9:
        wall_num_update = 2
    if door_num == 100:
        future_door_list = door_layout[door_past[1]]
        door_num = int(future_door_list[door_past[0]] / 10)
    match door_num:
        case 3:
            door_lock_update = 1
        case 6:
            door_lock_update = 2
        case 7:
            door_lock_update = 3
        case 8:
            door_lock_update = 4
    if door_num == 100:
        current_door_position = door_layout[current_position[0]]
        door_num = current_door_position[current_position[1]]
        if door_num == 100:
            door_num = 0
    print(door_num)
    return walk_sfx_array[new_list[x]], wall_sfx_array[new_list[x] - wall_num_update], door_open_array[door_num], door_locked_array[door_lock_update], object_sfx_number, new_list[x] - wall_num_update, name

pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame.time.set_timer(pygame.USEREVENT + 6, 1000)
pygame.time.set_timer(pygame.USEREVENT + 4, 1000)
timer = random.randint(5,10)
timer_break_in = random.randint(5, 10)
timer_jumpscare = 2
pygame.mixer.music.set_endevent(END_MUSIC)
clock = pygame.time.Clock()

while running:
    screen.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
    proper_pos = (mx - cx, my - cy)
    mouse_rect = pygame.Rect(mx, my, 50, 50)
    #MENU FUNKTION
    while menu:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("../SFX/Music/menu_theme_begin.mp3")
            pygame.mixer.music.play()
            pygame.mixer.music.queue("../SFX/Music/menu_theme_loop.mp3", "loop", 2000)
        mouse = pygame.mouse.get_pressed()
        screen.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        proper_pos = (mx - cx, my - cy)
        mouse_rect = pygame.Rect(mx, my, 50, 50)
        match _menu(menu_mask_array, menu_pos_array, mask_2, proper_pos, click):
            case 0:
                #START Knopf oder Click auf Papier beim Intro
                if not tutorial:
                    tutorial = True
                    pygame.mixer.music.fadeout(800)
                    menu_mask_array = [intro_page, text]
                    menu_pos_array = [(intro_page.get_width()/2, 0), (intro_page.get_width()-20*scale_x, 17*scale_y)]
                    pygame.mixer.music.queue("../SFX/Music/intro_ambience.mp3")
                else:
                    menu = False
                    pygame.mixer.music.fadeout(3000)
                    pygame.mixer.music.queue(ambience_array[0])
            case 1:
                #QUIT
                if not tutorial:
                    running = False
                    menu = False
        # Tonstärke Slider
        if not tutorial:
            slider.render(screen, mask_2, proper_pos)
            if slider.container_rect.collidepoint((mx,my)) and mouse[0]:
                slider.move_slider((mx,my))
            volume_level = slider.get_value()
            pygame.mixer.music.set_volume(volume_level)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = False
        pygame.display.flip()
        clock.tick(60)

    #HAUPTSPIEL

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
    if running:
        if mask_being_rendered == map and lost_map:
            mask_being_rendered = black
            mask = pygame.mask.from_surface(mask_being_rendered, 0)
        screen.blit(overlap_mask.to_surface(None, mask_being_rendered, None), note_position_offset)

    if not lost_map:
        for i in location_areas:
            i._show_in_pos(mask_2, proper_pos)

    #Finish Investigation
    if picture_taken and not pygame.mixer.Channel(2).get_busy():
        pygame.mixer.Channel(3).play(map_rustling)
        pygame.mixer.Channel(3).set_volume(volume_level, volume_level)
        mask_being_rendered = map
        currently_investigating = False
        note_position_offset = (0, 0)
        for i in location_areas:
            i.currently_investigating = False
            if i.which_am_i == _check_pos(0, 0):
                if i.which_am_i == 12:
                    man_can_be_murdered = True
                elif i.which_am_i == 16:
                    lost_map = False
                    for a in location_areas:
                        if a.which_am_i == 30:
                            a.investigated = True
                _finished_investigating(_check_pos(0, 0), map_layout, i, door_layout)
                i.investigated = True
                if i.which_am_i == 19:
                    jumpscare_can_commence = True
        mask = pygame.mask.from_surface(mask_being_rendered, 0)
        finished_investigating = False
        picture_taken = False
    for event in pygame.event.get():
        if event.type == END_MUSIC and not pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
        #Random Scary SFX
        if event.type == pygame.USEREVENT:
            timer -= 1
            if timer < 0:
                timer = random.randint(10, 25)
                pygame.mixer.Channel(7).play(random.choice(scary_sfx_array))
                pygame.mixer.Channel(7).set_volume(random.uniform(0, 1) * volume_level, random.uniform(0, 1) * volume_level)
        #Play door break sound once
        elif (event.type == pygame.USEREVENT + 4 and not break_in_not_happen):
            timer_break_in -= 1
            if timer_break_in < 0:
                if not door_broke:
                    pygame.mixer.Channel(5).play(door_broken)
                    pygame.mixer.Channel(5).set_volume(0, 1 * volume_level)
                    door_broke = True
        #Jumpscare timing
        elif event.type == pygame.USEREVENT + 6 and jumpscare_can_commence:
            timer_jumpscare -= 1
            if timer_jumpscare < 0:
                jumpscare_time = True
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load("../SFX/extra scary sfx/final_jumpscare.mp3")
                pygame.mixer.music.play()
        if event.type == pygame.KEYDOWN:
            #Investigating moment
            if event.key == pygame.K_e:
                if _check_pos(0, 0) > 10 and finished_investigating:
                    picture_taken = True
                    currently_investigation = False
                    pygame.mixer.Channel(2).play(picture)
                    pygame.mixer.Channel(2).set_volume(1*volume_level,1* volume_level)
                elif _check_pos(0, 0) > 10:
                    #Teleport with investigation
                    if _check_pos(0, 0) == 17:
                        mapX = 13
                        mapY = 5
                        current_layer = 9
                        for i in location_areas:
                            i.currently_investigating = False
                            if i.which_am_i == 17:
                                _finished_investigating(_check_pos(0, 0), map_layout, i, door_layout)
                                i.investigated = True
                        if not currently_investigation:
                            for i in range(len(object_sfx)):
                                for i in location_areas:
                                    i.currently_investigating = True
                                    if i.which_am_i == _check_pos(0, 0) and i.investigated:
                                        currently_investigation = True
                                if not currently_investigation:
                                    currently_investigating = True
                                    objects = RandomObject(final_invest_sprites, update_runner_array, object_sfx, 17, final_invest_sfx)
                                    update_runner_array.append(objects)
                    elif _check_pos(0, 0) == 19 and not currently_investigation:
                        #Investigating Final Room
                        for i in range(len(object_sfx)):
                            for i in location_areas:
                                if i.which_am_i == _check_pos(0,0) and i.investigated:
                                    currently_investigation = True
                                i.currently_investigating = True
                            if not currently_investigation:
                                currently_investigating = True
                                objects = RandomObject(final_invest_sprites, update_runner_array, object_sfx, 21, final_invest_sfx)
                                update_runner_array.append(objects)
                    elif _check_pos(0, 0) > 19 and not currently_investigation:
                        #Investigating Living Rooms
                        for i in range(len(object_sfx)):
                            for i in location_areas:
                                i.currently_investigating = True
                                if i.which_am_i == _check_pos(0, 0) and i.investigated:
                                    currently_investigation = True
                            if not currently_investigation:
                                currently_investigating = True
                                which_note = _check_pos(0,0) - 2
                                objects = RandomObject(final_invest_sprites, update_runner_array, object_sfx, which_note, final_invest_sfx)
                                update_runner_array.append(objects)
                    else:
                        #Investigating normal rooms
                        for i in range(len(object_sfx)):
                            for i in location_areas:
                                if i.which_am_i == _check_pos(0,0) and i.investigated:
                                    currently_investigation = True
                                i.currently_investigating = True
                            if not currently_investigation:
                                currently_investigating = True
                                objects = RandomObject(final_invest_sprites, update_runner_array, object_sfx, _check_pos(0, 0), final_invest_sfx)
                                update_runner_array.append(objects)
            if running and not currently_investigating:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_w:
                        if not pygame.mixer.Channel(0).get_busy():
                            num_to_check = _check_pos(0, 1)
                            future_position = [mapX, mapY + 1]
                            change_x_y = [0,-1]
                            #moves
                            if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check, open_door_sfx):
                                current_layer = num_to_check
                                mapY += 1
                                if not pygame.mixer.Channel(0).get_busy():
                                    walk_sfx.play()
                                    walk_sfx.set_volume(volume_level)
                            #goes through door
                            elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                                current_layer = _door(num_to_check)
                                mapY += 1
                                open_door = True
                            else:
                                #if a door is in the way
                                if _check_door(mapX, mapY + 1, num_to_check, (mapX, mapY-1)):
                                    locked_door = True
                                else:
                                    #wall
                                    wall_sfx.play()
                                left_channel.set_volume(1 * volume_level, 1 * volume_level)
                    case pygame.K_s:
                        if not pygame.mixer.Channel(0).get_busy():
                            num_to_check = _check_pos(0, -1)
                            future_position = [mapX, mapY - 1]
                            change_x_y = [0, 1]
                            # moves
                            if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check, open_door_sfx):
                                current_layer = num_to_check
                                mapY -= 1
                                if not pygame.mixer.Channel(0).get_busy():
                                    walk_sfx.play()
                                    walk_sfx.set_volume(volume_level)
                            # goes through door
                            elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                                current_layer = _door(num_to_check)
                                mapY -= 1
                                open_door = True
                            else:
                                # if a door is in the way
                                if _check_door(mapX, mapY - 1, num_to_check, (mapX, mapY+1)):
                                    locked_door = True
                                else:
                                    # wall
                                    wall_sfx.play()
                                left_channel.set_volume(0.5 * volume_level,0.5 * volume_level)
                    case pygame.K_d:
                        if not pygame.mixer.Channel(0).get_busy():
                            num_to_check = _check_pos(1, 0)
                            change_x_y = [-1, 0]
                            future_position = [mapX + 1, mapY]
                            # moves
                            if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check, open_door_sfx):
                                current_layer = num_to_check
                                mapX += 1
                                if not pygame.mixer.Channel(0).get_busy():
                                    walk_sfx.play()
                                    walk_sfx.set_volume(volume_level)
                            # goes through door
                            elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                                current_layer = _door(num_to_check)
                                mapX += 1
                                open_door = True
                            else:
                                # if a door is in the way
                                if _check_door(mapX + 1, mapY, num_to_check, (mapX-1, mapY)):
                                    locked_door = True
                                else:
                                    # wall
                                    wall_sfx.play()
                                left_channel.set_volume(0,1 * volume_level)
                    case pygame.K_a:
                        if not pygame.mixer.Channel(0).get_busy():
                            num_to_check = _check_pos(-1, 0)
                            future_position = [mapX - 1, mapY]
                            change_x_y = [1, 0]
                            # moves
                            if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check, open_door_sfx):
                                current_layer = num_to_check
                                mapX -= 1
                                if not pygame.mixer.Channel(0).get_busy():
                                    walk_sfx.play()
                                    walk_sfx.set_volume(volume_level)
                            # goes through door
                            elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                                current_layer = _door(num_to_check)
                                mapX -= 1
                                open_door = True
                            else:
                                # if a door is in the way
                                if _check_door(mapX - 1, mapY, num_to_check, (mapX+1, mapY)):
                                    locked_door = True
                                else:
                                    # wall
                                    wall_sfx.play()
                                left_channel.set_volume(1*volume_level,0)
                before_volume = volume
                # checks which sound to play based on position
                le_sfx = _check_sounds(mapX, mapY, (mapX, mapY), future_position, walk_sfx_array, wall_sfx_array, door_open_array, door_locked_array)
                new_list = floor_layout[mapY]
                if new_list[mapX] == 7 and not fell_down:
                    open_door_sfx.play()
                    walk_sfx = pygame.mixer.Sound("../SFX/falling_down_stairs.mp3")
                    fell_down = True
                    lost_map = True
                    current_layer = num_to_check
                    mapX -= 1
                    walk_sfx.stop()
                    walk_sfx.play()
                elif new_list[mapX] == 9 and not break_glass:
                    walk_sfx = pygame.mixer.Sound("../SFX/break_glass.mp3")
                    break_glass = True
                else:
                    walk_sfx = pygame.mixer.Sound(le_sfx[0])
                if current_layer == 16:
                    for i in range(len(object_sfx)):
                        for i in location_areas:
                            if i.which_am_i == _check_pos(0, 0) and i.investigated:
                                currently_investigation = True
                            i.currently_investigating = True
                        if not currently_investigation:
                            currently_investigating = True
                            objects = RandomObject(final_invest_sprites, update_runner_array,
                                                   object_sfx, _check_pos(0, 0), final_invest_sfx)
                            update_runner_array.append(objects)
                wall_sfx = pygame.mixer.Sound(le_sfx[1])
                open_door_sfx = pygame.mixer.Sound(le_sfx[2])
                locked_door_sfx = pygame.mixer.Sound(le_sfx[3])
                if locked_door:
                    locked_door_sfx.play()
                    locked_door_sfx.set_volume(volume_level)
                    locked_door = False
                elif open_door:
                    open_door_sfx.play()
                    open_door_sfx.set_volume(volume_level)
                    open_door = False
                object_sfx = investigation_arrays[le_sfx[4]]
                volume = le_sfx[5] + 1
                name = le_sfx[6]
                #volume setting
                pygame.mixer.music.set_volume(volume * volume_level)
                if before_volume != volume:
                    pygame.mixer.music.fadeout(1600)
                    pygame.mixer.music.queue(ambience_array[le_sfx[5]])
                if le_sfx[4] == 2:
                    garden_time = True
                else:
                    garden_time = False
                if currently_investigation:
                    for i in location_areas:
                        i.currently_investigating = False
                    currently_investigation = False
        if event.type ==pygame.QUIT:
            running = False
    match name:
        #positional audio
        case "main":
            if mapY < 5 or mapY > 5 and mapX == 8 or mapY > 5 and mapX == 9:
                distance = [8-mapX, 9-mapX]
                if distance[0] < distance[1]:
                    pos_audio._update(8, 7, mapX, mapY,elevator_flicker, True)
                else:
                    pos_audio._update(9, 7, mapX, mapY, elevator_flicker, True)
                if man_can_be_murdered:
                     pos_audio_2._update(8, 2, mapX, mapY, man_getting_killed, man_can_be_murdered)
                     man_can_be_murdered = False
        case "garden":
            man_not_murdered = False
            distance = [3 - mapY, 4 - mapY]
            if distance[0] < distance[1]:
                pos_audio._update(3,3, mapX, mapY, fountain, True)
            else:
                pos_audio._update(3, 4, mapX, mapY, fountain, True)
        case "staff_area":
            pos_audio._update(6,1, mapX, mapY, dying_man, True)
        case "comms_log":
            if comms_log_not_heard:
                pos_audio_2._update(6, 7, mapX, mapY, comms_log, comms_log_not_heard)
                comms_log_not_heard = False
        case "break_in":
            if break_in_not_happen:
                break_in_not_happen = False
        case "final":
            if currently_investigating:
                pos_audio._update(mapX, mapY, mapX, mapY, monster_mono, True)
            else:
                pos_audio._update(mapX, mapY, mapX, mapY, monster_stereo, True)
        case "nothing":
            pos_audio._update(10000,10000, 0, 0, silence, True)
            pos_audio_2._update(10000, 10000, 0, 0, silence, True)
    _update_runner(update_runner_array)

    while jumpscare_time:
        #jumpscare effect
        _jumpscare(note_position_offset, jumpscare_time, menu)
        if pygame.mixer.music.get_pos() > 33000:
            tutorial = False
            menu_mask_array = [start_button, quit_button, title]
            menu_pos_array = [(0 * scale_x, 200 * scale_y), (700 * scale_x, 500 * scale_y), (500 * scale_x, 50 * scale_y), (width / 2, height / 2)]
            menu = True
            jumpscare_time = False
        else:
            pygame.mixer.stop()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    jumpscare_time = False
        pygame.display.flip()
        clock.tick(60)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()