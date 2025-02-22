import pygame as pg


HOVER_COLOR = (100, 100, 100)
REGULAR_COLOR = (60, 60, 60)


class Button:
    def __init__(self, text=None, image_path=None, position=(0, 0), size=(150, 50)):#color=(0, 128, 255)
        self.text = text
        self.image = None
        self.image_rect = None
        self.size = size

        if image_path:
            self.image = pg.image.load(image_path)
            self.image = pg.transform.scale(self.image, size)
            self.image_rect = self.image.get_rect(topleft=position)

        self.rect = pg.Rect(position, size)
        #self.color = color
        self.font = pg.font.Font(None, 24) if text else None
        self.text_surface = self.font.render(text, True, (255, 255, 255)) if text else None

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.image_rect)
        else:
            mouse_pos = pg.mouse.get_pos()
            current_color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else REGULAR_COLOR
            pg.draw.rect(screen, current_color, self.rect)

            if self.text_surface:
                text_rect = self.text_surface.get_rect(center = self.rect.center)
                screen.blit(self.text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.image and self.image_rect.collidepoint(event.pos):
                return True
            elif not self.image and self.rect.collidepoint(event.pos):
                return True
        return False