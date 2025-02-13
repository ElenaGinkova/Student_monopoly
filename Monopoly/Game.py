import pygame as pg
import sys
from Characters.GirlsMagnet import GirlsMagnet
from Characters.BookWorm import BookWorm
from Characters.Tutor import Tutor
from Characters.CleaningLady import CleaningLady
from Characters.Roommate import Roommate
from Characters.TicketChecker import TicketChecker
from Characters.NightLife import NightLife
from Characters.CaffeineAddict import CaffeineAddict
from Characters.Librarian import Librarian
from collections import OrderedDict
from Button import Button
from Visualisations import *
from Board import Dice, Board
import random


SCREEN_DIMENSIONS = (1400, 700)
SCREEN_COLOR = (30, 30, 30)
SPRITE_SCALE = (100, 100)
FPS = 60
COLOR_INACTIVE = pg.Color("lightskyblue")
COLOR_ACTIVE = pg.Color("dodgerblue")
clock = pg.time.Clock()
JAIL_INDX = 1000, 200


#do not put everything in self and in the class...
#maybe gameprep class and other for gameplay
#maybe shouldnt be stored in self but get the info and forget abt it
#maybe in class player or idk
class Game:
    characters_paths = [f"Monopoly/assets/character{i}.png" for i in range(9)]#
    characters_dict = {0 : CleaningLady, 1 : Roommate, 2 : Tutor, 3 : TicketChecker,
                       4 : GirlsMagnet, 5 : BookWorm, 6 : NightLife, 7 : CaffeineAddict, 8 : Librarian}

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_DIMENSIONS)
        pg.display.set_caption("Monopoly")
        self.font = pg.font.Font(None, 32)
        self.players = []
        self.input_boxes = []
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
    
    def draw_background(self):
        self.screen.fill(SCREEN_COLOR)   
        self.screen.blit(self.background, (0, 100))
    
    def vis_button(self, text, x, y):
        button = pg.Rect(x, y, 100, 40)
        button_text = self.font.render(text, True, (255, 255, 255))
        pg.draw.rect(self.screen, COLOR_ACTIVE, button)
        self.screen.blit(button_text, (button.x + 10, button.y + 5))
        self.button = button
        pg.display.flip()
        clock.tick(FPS)

    def get_textbox_info(self, event, indx):
        if event.key == pg.K_BACKSPACE:
            self.input_boxes[indx][1] = self.input_boxes[indx][1][:-1]
        else:
            self.input_boxes[indx][1] += event.unicode

    def active_box_i(self, event):
        i = 0
        found = False
        for box, _ in self.input_boxes:
            if box.collidepoint(event.pos):  # Check clicked box
                found = True
                break
            i += 1
        if found:
            return i
        return -1
    
    def are_filled(self, input_boxes):
        for box in input_boxes:
            if box[1] == "":
                return False
        return True

#input boxes da ne sa v self
    def get_names(self):
        self.input_boxes = create_boxes(self.pl_count)
        active_box = None
        messege = False
        while True:
            self.screen.fill(SCREEN_COLOR)
            vis_boxes(self.input_boxes, self)
            if messege:
                display_message(self.screen, self.font, 700, 300, "Моля попълнете всички имена!")
            self.vis_button("Предай", 400, 500)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    active_box = None 
                    i = self.active_box_i(event)
                    if i != -1:
                        active_box = i

                    if self.button.collidepoint(event.pos):
                        if self.are_filled(self.input_boxes):
                            return self.input_boxes
                        else:
                            messege = True
                if event.type == pg.KEYDOWN and active_box is not None:
                    self.get_textbox_info(event, active_box)
                    messege = False

    def is_valid_count(self):
        try:
            number = int(self.input_boxes[0][1])
            if 2 <= number <= 10:
                return True
            else:
                return False
        except ValueError:
            return False

    def choose_count(self):
        self.input_boxes = [[pg.Rect(100, 100, 140, 32), ""]]
        valid = True
        while True:
            self.screen.fill(SCREEN_COLOR)
            display_message(self.screen, self.font, 60,50,"Въведете бройка играчи[2-10]: ")
            
            if not valid:
                display_message(self.screen, self.font,400, 50,"Грешен вход!")

            vis_boxes(self.input_boxes, self)
            self.vis_button("Нататък", 300, 300)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and self.button.collidepoint(event.pos):
                    valid = self.is_valid_count()
                    if valid:
                        return int(self.input_boxes[0][1])
                    
                if event.type == pg.KEYDOWN:
                    self.get_textbox_info(event, 0)
    
    def visualise_selected_characters(self, images, positions, selected):
        for i, img in enumerate(images):
            rect = img.get_rect(topleft=(positions[i]))
            self.screen.blit(img, rect)
            if i in selected:
                pg.draw.rect(self.screen, (0, 255, 0), rect, 5) # to show that you have selected
                text_surface = self.font.render(str(selected[i]), True, (255, 255, 255))
                self.screen.blit(text_surface, (rect.x + rect.width - 100, rect.y - 25)) # to show the i of the player

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
        images = [pg.image.load(path) for path in self.characters_paths]
        positions = [(i * 180 + 200, 350 - images[i].get_height()) for i in range(5)] # first row
        positions.extend([(i % 5 * 180 + 200, 650 - images[i].get_height()) for i in range(5,9)]) # second row
        selected = OrderedDict() # I need the order of adding 

        while True:
            self.screen.fill(SCREEN_COLOR)
            instructions = self.font.render("Изберете герои: {} оставащи".format(self.pl_count - len(selected)), True, (255, 255, 255))
            self.screen.blit(instructions, (50, 10))
            self.visualise_selected_characters(images, positions, selected)
            self.vis_button("Играй!", 900, 600)
            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.button.collidepoint(event.pos) and len(selected) == self.pl_count:
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
            # 1) ROLL -> add rolling button or mortage/unmortage/trade buttons and decision while roll then continue
            dice1, dice2 = self.dice.roll(self.screen)
            total = dice1 + dice2

            if player.is_in_jail:
                free = self.handle_jail(self.player, dice1, dice2, self.screen)
                if not free:
                    return
                else:
                    continue
            # 2) MOVE
            self.board.move(self.player, total, self.screen, self)      
            # 3) GET FIELD
            curr_field_indx = self.player.get_pos_indx()
            curr_field = self.board.get_field_from_indx(curr_field_indx)
            # 5) CHECK FOR DOUBLES
            again = False
            if dice1 == dice2:
                again = True
                rolling_doubles += 1
                display_message(self.screen, self.font,500,50,"Хвърлихте чифт!")
                if rolling_doubles == 3:
                    decision_menu(self.screen, "Три пъти чифт! Жълта книжка!", [["Ехх", (300, 370), (150, 50)]], self)
                    self.board.go_to_jail(self.player, self.screen, self)
                    return  # End turn after going to jail
            # 4) FIELD ACTION
            curr_field.action(self.screen, self)
            if not again:  
                again = self.handle_menu()
                if not again:
                    player.reset_power()
                    break

    def handle_mystery_shot(self):
        #visualise(self.screen, self)
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

    def handle_menu(self):
        dec = decision_menu(self.screen, "Изберете какво да правите", [["Mystery shot", (200, 300), (150, 50)], ["Ползвай диплома", (400, 300), (150, 50)], ["Отипотекирай", (600, 300), (150, 50)], [f"{self.get_player().get_power_name()}", (200, 400), (200, 50)], ["Ипотекирай", (800, 300), (150, 50)]], self, [Button(text = "Край на хода", image_path = "Monopoly/assets/quit.png", position = (800, 450), size = (70, 70)), Button(image_path = "Monopoly/assets/info.png", position = (700, 450), size = (70, 70))])
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
        return self.handle_menu()

    def handle_jail(self, player, dice1, dice2, screen):
        if dice1 == dice2:
            decision_menu(self.screen, "Хвърлихте чифт! Свободни като птичка!", [["Летим", (300, 370), (150, 50)]], self) 
            player.free_from_jail()
            return True
        if player.has_out_of_jail_card():
            dec = decision_menu(self.screen, "Имате карта за освобождаване. Искате лида я ползвате?", [["Да", (300, 370), (150, 50)], ["Не", (450, 370), (150, 50)]], self)
            if dec == "Да":
                player.free_from_jail()
                decision_menu(self.screen, "Вече не сте сред хората с жълтии книжки!", ["Супер", (300, 370), (150, 50)], self)
                return True
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
        
        #need quit button then - in menu or sth
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