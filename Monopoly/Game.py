import pygame as pg
import sys
from .Characters.GirlsMagnet import GirlsMagnet
from .Characters.BookWorm import BookWorm
from .Characters.Tutor import Tutor
from .Characters.CleaningLady import CleaningLady
from .Characters.Roommate import Roommate
from .Characters.TicketChecker import TicketChecker
from .Characters.NightLife import NightLife
from .Characters.CaffeineAddict import CaffeineAddict
from .Characters.Librarian import Librarian
from collections import OrderedDict
from .Button import Button
from .Visualisations import visualise, decision_menu, display_message, create_buttons, create_boxes, vis_boxes
from .Board import Dice, Board
from .Visualisations import visualise_selected_characters
import random


SCREEN_DIMENSIONS = (1500, 700)
SCREEN_COLOR = (30, 30, 30)
SPRITE_SCALE = (100, 100)
FPS = 60
COLOR_INACTIVE = pg.Color("lightskyblue")
COLOR_ACTIVE = pg.Color("dodgerblue")
clock = pg.time.Clock()
JAIL_INDX = 1000, 200
BACKGROUND = pg.image.load("Monopoly/assets/background.png")
BACKGROUND = pg.transform.scale(BACKGROUND, SCREEN_DIMENSIONS)


class Game:
    characters_paths = [f"Monopoly/assets/character{i}.png" for i in range(9)]#
    characters_dict = {0 : CleaningLady, 1 : Roommate, 2 : Tutor, 3 : TicketChecker,
                       4 : GirlsMagnet, 5 : BookWorm, 6 : NightLife, 7 : CaffeineAddict, 8 : Librarian}

    def __init__(self, players = []):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_DIMENSIONS)
        pg.display.set_caption("Monopoly")
        self.font = pg.font.Font(None, 32)
        self.players = players
        self.buttons = []
        self.player = None
        self.board = Board()
        self.effect = None
        self.effect_turns_left = 0

    def get_players(self):
        return self.players
    
    def get_player(self):
        return self.player
    
    def remove_player(self, player):
        self.players.remove(player)
    
    def get_buttons(self):
        return self.buttons
    
    def are_filled(self, input_boxes):
        for box in input_boxes:
            if box[1] == "":
                return False
        return True

    def get_names(self):
        input_boxes = create_boxes(self.pl_count)
        active_box = None
        messege = False
        button = Button(text = "Предай", position = (400, 500))
        panel_rect = pg.Rect(50, 50, 1400, 600)
        font = pg.font.Font(None, 42)
        mess_rect = pg.Rect(400, 85, 600, 60)
        while True:
            self.screen.blit(BACKGROUND, (0, 0))
            pg.draw.rect(self.screen, (25, 25, 112), panel_rect, border_radius=15)

            vis_boxes(input_boxes, self)
            if messege:
                pg.draw.rect(self.screen, (70, 130, 180), mess_rect, border_radius=15)
                display_message(self.screen, font, 450, 100, "Моля попълнете всички имена!")
            button.draw(self.screen)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    active_box = active_box_i(event, input_boxes)

                    for i in range(len(input_boxes)):
                        input_boxes[i][2] = (i == active_box)

                    if button.is_clicked(event):
                        if self.are_filled(input_boxes):
                            return input_boxes
                        else:
                            messege = True
                if event.type == pg.KEYDOWN and active_box is not None:
                    get_textbox_info(input_boxes, event, active_box)
                    messege = False

    def is_valid_count(self, input_box):
        try:
            number = int(input_box[1])
            if 2 <= number <= 9:
                return True
            else:
                return False
        except ValueError:
            return False

    def choose_count(self):
        button = Button(text="Продължи", position=(600, 400), size=(200, 50))
        input_box = [pg.Rect(600, 300, 200, 50), "", False]
        valid = True
        panel_rect = pg.Rect(500, 180, 400, 300)
        mess_rect = pg.Rect(600, 85, 210, 60)
        while True:
            self.screen.blit(BACKGROUND, (0, 0))
            pg.draw.rect(self.screen, (25, 25, 112), panel_rect, border_radius=15)

            display_message(self.screen, self.font, 600, 210, "Брой играчи [2-9]:")
            
            if not valid:
                pg.draw.rect(self.screen, (25, 25, 112), mess_rect, border_radius=15)
                display_message(self.screen, self.font, 630, 100, "Грешен вход!")

            box_color = (50, 200, 50) if input_box[2] else (200, 200, 200)
            pg.draw.rect(self.screen, box_color, input_box[0], border_radius=10)

            font = pg.font.Font(None, 42)
            text_surface = font.render(input_box[1], True, (0, 0, 0))
            self.screen.blit(text_surface, (input_box[0].x + 10, input_box[0].y + 10))
            button.draw(self.screen)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if button.is_clicked(event):
                        valid = self.is_valid_count(input_box)
                        if valid:
                            return int(input_box[1])
                    input_box[2] = input_box[0].collidepoint(event.pos)
                if event.type == pg.KEYDOWN and input_box[2]:  
                    if event.key == pg.K_BACKSPACE:
                        input_box[1] = input_box[1][:-1]
                    elif event.unicode.isdigit():  
                        input_box[1] += event.unicode

    def renumerate(self, selected, missing):
        if missing in selected:
            del selected[missing]

        for idx, key in enumerate(selected.keys(), start = 1):
            selected[key] = idx

    def click_character(self, event, images, positions, selected):
        x, y = event.pos
        for i, (px, py) in enumerate(positions):
            if images[i].get_rect(topleft = (px, py)).collidepoint(x, y):
                if i in selected: # Deselect if already selected
                    del selected[i] 
                    self.renumerate(selected, i)
                elif len(selected) < self.pl_count: # Select
                    selected[i] = len(selected) + 1
    
    def create_players(self, selected, names):
        i = 0
        for image_indx in selected.keys():
            self.players.append(self.characters_dict[image_indx](names[i][1]))
            i += 1
            
    def select_characters(self, names):
        panel_rect = pg.Rect(30, 30, 1300, 650)
        images = [pg.image.load(path) for path in self.characters_paths]
        positions = [(i * 180 + 200, 350 - images[i].get_height()) for i in range(5)] # first row
        positions.extend([(i % 5 * 180 + 200, 650 - images[i].get_height()) for i in range(5,9)]) # second row
        selected = OrderedDict() # I need the order of adding 
        button = Button(text = "Играй!", position=(900,600))
        font = pg.font.Font(None, 40)
        while True:
            self.screen.blit(BACKGROUND, (0, 0))
            pg.draw.rect(self.screen, (25, 25, 112), panel_rect, border_radius=15)
            instructions = font.render("Изберете герои: {} оставащи".format(self.pl_count - len(selected)), True, (255, 255, 255))
            self.screen.blit(instructions, (70, 40))
            visualise_selected_characters(self, images, positions, selected)
            button.draw(self.screen)
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if button.is_clicked(event) and len(selected) == self.pl_count:
                        self.create_players(selected, names)
                        return
                    self.click_character(event, images, positions, selected)   

    def take_turn(self, player):
        self.dice = Dice()
        self.player = player
        rolling_doubles = 0 
        while True:
            visualise(self.screen, self)
            pg.display.flip()
            if self.player.get_cooldown():
                decision_menu(self.screen, "Ден за почивка!", [["Ехх", (300, 370), (150, 50)]], self)
                self.player.reduce_cooldown()
                return

            if player.is_in_jail:
                free = self.handle_jail(self.player, self.screen)
                if not free:
                    return
                else:
                    continue
            # 1) ROLL -> add rolling button or mortage/unmortage/trade buttons and decision while roll then continue
            dice1, dice2 = self.dice.roll(self.screen)
            total = dice1 + dice2
            # 2) MOVE
            self.board.move(self.player, total, self.screen, self)      
            # 3) GET FIELD
            curr_field_indx = self.player.get_pos_indx()
            curr_field = self.board.get_field_from_indx(curr_field_indx)
            # 4) CHECK FOR DOUBLES
            again = False
            if dice1 == dice2:
                again = True
                rolling_doubles += 1
                display_message(self.screen, self.font,500,50,"Хвърлихте чифт!")
                if rolling_doubles == 3:
                    decision_menu(self.screen, "Три пъти чифт! Жълта книжка!", [["Ехх", (300, 370), (150, 50)]], self)
                    self.board.go_to_jail(self.player, self.screen, self)
                    return  # End turn after going to jail
            # 5) FIELD ACTION
            curr_field.action(self.screen, self)
            if not again:  
                again = self.handle_menu()
                if not again:
                    player.reset_power()
                    break

    def handle_mystery_shot(self):
        buttons = []
        players = self.get_players().copy()
        players.remove(self.get_player())
        x = 200
        y = 300
        pl_map = {}
        for pl in players:
            pl_map[pl.get_name()] = pl
            buttons.append([pl.get_name(), (x, y), (200, 50)])
            x += 250
            if x >= 900:
                y += 100
                x = 200
        buttons.append(["Отказ", (x, y), (200, 50)])
        dec = decision_menu(self.screen, "Изберете играч", buttons, self)
        if dec == "Отказ":
            return
        else:
            decision_menu(self.screen, f"{dec} загуби 10 живот", [["Добре", (200, 300), (200, 50)]] , self)
            pl_map[dec].change_life(-10, self)
            self.get_player().use_mystery_shot()

    def handle_diploma(self):
        if self.get_player().has_diploma():
            dec = decision_menu(self.screen, "Искате ли да използвате диплома?", [["Да", (200, 370), (150, 50)], ["Не", (400, 370), (150, 50)]], self)
            if dec == "Да":
                dec = decision_menu(self.screen, "Още един ход!", [["Добре", (200, 370), (150, 50)]], self)
                self.take_turn(self.get_player())
        else:
            display_message(self.screen, self.font,500,50,"Нямате налични дипломи!")
            pg.display.update()
            pg.time.wait(1000)

    def handle_info(self):
        overlay = pg.Surface((self.screen.get_width(), self.screen.get_height()), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        panel_rect = pg.Rect(140, 220, 820, 360)
        pg.draw.rect(self.screen, (50, 150, 50), panel_rect, border_radius=20) 
        pg.draw.rect(self.screen, (255, 255, 255), panel_rect, 5, border_radius=20)
        
        font = pg.font.Font(None, 30)
        texts = [
            "Mystery shot - получава се при хвърляне на чифт от зарове",
            "Принуждава опонент да пропусне ход",
            "Диплома - получава се от УНСС",
            "Ползва се за бонус ход и нищо повече"
            "Можете да получите живот от:",
            "стола или от изпит",
            "Резерве-опция, която се прилага на най-много едно поле",
            "Полето е резервирано, докато не бъде преминато през него пак"
        ]
        
        for i, text in enumerate(texts):
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(panel_rect.centerx, panel_rect.top + 50 + i * 45))
            self.screen.blit(text_surface, text_rect)
        
        pg.display.flip()
        pg.time.wait(3000)

    def handle_menu(self):
        dec = decision_menu(self.screen, "Изберете какво да правите", [["Mystery shot", (200, 300), (150, 50)], ["Ползвай диплома", (400, 300), (150, 50)], ["Отипотекирай", (600, 300), (150, 50)], [f"{self.get_player().get_power_name()}", (200, 400), (200, 50)], ["Ипотекирай", (800, 300), (150, 50)], ["Купи резерве", (450, 400), (150, 50)]], self, [Button(text = "Край на хода", image_path = "Monopoly/assets/quit.png", position = (800, 450), size = (70, 70)), Button(text = "Инфо", image_path = "Monopoly/assets/info.png", position = (700, 450), size = (70, 70))])
        if dec == "Mystery shot":
            if self.get_player().has_mystery_shots():
                self.handle_mystery_shot()
            else:
                display_message(self.screen, self.font,500,50,"Нямате Mystery shot!")
                pg.display.update()
                pg.time.wait(1000)
        elif dec == "Ползвай диплома":
            self.handle_diploma()
        elif dec == "Отипотекирай":
            self.get_player().handle_unmortage(self.screen, self)
        elif dec == "Ипотекирай":
            self.get_player().handle_mortage(self.screen, self)
        elif dec == self.get_player().get_power_name():
            self.get_player().power(self)
        elif dec == "Край на хода":
            return False
        elif dec == "Купи резерве":
            self.get_player().buy_reserved(self)
        elif dec == "Инфо":
            self.handle_info()
        return self.handle_menu()

    def handle_jail(self, player, screen):
        buttons = create_buttons(3, ["Плащам 50лв.", "Карта", "Зарове"])
        dec = decision_menu(self.screen, "Как искате да се измъкнете?", buttons, self)
        if dec == "Плащам 50лв.":
            if player.can_pay(50):
                display_message(self.screen, self.font, 500, 40, "Успешно")
                player.free_from_jail()
                return True
            else:
                display_message(self.screen, self.font, 500, 40, "Неуспешно")
                pg.display.flip()
                pg.time.wait(2000)
                return self.handle_jail(player, screen)
        elif dec == "Зарове":
            dice1, dice2 = self.dice.roll(self.screen)
            if dice1 == dice2:
                decision_menu(self.screen, "Хвърлихте чифт! Свободни като птичка!", [["Летим", (300, 370), (150, 50)]], self) 
                player.free_from_jail()
                return True
            else:
                visualise(screen, self)
                display_message(self.screen, self.font, 500, 40, "Неуспешно")
                pg.display.flip()
                pg.time.wait(1000)
                return False
        elif dec == "Карта":
            if player.has_out_of_jail_card():
                dec = decision_menu(self.screen, "Имате карта за освобождаване. Искате лида я ползвате?", [["Да", (300, 370), (150, 50)], ["Не", (500, 370), (150, 50)]], self)
                if dec == "Да":
                    player.free_from_jail()
                    decision_menu(self.screen, "Вече не сте сред хората с жълтии книжки!", [["Супер", (300, 370), (150, 50)]], self)
                    return True
                else:
                    return self.handle_jail(player, screen)
            else:
                display_message(self.screen, self.font, 500, 40, "Нямате налична карта")
                pg.display.flip()
                pg.time.wait(1000)
                return self.handle_jail(player, screen)
        if player.jail_days == 3:
            decision_menu(self.screen, "Това беше последният ден на лудост!", [["Добре", (300, 370), (150, 50)]], self) 
            player.free_from_jail()
            return False
        player.day_in_jail()
        decision_menu(self.screen, f"Още {3 - player.jail_days} дни на лудост!", [["Добре", (300, 370), (150, 50)]], self)
        return False

    def go_to_jail(self):
        decision_menu(self.screen, "Връчена ви е жълта книжка!", [["Добре", (300, 370), (150, 50)]], self) 
        self.board.go_to_jail(self.player, self.screen, self)

    def eliminate(self, player):
        self.players.remove(player)

    def play(self):
        self.pl_count = self.choose_count()
        names = self.get_names()
        self.select_characters(names)
        self.sprites = pg.sprite.Group()
        self.background = pg.image.load('Monopoly/assets/BoardUNI.png')
        self.background = pg.transform.smoothscale(self.background, (1100, 600) )
        
        while True:
            for player in self.players:
                if self.effect:
                    self.effect_turns_left -= 1
                if self.effect_turns_left == 0:
                    self.effect = None

                self.take_turn(player)
                if len(self.players) == 1:
                    decision_menu(self.screen, f"Победител! {self.players[0].get_name()}", [["Йее", (300, 370), (150, 50)]], self)
                    dec = decision_menu(self.screen, "Играй отново?", [["Да", (300, 370), (150, 50)], ["Не", (500, 370), (150, 50)]], self)
                    if dec == "Да":
                        self.players.clear()
                        self.play()
                    else:
                        pg.quit()
                        sys.exit()


def get_textbox_info(input_boxes, event, indx):
    if event.key == pg.K_BACKSPACE:
        input_boxes[indx][1] = input_boxes[indx][1][:-1]
    elif len(input_boxes[indx][1]) <= 10:
        input_boxes[indx][1] += event.unicode


def active_box_i(event, input_boxes):
    for i, (box, _, _) in enumerate(input_boxes):
        if box.collidepoint(event.pos):
            return i 
    return -1 