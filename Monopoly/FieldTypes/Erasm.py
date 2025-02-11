from FieldTypes.Fields import Field
from Button import decision_menu
import pygame as pg
import random


FIELD_COUNT = 34


class Erasm(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        mess = f"{self.name} - Май ще пътуваме?"
        decision_menu(game.screen, mess, [["Айде", (300, 370), (150, 50)]], game)
        field_indx = random.randint(0, FIELD_COUNT - 1)
        field = game.board.get_field_from_indx(field_indx)
        game.get_player().move(field, screen, game)
        game.get_player().recieve_money(screen, game, 200)
        mess = f"Телепортира се на {field.get_name()} и спечели 200!"
        decision_menu(game.screen, mess, [["Супер", (300, 370), (150, 50)]], game)
        field.action(screen, game)
        
        