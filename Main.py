import pygame

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((826, 532))
map = pygame.image.load("map.webp").convert()
map = pygame.transform.scale_by(map, 0.5)
cursor = pygame.image.load("cursor.png").convert_alpha()
font = pygame.font.Font(None, 100)
running = True

mask = pygame.mask.from_surface(map)
mask_2 = pygame.mask.from_surface(cursor)
while running:
    screen.fill((255, 255, 255))
    mx, my = pygame.mouse.get_pos()

    #screen.blit(map, (0,0))
    screen.blit(cursor, (mx, my))
    text = font.render("Le Map", True, (0, 0, 0))
    screen.blit(text, (300, 200))

    overlap_mask = mask.overlap_mask(mask_2, (mx, my))
    screen.blit(overlap_mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(255,0,0,255)), (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)
pygame.quit()