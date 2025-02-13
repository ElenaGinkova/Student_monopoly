import random
import pygame as pg
from Button import Button
from Visualisations import display_message
from FieldTypes.Property import Property
from FieldTypes.Chance import Chance
from FieldTypes.Go_to_jail import GoToJail
from FieldTypes.Go import Go
from FieldTypes.Nothing import Nothing
from FieldTypes.UNSS import UNSS
from FieldTypes.Canteen import Canteen
from FieldTypes.December8 import December8
from FieldTypes.Bus_property import BusProperty
from FieldTypes.Radio import Radio
from FieldTypes.Erasm import Erasm
from FieldTypes.Exe import Exe
from FieldTypes.Exam import Exam
import sys


DICE_PATHS = [f"Monopoly/assets/dice/{i}.png" for i in range(1, 7)]
TYPE_CLASS_LIST = [] # classes
BACKGROUND = pg.image.load('Monopoly/assets/BoardUNI.png')
BACKGROUND = pg.transform.smoothscale(BACKGROUND, (1100, 600) )
SCREEN_COLOR = (30, 30, 30)
FIELD_COUNT = 34
GO_MONEY = 200
JAIL_INDX = 28


#TO DO
# -> bus_propery да насл prop ама като пита за къши да казва не а за цена спрямо бройката която притежава
# -> стол
# -> радио
# -> exe
# -> изпит
# -> УНСС
# -> еразъм


# chance (self, indx, name, position):
# go jail (self, indx, name, position):
# go  (self, indx, name, position):
# nothing (self, indx, name, position, text):
# property (self, indx, name, position, price, color_group, owner = None):
class Board:
    def __init__(self):
        self.bus_indexes = [6, 13, 22, 32]
        self.fields = [
            #1
            Go(0, "GO", (1000, 600)), December8(1, "8 декември", (900,600)),
            Radio(2, "Студентско радио", (810,600)), Property(3, "Лападунди", (720,600), 30, 1),
            Canteen(4, "Стол", (640,600)), Property(5, "Фитнес33", (560,600), 60, 1),
            BusProperty(6, "Христо Ботев", (480,600), 200, 9), Property(7, "Joystation", (390,600), 100, 2),
            Chance(8, "Карта пробвай се!", (300,600)), Property(9, "KFC", (220,600), 120, 2),
            Exe(10, "Exe", (140,600)), GoToJail(11, "Усмири се", (30,600)),
            #2
            Property(12, "Тмаркет", (30,500), 140, 3), BusProperty(13, "Зимен дворец", (30,420), 200, 9),
            Property(14, "Сими теви", (30,340), 160, 3), Property(15, "Петлето", (30,260), 180, 4),
            Property(16, "Donnas", (30,180), 200, 4), Nothing(17, "Почивка", (30,100), "Имаш ден без притеснения! Отпусни се"),
            #3
            Canteen(18, "Стол", (130,80)), Property(19, "GyroLand", (220,80), 220, 5),
            Exam(20, "Изпит", (310,80)), Property(21, "Исос", (390,80), 240, 5),
            BusProperty(22, "Детски дом", (480,80), 200, 9), Property(23, "Малинова долина", (560,80), 260, 6),
            UNSS(24, "УНСС", (650,80)), Property(25, "Илюжън", (730,80), 280, 6), 
            Chance(26, "Карта пробвай се!", (810,80)), Erasm(27, "Еразъм!", (900,80)),
            Nothing(28, "Наблюдавайте лудите", (1010, 80), "Този път не сте сред тях"), Property(29, "Клуб 33", (1010,190), 300, 7),
            #4
            Exam(30, "Изпит", (1010,270)), Property(31, "Плаза", (1010,350), 320, 7),
            BusProperty(32, "Детски ясли", (1010,430), 200, 9), Property(33, "Дианабад", (1010,510), 350, 8)
        ] 

    def get_pos_from_indx(self, indx):
        return self.fields[indx].position
    
    #Animation for movement
    def move(self, player, steps, screen, game):
        old_pos_indx = player.get_pos_indx()
        new_pos_indx = old_pos_indx
        if player.reverse_moving:
            new_pos_indx -= steps
            if new_pos_indx < 0:
                new_pos_indx += FIELD_COUNT
            player.reverse_move()
            if new_pos_indx > old_pos_indx and new_pos_indx != 0:
                player.recieve_money(screen, game, GO_MONEY)
            player.move(self.fields[new_pos_indx], screen, game)
        else:
            new_pos_indx = (old_pos_indx + steps) % FIELD_COUNT
            player.move(self.fields[new_pos_indx], screen, game)
            if new_pos_indx < old_pos_indx and new_pos_indx != 0:
                player.recieve_money(screen, game, GO_MONEY)
    
    def get_field_from_indx(self, indx):
        return self.fields[indx]

    def go_to_jail(self, player, screen, game):
        player.move(self.fields[JAIL_INDX], screen, game)
        player.go_to_jail()

    def get_next_bus_field(self, indx):
        if indx >= self.bus_indexes[3]: return self.fields[0]

        for i in self.bus_indexes:
            if i > indx:
                return self.fields[i]

        
#чифтове също трябва да се отчитат        
class Dice:    
    def __init__(self, pos1 = (1200, 500), pos2 = (1300, 500), button_pos = (1200, 400)):
        self.dice1 = 1
        self.dice2 = 1
        self.pos1 = pos1
        self.pos2 = pos2
        self.button = Button(text = "Хвърли заровете", position = button_pos)

    def vis_dices(self, screen):
        dice1_im = pg.image.load(DICE_PATHS[self.dice1 - 1])
        dice2_im  = pg.image.load(DICE_PATHS[self.dice2 - 1])
        dice1_im = pg.transform.scale(dice1_im, (70, 70))
        dice2_im = pg.transform.scale(dice2_im, (70, 70))
        screen.blit(dice1_im, self.pos1)
        screen.blit(dice2_im, self.pos2)

    def roll(self, screen):
        font = pg.font.Font(None, 32)
        while True:
            display_message(screen, font, 500, 40, "ДЕЙСТВИЕ: ХВЪРЛИ ЗАРОВЕТЕ")
            self.button.draw(screen)
            self.vis_dices(screen)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if self.button.is_clicked(event):
                    self.dice1 = random.randint(1,6)
                    self.dice2 = random.randint(1,6)
                    #self.vis_dices(screen)
                    pg.display.update()
                    return self.dice1, self.dice2
                
