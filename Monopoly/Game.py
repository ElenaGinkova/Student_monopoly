import pygame as pg
import sys
from Characters.GirlsMagnet import GirlsMagnet
from Characters.BookWorm import BookWorm
from Characters.Tutor import Tutor
from Characters.CleaningLady import CleaningLady
from Characters.Roommate import Roommate
from Characters.TicketChecker import TicketChecker
from Characters.NightLife import NightLife
from collections import OrderedDict
from Button import Button, display_message, visualise, decision_menu
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
class Game:
    characters_paths = [f"Monopoly/assets/character{i}.png" for i in range(7)]#
    characters_dict = {0 : CleaningLady, 1 : Roommate, 2 : Tutor, 3 : TicketChecker, 4 : GirlsMagnet, 5 : BookWorm, 6 : NightLife}

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
        
    def remove_player(self, player):
        self.players.remove(player)

    def get_player(self):
        return self.player
    
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

    #maybe shouldnt be stored in self but get the info and forget abt it
    #maybe in class player or idk
    def vis_input_boxes(self):
        for box, saved_text in self.input_boxes:
            txt = self.font.render(saved_text, True, COLOR_ACTIVE)
            box.w = max(200, txt.get_width() + 10)
            self.screen.blit(txt, (box.x + 5, box.y + 5))
            pg.draw.rect(self.screen, 100, box, 2)

    def get_textbox_info(self, event, indx):
        if event.key == pg.K_BACKSPACE:
            self.input_boxes[indx][1] = self.input_boxes[indx][1][:-1]
        else:
            self.input_boxes[indx][1] += event.unicode

    def create_name_boxes(self, count):
        self.input_boxes = []
        x_coord = 100
        y_coord = 100
        for _ in range(0, count):
            self.input_boxes.append([pg.Rect(x_coord, y_coord, 140, 32), ""])
            if x_coord < 700:
                x_coord += 300
            else:
                x_coord = 100
                y_coord += 100

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

    def get_names(self):
        self.create_name_boxes(self.pl_count)
        active_box = None
        messege = False
        while True:
            self.screen.fill(SCREEN_COLOR)
            self.vis_input_boxes()
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

            self.vis_input_boxes()
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

        for idx, key in enumerate(selected.keys(), start=1):
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
        positions.extend([(i % 5 * 180 + 200, 650 - images[i].get_height()) for i in range(5,7)]) # second row
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
        
    def vis_players(self):
        for p in self.players:
            p.draw(self.screen)

    def vis_playing(self):
        display_message(self.screen, self.font,1200, 100, f"Playing: {self.player.get_name()}")
        display_message(self.screen, self.font,1200, 130, f"Money: {self.player.get_money()}")
        display_message(self.screen, self.font,1200, 160, f"Life: {self.player.get_life()}")
        self.player.display_image(self.screen, (1110, 200))

    def populate_buttons(self):
        #self.buttons.append(Button(text = "Roll Dice", position = (1200, 400)))
        self.buttons.append(Button(text = "Buy Property", position = (20, 20)))
        self.buttons.append(Button(text = "End Turn", position = (220, 20)))

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    #to do
    def execute_action(self, button_text):
        pass
        # if button_text == "Roll Dice":
        #     self.dice.roll(self.screen)
        # elif button_text == "Buy Property":
        #     self.buy_property()
        # elif button_text == "End Turn":
        #     pass
            #self.end_turn()

    def handle_clicks(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                self.execute_action(button.text)

    #add mortage/unmortage button as option 
    def take_turn(self, player):
        self.dice = Dice()
        #self.dice.vis_dices(self.screen)
        self.player = player
        rolling_doubles = 0 

        #we need end of turn 
        while True:
            visualise(self.screen, self)
            #self.dice.vis_dices(self.screen)
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
            # 6) -> add rolling button or mortage/unmortage/trade buttons and decision while roll then continue
            #self.handle_clicks(event)
            # 6.1) has_diploms - more rolls
            if not again: break
            
  
    
    def play(self):
        self.pl_count = self.choose_count()
        names = self.get_names()
        self.select_characters(names)
        self.sprites = pg.sprite.Group()
        self.background = pg.image.load('Monopoly/assets/BoardUNI.png')
        self.background = pg.transform.smoothscale(self.background, (1100, 600) )
        self.populate_buttons()
        
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
                        self.play()
                    else:
                        pg.quit()
                        sys.exit()

        
            
                 
    
    #to do
    def create_menu(self):
        self.buttons = []#roll, quit, ...   
    
    def animate_movement(self, player, total_roll, screen):
        pass

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
        decision_menu(self.screen, f"Още {3 - player.jail_days} дни на лудост!", [["Добре", (300, 370), (150, 50)]], self) 
        return False


    def go_to_jail(self):
        decision_menu(self.screen, "Връчена ви е жълта книжка!", [["Добре", (300, 370), (150, 50)]], self) 
        self.board.go_to_jail(self.player, self.screen, self)

    def eliminate(self, player):
        self.players.remove(player)