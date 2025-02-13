import pygame as pg
from Button import Button
import sys


COLOR_ACTIVE = pg.Color("dodgerblue")
BACKGROUND = pg.image.load("Monopoly/assets/BoardUNI.png")
BACKGROUND = pg.transform.smoothscale(BACKGROUND, (1100, 600) )
SCREEN_COLOR = (30, 30, 30)
GREEN_COLOR = (100, 140, 100)
HOUSE_IMAGE = pg.image.load("Monopoly/assets/house.png")
HOTEL_IMAGE = pg.image.load("Monopoly/assets/hotel.png")
    

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
    draw_background(game)
    game.dice.vis_dices(screen)
    font = pg.font.Font(None, 32)
    for p in game.get_players():
        p.draw(screen)
    display_message(screen, font,1200, 20, f"Играч: {game.get_player().get_name()}")
    display_message(screen, font,1200, 40, f"Джобни: {game.get_player().get_money()}лв.")
    display_message(screen, font,1200, 60, f"Живот: {game.get_player().get_life()}")
    if game.get_player().get_reserve():
        display_message(screen, font,1200, 80, f"Резерве: {game.get_player().get_reserve().get_name()}")
    else:
        display_message(screen, font,1200, 80, f"Резерве: ")
    game.get_player().display_image(screen, (1110, 80))
    visualise_houses_and_hotels(game)
    properties = game.get_player().get_properties()
    display_message(screen, font, 1200, 100, f"Собствености: ")
    y = 120
    for p in properties:
        mess = f"{p.get_name()}"
        if p.is_mortage():
            mess = mess + " (М)"
        display_message(screen, font, 1220, y, mess)
        y += 20
    for button in game.get_buttons():
        button.draw(screen)


def decision_menu(screen, message, buttons_info, game, image_buttons=None):
    buttons = [Button(text=option[0], position=option[1], size=option[2]) for option in buttons_info]

    if image_buttons:
        for button in image_buttons:
            buttons.append(button)

    while True:
        visualise(screen, game)

        overlay = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        panel_rect = pg.Rect(140, 220, 820, 360)
        pg.draw.rect(screen, (50, 150, 50), panel_rect, border_radius=20) 
        pg.draw.rect(screen, (255, 255, 255), panel_rect, 5, border_radius=20)

        font = pg.font.Font(None, 40)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(panel_rect.centerx, panel_rect.top + 50))
        screen.blit(text_surface, text_rect)

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


def create_boxes(count):
    boxes = []
    x_coord = 100
    y_coord = 200
    for _ in range(0, count):
        boxes.append([pg.Rect(x_coord, y_coord, 140, 32), ""])
        if x_coord < 700:
            x_coord += 300
        else:
            x_coord = 100
            y_coord += 100
    return boxes


def create_buttons(count, texts):
    buttons = []
    x_coord = 200
    y_coord = 300
    for i in range(0, count):
        buttons.append([texts[i], (x_coord, y_coord), (150, 50)])
        if x_coord < 700:
            x_coord += 200
        else:
            x_coord = 200
            y_coord += 100
    return buttons


def vis_boxes(boxes, game):
    for box, saved_text in boxes:
        txt = game.font.render(saved_text, True, COLOR_ACTIVE)
        box.w = max(200, txt.get_width() + 10)
        game.screen.blit(txt, (box.x + 5, box.y + 5))
        pg.draw.rect(game.screen, 100, box, 2)


def choose_between_players(game, mess):
    player = game.get_player()
    players = game.get_players().copy()
    players.remove(player)
    texts = []
    pl_map = {}
    for pl in players:
        pl_map[pl.get_name()] = pl
        texts.append(pl.get_name())
    buttons = create_buttons(len(texts), texts)
    chosen = decision_menu(game.screen, mess, buttons, game)
    return pl_map[chosen]


def visualise_selected_characters(game, images, positions, selected):
    for i, img in enumerate(images):
        rect = img.get_rect(topleft=(positions[i]))
        game.screen.blit(img, rect)
        if i in selected:
            pg.draw.rect(game.screen, (0, 255, 0), rect, 5) # to show that you have selected
            text_surface = game.font.render(str(selected[i]), True, (255, 255, 255))
            game.screen.blit(text_surface, (rect.x + rect.width - 100, rect.y - 25)) # to show the i of the player


def draw_background(game):
    game.screen.fill(SCREEN_COLOR)   
    game.screen.blit(game.background, (0, 100))