import pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
screen.fill(255,255,255)
pygame.display.update()

subway_surfer=pygame.image.load("subwaysurfer.png")
ludo = pygame.image.load("ludo.png")
templerun = pygame.image.load("temple run.png")
candyrush = pygame.image.load("candy rush.jpg")

screen.blit(subway_surfer, (150, 150))
screen.blit(ludo, (150, 250))
screen.blit(templerun, (150, 350))
screen.blit(candyrush, (150, 450))

font = pygame.font.Sysfont("Times New Roman", 36)
text1 = font.render("Subway Surfer", True, (0, 0, 0))
text2 = font.render("Temple Run", True, (0, 0, 0))
text3 = font.render("Candy Rush", True, (0, 0, 0))
text4 = font.render("Ludo", True, (0, 0, 0))

screen.blit(text1, (350, 150))
screen.blit(text2, (350, 250))
screen.blit(text3, (350, 350))
screen.blit(text4, (350, 450))
pygame.display.update()

while 1:
    event=pygame.event.poll()
    if event.type==pygame.MOUSEBUTTONDOWN:
        pos1=pygame.mouse.get_pos
        pygame.draw.circle(screen, (0, 0, 0), (pos1), 20, 0)
        pygame.display.update()
    elif event.type == pygame.MOUSEBUTTONUP:
        pos2=pygame.mouse.get_pos()
        pygame.draw.line(screen, (0, 0, 0),(pos1),(pos2),5)
        pygame.draw.circle(screen, (0, 0, 0), (pos2), 20, 0)
        pygame.display.update()