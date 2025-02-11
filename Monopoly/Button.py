import pygame as pg
import sys


BACKGROUND = pg.image.load('Monopoly/assets/BoardUNI.png')
BACKGROUND = pg.transform.smoothscale(BACKGROUND, (1100, 600) )
SCREEN_COLOR = (30, 30, 30)
GREEN_COLOR = (100, 140, 100)


class Button:
    def __init__(self, text=None, image_path=None, position=(0, 0), size=(150, 50), color=(0, 128, 255)):
        self.text = text
        self.image = None
        self.image_rect = None

        if image_path:
            self.image = pg.image.load(image_path)
            self.image = pg.transform.scale(self.image, size)
            self.image_rect = self.image.get_rect(topleft=position)

        self.rect = pg.Rect(position, size)  # Default rect for non-image buttons
        self.color = color  # Background color for text-based buttons
        self.font = pg.font.Font(None, 24) if text else None
        self.text_surface = self.font.render(text, True, (255, 255, 255)) if text else None

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.image_rect)
        else:
            pg.draw.rect(screen, self.color, self.rect)
            if self.text_surface:
                text_rect = self.text_surface.get_rect(center = self.rect.center)
                screen.blit(self.text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.image and self.image_rect.collidepoint(event.pos):  # Clicked for image button
                return True
            elif not self.image and self.rect.collidepoint(event.pos):  # Clicked for text button
                return True
        return False
    
def desicion(message, screen, game):
    buttons = [Button(text = "Yes", position = (600, 300), size = (100, 50)), Button(text = "No", position = (760, 300), size = (100, 50))]
    while True:
        visualise(screen, game)
        pg.draw.rect(screen, GREEN_COLOR, (580, 240, 370, 150))
        display_message(screen, pg.font.Font(None, 32), 600, 250, message)
        for button in buttons:
            button.draw(screen)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event):
                        return button.text == "Yes"

def ok_button(message, screen, game):
    button = Button(text = "OK", position = (600, 300), size = (100, 50))
    while True:
       visualise(screen, game)
       pg.draw.rect(screen, GREEN_COLOR, (580, 240, 370, 150))
       display_message(screen, pg.font.Font(None, 32), 600, 250, message)
       button.draw(screen)
       pg.display.flip()
       for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN and button.is_clicked(event):
                return

#maybe anouther function notify like
def display_message(screen, font, x, y, txt):
        
        instruction_text = font.render(txt, True, (255, 255, 255))
        screen.blit(instruction_text, (x, y))

def visualise(screen, game):
    game.draw_background()
    #game.dice.vis_dices(screen)
    font = pg.font.Font(None, 32)
    for p in game.get_players():
        p.draw(screen)
    display_message(screen, font,1200, 20, f"Играч: {game.get_player().get_name()}")
    display_message(screen, font,1200, 40, f"Джобни: {game.get_player().get_money()}")
    display_message(screen, font,1200, 60, f"Живот: {game.get_player().get_life()}")
    game.get_player().display_image(screen, (1110, 80))
    properties = game.get_player().get_properties()
    display_message(screen, font, 1200, 80, f"Собствености: ")
    y = 100
    for p in properties:
        display_message(screen, font, 1220, y, p.get_name())
        y += 20
    for button in game.get_buttons():
        button.draw(screen)

def decision_menu(screen, message, buttons_info, game):
    buttons = [Button(text=option[0], position=option[1], size=option[2]) for option in buttons_info]
    while True:
        visualise(screen, game)
        pg.draw.rect(screen, GREEN_COLOR, (150, 220, 800, 300))
        display_message(screen, pg.font.Font(None, 32), 250, 250,message)
        for button in buttons:
            button.draw(screen)
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event):
                        return button.text 
        

  