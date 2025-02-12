import pygame as pg
from Button import Button

class Menu:
    def __init__(self, x, y):
        x, y = 10, 10
        icon_button = Button(text="≡", position=(10, 10), size=(40, 40), color=(150, 150, 150))
        option1 = Button(text="Опция 1", position=(20, 60), size=(160, 40), color=(0, 128, 255))
        option2 = Button(text="Опция 2", position=(20, 110), size=(160, 40), color=(0, 128, 255))
        option3 = Button(text="Опция 3", position=(20, 160), size=(160, 40), color=(0, 128, 255))

        option1.callback = lambda: option_callback("Опция 1")
        option2.callback = lambda: option_callback("Опция 2")
        option3.callback = lambda: option_callback("Опция 3")
        option_buttons = [option1, option2, option3]
        expanded_size=(200, 250)

        self.x = x
        self.y = y
        self.icon_button = icon_button       
        self.option_buttons = option_buttons   
        self.expanded_rect = pg.Rect(x, y, expanded_size[0], expanded_size[1])
        self.expanded = False  

    def draw(self, screen):
        if self.expanded:
            pg.draw.rect(screen, (220, 220, 220), self.expanded_rect)
            for button in self.option_buttons:
                button.draw(screen)
        else:
            self.icon_button.draw(screen)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.expanded:
                for button in self.option_buttons:
                    if button.is_clicked(event):
                        if hasattr(button, 'callback') and callable(button.callback):
                            button.callback()
                        self.expanded = False
                        return
                if not self.expanded_rect.collidepoint(event.pos):
                    self.expanded = False
            else:
                if self.icon_button.is_clicked(event):
                    self.expanded = True