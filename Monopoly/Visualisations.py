import pygame as pg
from Button import Button
import sys

BACKGROUND = pg.image.load("Monopoly/assets/BoardUNI.png")
BACKGROUND = pg.transform.smoothscale(BACKGROUND, (1100, 600) )
SCREEN_COLOR = (30, 30, 30)
GREEN_COLOR = (100, 140, 100)
HOUSE_IMAGE = pg.image.load("Monopoly/assets/house.png")
HOTEL_IMAGE = pg.image.load("Monopoly/assets/hotel.png")
    

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

def display_message(screen, font, x, y, txt):
        
        instruction_text = font.render(txt, True, (255, 255, 255))
        screen.blit(instruction_text, (x, y))

def visualise(screen, game):
    game.draw_background()
    game.dice.vis_dices(screen)
    font = pg.font.Font(None, 32)
    for p in game.get_players():
        p.draw(screen)
    display_message(screen, font,1200, 20, f"Играч: {game.get_player().get_name()}")
    display_message(screen, font,1200, 40, f"Джобни: {game.get_player().get_money()}")
    display_message(screen, font,1200, 60, f"Живот: {game.get_player().get_life()}")
    game.get_player().display_image(screen, (1110, 80))
    visualise_houses_and_hotels(game)
    properties = game.get_player().get_properties()
    display_message(screen, font, 1200, 80, f"Собствености: ")
    y = 100
    for p in properties:
        mess = f"{p.get_name()}"
        if p.is_mortage():
            mess = mess + " (М)"
        display_message(screen, font, 1220, y, mess)
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
        
def visualise_houses_and_hotels(game):
    players = game.get_players()
    for pl in players:
        props = pl.get_properties()
        for pr in props:
            x, y = pr.get_position()
            indx = pr.get_indx()
            if pr.has_hotel():
                if indx <= 10:
                    y -= 60
                elif indx > 10 and indx <= 16:
                    x += 100
                    y += 15
                elif indx > 16 and indx <= 27:
                    x -= 10
                    y += 125
                else: 
                    x -= 75
                    y -= 10
                game.screen.blit(HOTEL_IMAGE, (x, y))
            for i in range(0, pr.get_house_count()):
                if indx <= 10:
                    x -= 10
                    y -= 40 
                    y += i * 10
                elif indx > 10 and indx <= 16:
                    x += 100
                    y += 15
                    y += i * 10
                elif indx > 16 and indx <= 27:
                    x -= 10
                    y += 120
                    x += i * 10
                else: 
                    x -= 75
                    y += i * 10
                game.screen.blit(HOUSE_IMAGE, (x, y))