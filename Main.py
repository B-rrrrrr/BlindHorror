import pygame
from pygame import FULLSCREEN

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((826, 532))
map = pygame.image.load("map.webp").convert_alpha()
cursor = pygame.image.load("cursor.png").convert_alpha()
cursor = pygame.transform.scale_by(cursor, 0.25)
cx = cursor.get_width()/2
cy = cursor.get_height()/2
font = pygame.font.Font(None, 100)
running = True

mask = pygame.mask.from_surface(map, 0)
mask.fill()
mask_2 = pygame.mask.from_surface(cursor, 0)

mapX=2
mapY=2
mapS=16
map_layout = [
    [0, 41,42,43,44],
    [0, 31,32,33,34],
    [0, 21,22,23,24],
    [0, 11,12,13,14],
    [0]
]
map_layout.reverse()


while running:
    screen.fill((255, 255, 255))
    mx, my = pygame.mouse.get_pos()
    screen.blit(map, (0,0))
    screen.blit(cursor, (mx - cx, my - cx))
    text = font.render("Le Map", True, (0, 0, 0))
    screen.blit(text, (300, 200))

    overlap_mask = mask.overlap_mask(mask_2, (mx - cx, my - cy))
    screen.blit(overlap_mask.to_surface(None,map, None), (0,0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
            if (event.key == pygame.K_w and mapY < 4):
                mapY += 1
            if event.key == pygame.K_s and mapY > 1:
                mapY -= 1
            if event.key == pygame.K_a and mapX > 1:
                mapX -= 1
            if event.key == pygame.K_d and mapX < 4:
                mapX += 1
            new_list = map_layout[mapY]
            print(new_list[mapX])
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()