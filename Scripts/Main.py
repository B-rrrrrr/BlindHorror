import os
import socket

import pygame
import random
from pygame import Vector2

pygame.init()
pygame.mixer.init()

left_channel = pygame.mixer.Channel(0)
background_channel = pygame.mixer.Channel(1)
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

comms_log_heard = False
elevator_flicker = pygame.mixer.Sound("../SFX/Background SFX/elevator_flickering.mp3")
dying_man = pygame.mixer.Sound("../SFX/Background SFX/staff_area_dying_man.mp3")
comms_log = pygame.mixer.Sound("../SFX/Background SFX/comms_voice_message.mp3")
fountain = pygame.mixer.Sound("../SFX/Background SFX/garden_fountain.mp3")
slider_body = pygame.image.load("../Sprites/slider.png").convert_alpha()
#slider_body = pygame.transform.scale(slider_body, (200 * 2 * scale_x, 100 * 2 * scale_y))
slider_knob = pygame.image.load("../Sprites/slider_knob.png").convert_alpha()
#slider_knob = pygame.transform.scale(slider_knob, (200 * 2 * scale_x, 100 * 2 * scale_y))
speaker_symbol = pygame.image.load("../Sprites/speaker_symbol.png").convert_alpha()
speaker_symbol = pygame.transform.scale(speaker_symbol, (50 * 2 * scale_x, 50 * 2 * scale_y))
start_button = pygame.image.load("../Sprites/start_button.png").convert_alpha()
quit_button = pygame.image.load("../Sprites/quit_button.png").convert_alpha()
start_button = pygame.transform.scale(start_button, (200 * 2 * scale_x, 100 * 2 * scale_y))
quit_button = pygame.transform.scale(quit_button, (200 * 2 * scale_x, 100 * 2 * scale_y))
title = pygame.image.load("../Sprites/title.png").convert_alpha()
title = pygame.transform.scale(title, (200 * 3 * scale_x, 100 * 3 * scale_y))
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
wall_sfx = pygame.mixer.Sound("../SFX/walls_sfx/00_main_area_wall.mp3")
walk_sfx = pygame.mixer.Sound("../SFX/walking_sfx/00_walking_normal.mp3")
locked_door_sfx = pygame.mixer.Sound("../SFX/Doors/locked_sfx/00_main_area_door_locked.mp3")
open_door_sfx = pygame.mixer.Sound("../SFX/Doors/open_sfx/00_main_area_door_open.mp3")
print("Hello, " +socket.gethostname() + ". Thank you for your interest.")
object_sfx = []
final_invest_sfx = []
cursor = pygame.transform.scale(cursor, (150 * scale_x, 150 * scale_y))
cx = cursor.get_width()/2
cy = cursor.get_height()/2
font = pygame.font.Font(None, 100)
running = True

END_MUSIC = pygame.USEREVENT + 1
mask = pygame.mask.from_surface(map, 0)
mask_2 = pygame.mask.from_surface(cursor, 0)
menu_mask_array = [start_button, quit_button, title]
menu_pos_array = [(0 * scale_x, 200 * scale_y), (700 * scale_x, 500 * scale_y), (500 * scale_x, 50 * scale_y)]
mask_being_rendered = map
note_position_offset = Vector2(0, 0)
finished_investigating = False

update_runner_array = []

mapX=8
mapY=1
current_layer =0
map_layout = [
    [0, 16,26,26,26,26,26,26,26,26,26,26,26,26],
    [0, 4,4,26,26,26,26,26,26,26,26,26,26,26],
    [0, 4,4,7,5,5,15,6,2,2,20,21,22,19],
    [0, 4,4,7,5,5,5,5,0,0,10,27,27,27],
    [0, 26,26,3,3,3,17,8,0,0,9,9,9,18],
    [0, 26,26,13,3,3,0,0,0,0,0,0,0,0],
    [0, 26,26,13,3,3,0,0,0,0,12,25,25,1],
    [0, 26,26,3,3,3,2,2,2,11,2,25,1,1],
    [0, 26,26,3,3,3,14,4,0,0,2,1,1,1],
    [0]
]
door_layout = [
    [0, 0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0, 0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0, 0,0,0,1,1,0,0,0,0,0,0,0,0,0],
    [0, 0,0,70,70,0,0,60,0,0,100,100,100,110,0],
    [0, 0,0,70,70,30,30,0,0,0,90,100,100,110,0],
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
fell_down = False
break_glass = False
volume = 1
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
#PROBLEM WITH INVESTIGATION WITH SOMETIMES SKIPPING OVER THINGS IVE DONE IDK LOL
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
        case "08_final_room":
            for a in os.scandir(i):
                new_sound = sound + os.path.basename(a)
                investigation_arrays[8].append(pygame.mixer.Sound(new_sound))
map_layout.reverse()
door_layout.reverse()
floor_layout.reverse()
walk_sfx_array.sort()
wall_sfx_array.sort()
door_open_array.sort()
door_locked_array.sort()
final_invest_sfx.sort()
ambience_array.sort()
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


for y in map_layout:
    for i, x in enumerate(y):
        if x > 10 and x < 20:
            obj = InvestigateArea((-8 + (i * 5)) * 20 * scale_x - loc_x, (38 - (map_layout.index(y) * 5)) * 20 * scale_y - loc_y, location_to_hit, location_hit, x)
            location_areas.append(obj)

def _check_pos(change_x, change_y):
    if (mapY + change_y) > 0 and (mapY + change_y) < 10 and (mapX + change_x) > 0 and (mapX+change_x) < 14:
        new_list = map_layout[mapY + change_y]
        return new_list[mapX + change_x]
    return 100

def _check_door(x, y):
    new_list = door_layout[y]
    if new_list[x] == 1 or new_list[x] == 2 or new_list[x] == 9:
        return True
    return False
name = "nothing"
class _positional_audio():
    def __init__(self):
        print("cool")
    def _update(self, pos_x, pos_y, mapX, mapY, audio):
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

        if not pygame.mixer.Channel(1).get_busy():
            pygame.mixer.Channel(1).play(audio)
        elif audio != pygame.mixer.Channel(1).get_sound():
            pygame.mixer.Channel(1).fadeout(1600)
        if not equal:
            if left_ear > right_ear and not left or left_ear < right_ear and left:
                background_channel.set_volume(right_ear, left_ear)
            else:
                background_channel.set_volume(left_ear, right_ear)
        else:
            if right_ear < left_ear:
                background_channel.set_volume(right_ear, right_ear)
            else:
                background_channel.set_volume(left_ear, left_ear)
pos_audio = _positional_audio()
def _check_sounds(x, y, future_pos, walk_sfx_array, wall_sfx_array, door_open_array, door_locked_array):
    new_list = floor_layout[y]
    door_list = door_layout[y]
    door_num = int(door_list[x]/10)
    wall_num_update = 0
    door_lock_update = 0
    object_sfx_number = 0
    name = "nothing"
    match future_pos:
        case 3:
            door_lock_update = 1
        case 6:
            door_lock_update = 2
        case 7:
            door_lock_update = 3
        case 10:
            door_lock_update = 4
    match new_list[x]:
        case 0:
            name = "main"
        case 2:
            object_sfx_number = 1
        case 3:
            name = "garden"
        case 5:
            name = "staff_area"
        case 6:
            name = "comms_log"
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
            object_sfx_number = 8
    if new_list[x] == 8:
        wall_num_update = 1
    elif new_list[x] >= 9:
        wall_num_update = 2
    print(new_list[x])
    return walk_sfx_array[new_list[x]], wall_sfx_array[new_list[x] - wall_num_update], door_open_array[door_num], door_locked_array[door_lock_update], object_sfx_number, new_list[x] - wall_num_update, name

class RandomObject():
    def __init__(self, note_to_be_used, object_array, sound_array, which_invest, final_invest_sfx):
        if len(object_array) == 0:
            self.sound = final_invest_sfx[which_invest - 11]
        else:
            self.sound = sound_array[len(object_array) - 1]
        self.count = 0
        self.can_col = True
        self.note = note_to_be_used
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
                if is_note == 0:
                    self.count += 1
                    if self.count == 2:
                        self.sound.play()
                        update_runner_array.clear()
                        update_runner_array.append(self)
                self.can_col = False
        #pygame.draw.rect(screen, (255, 0, 0), self.this_obj)
    def _get_image(self):
        return self.note

def _update_runner(object_arr):
    for i in object_arr:
        i.update(mouse_rect, object_arr.index(i))

def _door(new_layer_num):
    #check which area
    return  new_layer_num

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
def _wall_checker(c_layer, future_layer, door_sfx):
    if c_layer >= 20:
        match c_layer:
            case 20:
                if future_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    return True
            case 21:
                if future_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    return True
            case 22:
                if future_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    return True
            case 25:
                if future_layer == 1:
                    return True
            case 27:
                if future_layer == 10 or future_layer >= 19 and future_layer <= 22:
                    door_sfx.play()
                    return True
    elif future_layer >= 20:
        match future_layer:
            case 20:
                if c_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    return True
            case 21:
                if c_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    return True
            case 22:
                if c_layer == 10 or future_layer == 27:
                    door_sfx.play()
                    return True
            case 25:
                if c_layer == 1:
                    return  True
            case 27:
                if c_layer == 10 or future_layer >= 20 and future_layer <= 22:
                    return True
    return False
menu = True
def _menu(mask_array, pos_array, mouse_mask, proper_pos, is_clicked):
    for i in mask_array:
        mask = pygame.mask.from_surface(i, 0)
        position = pos_array[mask_array.index(i)]
        button_rect = pygame.Rect(position[0], position[1], i.get_width(), i.get_height())
        overlapping_mask = mask.overlap_mask(mouse_mask, (proper_pos[0] - position[0], proper_pos[1] - position[1]))
        screen.blit(overlapping_mask.to_surface(None, i, None), position)
        if button_rect.collidepoint(proper_pos[0], proper_pos[1]) and is_clicked:
            return mask_array.index(i)


class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int, slider_body, slider_knob, speaker) -> None:
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
        overlapping_mask_speaker = self.speaker_mask.overlap_mask(mouse_mask, (proper_pos[0] - self.speaker_pos[0], proper_pos[1] - self.speaker_pos[1]))
        screen.blit(overlapping_mask_speaker.to_surface(None, self.speaker, None), self.speaker_pos)
        overlapping_mask_slider_body = self.slider_body_mask.overlap_mask(mouse_mask, (proper_pos[0] - self.slider_body_pos[0], proper_pos[1] - self.slider_body_pos[1]))
        screen.blit(overlapping_mask_slider_body.to_surface(None, self.slider_body, None), self.slider_body_pos)
        overlapping_mask_slider_knob = self.slider_knob_mask.overlap_mask(mouse_mask, (
        proper_pos[0] - self.slider_knob_pos[0], proper_pos[1] - self.slider_knob_pos[1]))
        screen.blit(overlapping_mask_slider_knob.to_surface(None, self.slider_knob, None), self.slider_knob_pos)
        
    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min
click = False
pygame.time.set_timer(pygame.USEREVENT, 1000)
timer = random.randint(5,10)
pygame.mixer.music.set_endevent(END_MUSIC)
slider = Slider((300 * scale_x,600 * scale_y), (200 * scale_x,100 * scale_y), 0.5, 0, 100, slider_body, slider_knob, speaker_symbol)
while running:
    screen.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
    proper_pos = (mx - cx, my - cy)
    mouse_rect = pygame.Rect(mx, my, 50, 50)
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
                menu = False
                pygame.mixer.music.fadeout(3000)
                pygame.mixer.music.queue(ambience_array[0])
            case 1:
                running = False
                menu = False
                #pygame.mixer.music.fadeout(3000)
        slider.render(screen, mask_2, proper_pos)
        if slider.container_rect.collidepoint((mx,my)) and mouse[0]:
            slider.move_slider((mx,my))

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
        screen.blit(overlap_mask.to_surface(None, mask_being_rendered, None), note_position_offset)

    for i in location_areas:
        i._show_in_pos(mask_2, proper_pos)

    for event in pygame.event.get():
        if event.type == END_MUSIC and not pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
        if event.type == pygame.USEREVENT:
            timer -= 1
            if timer < 0:
                timer = random.randint(5, 10)
                #pygame.mixer.Channel(7).play(random.choice(scary_sfx_array))
                #pygame.mixer.Channel(7).set_volume(random.uniform(0, 1), random.uniform(0, 1))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if _check_pos(0, 0) > 10 and finished_investigating:
                    mask_being_rendered = map
                    note_position_offset = (0, 0)
                    for i in location_areas:
                        i.currently_investigating = False
                        if i.which_am_i == _check_pos(0, 0):
                            _finished_investigating(_check_pos(0, 0), map_layout, i, door_layout)
                            i.investigated = True
                    mask = pygame.mask.from_surface(mask_being_rendered, 0)
                    finished_investigating = False
                elif _check_pos(0, 0) > 10:
                    if _check_pos(0, 0) == 17:
                        mapX = 13
                        mapY = 5
                        current_layer = 9
                        for i in location_areas:
                            i.currently_investigating = False
                            if i.which_am_i == 17:
                                _finished_investigating(_check_pos(0, 0), map_layout, i, door_layout)
                                i.investigated = True
                    elif _check_pos(0, 0) > 19:
                        print(_check_pos(0, 0))
                    else:
                        for i in range(len(object_sfx)):
                            for i in location_areas:
                                i.currently_investigating = True
                            objects = RandomObject(note_1, update_runner_array, object_sfx, _check_pos(0, 0), final_invest_sfx)
                            update_runner_array.append(objects)
            if running:
                match event.key:
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_w:
                        if not pygame.mixer.Channel(0).get_busy():
                            num_to_check = _check_pos(0, 1)
                            change_x_y = [0,-1]
                            if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check, open_door_sfx):
                                current_layer = num_to_check
                                mapY += 1
                                if not pygame.mixer.Channel(0).get_busy():
                                    walk_sfx.play()
                            elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                                current_layer = _door(num_to_check)
                                mapY += 1
                                open_door_sfx.play()
                            else:
                                if _check_door(mapX, mapY + 1):
                                    locked_door_sfx.play()
                                else:
                                    wall_sfx.play()
                                left_channel.set_volume(1, 1)
                    case pygame.K_s:
                        if not pygame.mixer.Channel(0).get_busy():
                            num_to_check = _check_pos(0, -1)
                            change_x_y = [0, 1]
                            if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check, open_door_sfx):
                                current_layer = num_to_check
                                mapY -= 1
                                if not pygame.mixer.Channel(0).get_busy():
                                    walk_sfx.play()
                            elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                                current_layer = _door(num_to_check)
                                mapY -= 1
                                open_door_sfx.play()
                            else:
                                if _check_door(mapX, mapY - 1):
                                    locked_door_sfx.play()
                                else:
                                    wall_sfx.play()
                                left_channel.set_volume(0.5,0.5)
                    case pygame.K_d:
                        if not pygame.mixer.Channel(0).get_busy():
                            num_to_check = _check_pos(1, 0)
                            change_x_y = [-1, 0]
                            if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check, open_door_sfx):
                                current_layer = num_to_check
                                mapX += 1
                                if not pygame.mixer.Channel(0).get_busy():
                                    walk_sfx.play()
                            elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                                current_layer = _door(num_to_check)
                                mapX += 1
                                open_door_sfx.play()
                            else:
                                if _check_door(mapX + 1, mapY):
                                    locked_door_sfx.play()
                                else:
                                    wall_sfx.play()
                                left_channel.set_volume(0,1)
                    case pygame.K_a:
                        if not pygame.mixer.Channel(0).get_busy():
                            num_to_check = _check_pos(-1, 0)
                            change_x_y = [1, 0]
                            if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check, open_door_sfx):
                                current_layer = num_to_check
                                mapX -= 1
                                if not pygame.mixer.Channel(0).get_busy():
                                    walk_sfx.play()
                            elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                                current_layer = _door(num_to_check)
                                mapX -= 1
                                open_door_sfx.play()
                            else:
                                if _check_door(mapX - 1, mapY):
                                    locked_door_sfx.play()
                                else:
                                    wall_sfx.play()
                                left_channel.set_volume(1,0)
                before_volume = volume
                le_sfx = _check_sounds(mapX, mapY, num_to_check, walk_sfx_array, wall_sfx_array, door_open_array, door_locked_array)
                new_list = floor_layout[mapY]
                if new_list[mapX] == 7 and not fell_down:
                    walk_sfx = pygame.mixer.Sound("../SFX/falling_down_stairs.mp3")
                    fell_down = True
                elif new_list[mapX] == 8 and not break_glass:
                    walk_sfx = pygame.mixer.Sound("../SFX/break_glass.mp3")
                    break_glass = True
                else:
                    walk_sfx = pygame.mixer.Sound(le_sfx[0])
                wall_sfx = pygame.mixer.Sound(le_sfx[1])
                open_door_sfx = pygame.mixer.Sound(le_sfx[2])
                locked_door_sfx = pygame.mixer.Sound(le_sfx[3])
                object_sfx = investigation_arrays[le_sfx[4]]
                volume = le_sfx[5] + 1
                name = le_sfx[6]
                pygame.mixer.music.set_volume(volume)
                if before_volume != volume:
                    pygame.mixer.music.fadeout(1600)
                    pygame.mixer.music.queue(ambience_array[le_sfx[5]])
                if le_sfx[4] == 2:
                    garden_time = True
                else:
                    garden_time = False
        if event.type ==pygame.QUIT:
            running = False
    match name:
        case "main":
            pos_audio._update(8, 7, mapX, mapY,elevator_flicker)
        case "garden":
            pos_audio._update(3,3, mapX, mapY, fountain)
        case "staff_area":
            pos_audio._update(6,1, mapX, mapY, dying_man)
        case "comms_log":
            if not comms_log_heard:
                pos_audio._update(6, 7, mapX, mapY, comms_log)
        case "nothing":
            pos_audio._update(10000,10000, 0, 0, pygame.mixer.Sound("../SFX/break_glass.mp3"))
    _update_runner(update_runner_array)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()