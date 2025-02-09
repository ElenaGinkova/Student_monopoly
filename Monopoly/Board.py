import random
import pygame as pg
from Button import Button,display_message
from Fields import Property
import sys


DICE_PATHS = [f"Monopoly/assets/dice/{i}.png" for i in range(1, 7)]
TYPE_CLASS_LIST = [] # classes
BACKGROUND = pg.image.load('Monopoly/assets/BoardUNI.png')
BACKGROUND = pg.transform.smoothscale(BACKGROUND, (1100, 600) )
SCREEN_COLOR = (30, 30, 30)
FIELD_COUNT = 34
GO_MONEY = 200
JAIL_INDX = 28

#indx, name, position, action, price, color_group,
class Board:
    def __init__(self):
        self.fields = [Property(0, "0", (1100,600), "property", 20, 1), Property(1, "1", (1000,600), "property", 20, 1),
        Property(2, "2", (900,600), "property", 20, 1),Property(3, "3", (800,600), "property", 20, 1),
        Property(4, "4", (700,600), "property", 20, 1),Property(5, "5", (600,600), "property", 20, 1),
        Property(6, "6", (500,600), "property", 20, 1),Property(7, "7", (400,600), "property", 20, 1),
        Property(8, "8", (300,600), "property", 20, 1),Property(9, "9", (200,600), "property", 20, 1),
        Property(10, "10", (100,600), "property", 20, 1),Property(11, "11", (100,500), "property", 20, 1),
        Property(12, "12", (100,400), "property", 20, 1)] 

    def get_pos_from_indx(self, indx):
        return self.fields[indx].position
    
    #Animation for movement
    def move(self, player, steps, screen, game, indx = 0):
        old_pos_indx = player.get_pos_indx()
        new_pos_indx = (old_pos_indx + steps) % FIELD_COUNT
        player.move(self.fields[new_pos_indx], screen, game)
        if new_pos_indx < old_pos_indx:
            player.get_money(GO_MONEY)
    
    def get_field_from_indx(self, indx):
        return self.fields[indx]
    
    def go_to_jail(self, player, screen, game):
        self.move(player, 0, screen, JAIL_INDX)
        player.go_to_jail()

        
#чифтове също трябва да се отчитат        
class Dice:    
    def __init__(self):
        self.dice1 = 1
        self.dice2 = 1

    def vis_dices(self, screen):
        dice1_im = pg.image.load(DICE_PATHS[self.dice1 - 1])
        dice2_im  = pg.image.load(DICE_PATHS[self.dice2 - 1])
        dice1_im = pg.transform.scale(dice1_im, (70, 70))
        dice2_im = pg.transform.scale(dice2_im, (70, 70))
        screen.blit(dice1_im, (1200, 500))
        screen.blit(dice2_im, (1300, 500))

    def roll(self, screen):
        font = pg.font.Font(None, 32)
        button = Button(text = "Хвърли заровете", position = (1200, 400))
        while True:
            display_message(screen, font, 500, 40, "ДЕЙСТВИЕ: ХВЪРЛИ ЗАРОВЕТЕ")
            button.draw(screen)
            self.vis_dices(screen)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if button.is_clicked(event):
                    self.dice1 = random.randint(1,6)
                    self.dice2 = random.randint(1,6)
                    self.vis_dices(screen)
                    pg.display.update()
                    pg.time.wait(2000)
                    return self.dice1, self.dice2
                
