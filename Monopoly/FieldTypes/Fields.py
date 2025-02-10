import random
import pygame as pg
from Button import Button
from Button import display_message, ok_button, decision_menu, visualise
import sys

TYPE_LIST = ["Property", "Sanction"] # str repr


class Field:
    def __init__(self, indx, name, position):
        self.indx = indx # in the board
        self.name = name
        self.position = position
        #extra rules

    def get_name(self):
        return self.name
    
    def action(self, player, screen):
        pass

    def get_position(self):
        return self.position
    
    def get_indx(self):
        return self.indx

#should impolement execute/play
def Sanction(Field):
    def __init__(self, indx, name, position, sanction):
        super().__init__(indx, name, position )
        self.sanction = sanction
    @property
    def field_type(self):
        return TYPE_LIST[1]
    
    def __repr__(self):
        return f"{self.name} ({self.field_type}) на {self.position} - санцкия: ${self.sanction}"
    
    def action(self, screen, game):
        message = f"{game.get_player().name}, трябва да платите санкция ${self.sanction}?"
        ok_button(message, screen, game)
        game.get_player().pay_amount(self.sanction, screen, game)