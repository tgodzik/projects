import pygame
from pygame.locals import *
import buttons


def play(what):
    def inner_play():
        pygame.mixer.music.load(what)
        pygame.mixer.music.play(0)

    return inner_play


#Initialize pygame

class ButtonWindow:
    def __init__(self, resolution):
        self.resolution = resolution
        pygame.init()
        self.screen = pygame.display.set_mode((resolution[0], resolution[1]), 0, 32)
        pygame.display.set_caption("Sample interface")
        w = self.resolution[0]
        h = self.resolution[1]
        self.button1 = buttons.Button(self.screen, color=(107, 142, 35), x=w / 8, y=h / 8,
                                      length=w / 4, height=h / 4, text="Sound 1")
        self.button2 = buttons.Button(self.screen, color=(107, 142, 35), x=5 * w / 8, y=h / 8,
                                      length=w / 4, height=h / 4, text="Sound 2")
        self.button3 = buttons.Button(self.screen, color=(107, 142, 35), x=w / 8, y=5 * h / 8,
                                      length=w / 4, height=h / 4, width=0, text="Sound 3")
        self.button4 = buttons.Button(self.screen, color=(107, 142, 35), x=5 * w / 8, y=5 * h / 8,
                                      length=w / 4, height=h / 4, width=0, text="Sound 4")

    #Update the display and show the button
    def update_display(self):
        self.screen.fill((255, 255, 255))
        self.button1.draw()
        self.button2.draw()
        self.button3.draw()
        self.button4.draw()
        pygame.display.flip()

    def do(self):
        self.update_display()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                if self.button1.pressed(pygame.mouse.get_pos()):
                    play('data/b1.wav')()
                if self.button2.pressed(pygame.mouse.get_pos()):
                    play('data/b2.wav')()
                if self.button3.pressed(pygame.mouse.get_pos()):
                    play('data/b3.wav')()
                if self.button4.pressed(pygame.mouse.get_pos()):
                    play('data/b4.wav')()



