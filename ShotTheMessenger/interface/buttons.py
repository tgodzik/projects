import pygame


class Button:
    def __init__(self, surface, color, x, y, length, height, text, text_color=(255, 255, 255), width=0):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.length = length
        self.height = height
        self.width = width
        self.text = text
        self.text_color = text_color
        self.rect = pygame.Rect(self.x, self.y, self.length, self.height)

    def write_text(self):
        font_size = int(self.length // len(self.text))
        font = pygame.font.SysFont("Calibri", font_size)
        rendered_text = font.render(self.text, 1, self.text_color)
        self.surface.blit(rendered_text, ((self.x + self.length / 2) - rendered_text.get_width() / 2,
                                          (self.y + self.height / 2) - rendered_text.get_height() / 2))

    def draw_button(self):
        for i in range(1, 10):
            s = pygame.Surface((self.length + (i * 2), self.height + (i * 2)))
            s.fill(self.color)
            alpha = (255 / (i + 2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, self.color, (self.x - i, self.y - i, self.length + i, self.height + i), self.width)
            self.surface.blit(s, (self.x - i, self.y - i))
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.length, self.height), 0)
        pygame.draw.rect(self.surface, (190, 190, 190), (self.x, self.y, self.length, self.height), 1)

    def draw(self):
        self.draw_button()
        self.write_text()


    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
