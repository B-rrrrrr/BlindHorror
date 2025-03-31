import os, socket

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
wall_sfx = pygame.mixer.Sound("../SFX/hitwall.mp3")
walk_sfx = pygame.mixer.Sound("../SFX/walking.mp3")
print("Hello, " +socket.gethostname() + ". Thank you for your interest.")
object_sfx = []
for i in os.scandir("../SFX/temporaryshit"):
    object_sfx.append(pygame.mixer.Sound(i))
cursor = pygame.transform.scale(cursor, (150 * scale_x, 150 * scale_y))
cx = cursor.get_width()/2
cy = cursor.get_height()/2
font = pygame.font.Font(None, 100)
running = True

mask = pygame.mask.from_surface(map, 0)
mask_2 = pygame.mask.from_surface(cursor, 0)
menu_mask_array = [start_button, quit_button, title]
menu_pos_array = [(0 * scale_x, 200 * scale_y), (700 * scale_x, 500 * scale_y), (500 * scale_x, 50 * scale_y)]
mask_being_rendered = map
note_position_offset = Vector2(0, 0)
finished_investigating = False

update_runner_array = []

mapX=6
mapY=1
current_layer = 0
map_layout = [
    [0, 7,5,5,15,6,1,1,20,21,22,18],
    [0, 7,5,5,5,5,0,0,10,10,10,10],
    [0, 3,3,3,8,8,0,0,9,9,9,17],
    [0, 13,3,3,0,0,0,0,0,0,0,0],
    [0, 13,3,3,0,0,0,0,12,25,25,1],
    [0, 3,3,3,2,2,2,11,2,25,1,1],
    [0, 3,3,3,14,4,0,0,2,1,1,1],
    [0]
]

map_layout.reverse()
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
            obj = InvestigateArea((2 + (i * 5)) * 20 * scale_x - loc_x, (38 - (map_layout.index(y) * 5)) * 20 * scale_y - loc_y, location_to_hit, location_hit, x)
            location_areas.append(obj)

def _check_pos(change_x, change_y):
    if (mapY + change_y) > 0 and (mapY + change_y) < 8 and (mapX + change_x) > 0 and (mapX+change_x) < 12:
        new_list = map_layout[mapY + change_y]
        return new_list[mapX + change_x]
    return 100

class RandomObject():
    def __init__(self, note_to_be_used, object_array, sound_array):
        self.sound = sound_array[len(object_array)]
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
        pygame.draw.rect(screen, (255, 0, 0), self.this_obj)
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
            #idk
            return True
        case 17:
            if answer == 9:
                return  True
        case 18:
            if answer == 10:
                return True
    return False

def _finished_investigating(current_num, map_layout, this_thing):
    match this_thing.which_am_i:
        case 11:
            #reception
            pass
        case 12:
            for y in map_layout:
                for i, x in enumerate(y):
                    if y[i] == 3:
                        y[i] = 1
                    elif y[i] == 4:
                        y[i] = 3
        case 13:
            #fountain
            pass
        case 14:
            for y in map_layout:
                for i, x in enumerate(y):
                    if y[i] == 5:
                        y[i] = 2
                    elif x == 6:
                        y[i] = 3
        case 15:
            for y in map_layout:
                for i, x in enumerate(y):
                    if y[i] == 7:
                        y[i] = 3
        case 16:
            for y in map_layout:
                for i, x in enumerate(y):
                    if y[i] == 8:
                        y[i] = 3
        case 17:
            #teleported into other room
            pass
        case 18:
            #final
            pass
def _wall_checker(c_layer, future_layer):
    if c_layer >= 25:
        match c_layer:
            case 25:
                if future_layer == 1:
                    return True
    elif future_layer >= 25:
        match future_layer:
            case 25:
                if c_layer == 1:
                    return  True
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
slider = Slider((300 * scale_x,600 * scale_y), (200 * scale_x,100 * scale_y), 0.5, 0, 100, slider_body, slider_knob, speaker_symbol)
while running:
    screen.fill((0,0,0))
    mx, my = pygame.mouse.get_pos()
    proper_pos = (mx - cx, my - cy)
    mouse_rect = pygame.Rect(mx, my, 50, 50)
    while menu:
        mouse = pygame.mouse.get_pressed()
        screen.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        proper_pos = (mx - cx, my - cy)
        mouse_rect = pygame.Rect(mx, my, 50, 50)
        match _menu(menu_mask_array, menu_pos_array, mask_2, proper_pos, click):
            case 0:
                menu = False
            case 1:
                running = False
                menu = False
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if _check_pos(0, 0) > 10 and finished_investigating:
                    mask_being_rendered = map
                    note_position_offset = (0, 0)
                    for i in location_areas:
                        i.currently_investigating = False
                        if i.which_am_i == _check_pos(0, 0):
                            _finished_investigating(_check_pos(0, 0), map_layout, i)
                            i.investigated = True
                    mask = pygame.mask.from_surface(mask_being_rendered, 0)
                    finished_investigating = False
                elif _check_pos(0, 0) > 10:
                    for i in range(6):
                        for i in location_areas:
                            i.currently_investigating = True
                        objects = RandomObject(note_1, update_runner_array, object_sfx)
                        update_runner_array.append(objects)
            match event.key:
                case pygame.K_ESCAPE:
                    running = False
                case pygame.K_w:
                    num_to_check = _check_pos(0, 1)
                    if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check):
                        current_layer = num_to_check
                        mapY += 1
                        walk_sfx.play()
                    elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                        current_layer = _door(num_to_check)
                        object_sfx[1].play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(1, 1)
                case pygame.K_s:
                    num_to_check = _check_pos(0, -1)
                    if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check):
                        current_layer = num_to_check
                        mapY -= 1
                        walk_sfx.play()
                    elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                        current_layer = _door(num_to_check)
                        object_sfx[1].play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(0.5,0.5)
                case pygame.K_d:
                    num_to_check = _check_pos(1, 0)
                    if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check):
                        current_layer = num_to_check
                        mapX += 1
                        walk_sfx.play()
                    elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                        current_layer = _door(num_to_check)
                        object_sfx[1].play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(0,1)
                case pygame.K_a:
                    num_to_check = _check_pos(-1, 0)
                    if num_to_check == current_layer or _check_investigate_area(current_layer, num_to_check) or _wall_checker(current_layer, num_to_check):
                        current_layer = num_to_check
                        mapX -= 1
                        walk_sfx.play()
                    elif num_to_check == current_layer + 1 and not current_layer >= 11 or num_to_check == current_layer - 1 and not current_layer >= 11:
                        current_layer = _door(num_to_check)
                        object_sfx[1].play()
                    else:
                        wall_sfx.play()
                        left_channel.set_volume(1,0)
        if event.type ==pygame.QUIT:
            running = False
    _update_runner(update_runner_array)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()