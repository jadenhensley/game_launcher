import os, sys, subprocess
import shutil
from game_data import PROJECT_PATH, game_data
import pygame
from pygame.locals import *
from datetime import datetime
from install_games import install_game, install_games

sWidth = 1400
sHeight = 500
sIcon = sWidth *.20
pygame.init()
# screen = pygame.display.set_mode((sWidth, sHeight))
screen = pygame.display.set_mode((sWidth, sHeight), pygame.RESIZABLE)
pygame.display
clock = pygame.time.Clock()
monogram = pygame.font.Font(f"monogram.ttf", 32)

MOUSEDOWN = False

class GUIButton():
    def __init__(self, surface, text, x, y, function):
        self.rect = pygame.rect.Rect(x, y, len(text)*20, 52)
        self.text = text
        self.surface = surface
        self.function = function
        self.color = (10,10,10)

    def update(self):
        global MOUSEDOWN
        pygame.draw.rect(self.surface, self.color, self.rect)
        printg(self.surface, self.text, self.rect.x, self.rect.y)
        c = pygame.mouse.get_pos()
        if self.rect.collidepoint(c[0],c[1]):
            self.color = (90,90,90)
            pygame.draw.rect(self.surface, self.color, self.rect)
            printg(self.surface, self.text, self.rect.x, self.rect.y)
            if MOUSEDOWN:
                self.function()

class GUIGameIcon():
    def __init__(self, surface, text, icon, x, y, executable):
        self.rect = pygame.rect.Rect(x, y, sIcon, sIcon)
        self.text = text
        self.icon = pygame.image.load(f"{PROJECT_PATH}/{icon}")
        self.icon = pygame.transform.scale(self.icon, (sIcon, sIcon))
        self.color = (40, 180, 99)
        self.surface = surface
        self.executable = executable

    
    def update(self):
        global MOUSEDOWN, fullscreen
        self.surface.blit(self.icon, (self.rect.x, self.rect.y))
        pygame.draw.rect(self.surface, self.color, self.rect, 5)
        c = pygame.mouse.get_pos()
        if self.rect.collidepoint(c[0],c[1]):
            pygame.draw.rect(self.surface, (255,255,255), self.rect, 5)
            if MOUSEDOWN:
                # pygame.draw.rect(self.surface, (255,0,0), self.rect)
                if 'py' in self.executable:
                    fullscreen = False
                    run_game = subprocess.run(f"py {PROJECT_PATH}/{self.executable}", stdout=subprocess.PIPE, shell=True)
                    message = run_game.stdout.decode()
                    print(message)
                if 'exe' in self.executable:
                    run_game = subprocess.run(f"./{PROJECT_PATH}/{self.executable}", stdout=subprocess.PIPE, shell=True)
                    message = run_game.stdout.decode()
                    print(message)
                if 'install' in self.executable:
                    href = self.executable.split()[1]
                    install_game(self.text, href)
        printg(self.surface, self.text, self.rect.x, self.rect.y-30, self.color)


def printg(surface, text, x, y, color=(255,255,255)):
    text = monogram.render(text, True, color)
    surface.blit(text, (x, y))

fullscreen = False

# delButton = GUIButton(screen, "delete games", sWidth - 200, sHeight - 200, delete_games)

def launcher():
    global MOUSEDOWN, screen, fullscreen, monogram, sIcon
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_f]:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((sWidth, sHeight), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((sWidth, sHeight))
                # pygame.display.toggle_fullscreen()
            if key[pygame.K_a]:
                print(pygame.display.get_window_size())
                monogram = pygame.font.Font(f"monogram.ttf", pygame.display.get_window_size()[1]//20)
        if event.type == pygame.MOUSEBUTTONDOWN:
            MOUSEDOWN = True
        if event.type == pygame.MOUSEBUTTONUP:
            MOUSEDOWN = False

    screen.fill((0,0,0))

    # monogram = pygame.font.Font(f"monogram.ttf", pygame.display.get_window_size()[1]//20)
    sIcon = pygame.display.get_window_size()[0] *.20


    for x, game in enumerate(game_data["games"]):
        try:
            i = GUIGameIcon(screen, game_data["games"][game]["title"], game_data["games"][game]["icon"], 20+x*1*(sIcon+30), 100, game_data["games"][game]["executable"])
            i.update()
        except FileNotFoundError:
            href = game_data["games"][game]["repository"]
            i = GUIGameIcon(screen, game, "notfound.png", 20+x*1*(sIcon+30), 100, f"install {href}")
            i.update()
            printg(screen, "click icon to install game", 20, sHeight - 100)

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    printg(screen, current_time, pygame.display.get_window_size()[0] // 2, 10)
    printg(screen, "Pygame Launcher / OS", 10, 10)

    # delButton.update()

    pygame.display.update()
    # pygame.display.flip()

while True:
    launcher()
    clock.tick(60)
    pygame.display.set_caption("Pygame Launcher")
