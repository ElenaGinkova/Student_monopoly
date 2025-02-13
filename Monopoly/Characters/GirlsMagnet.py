from Players import Player
from Visualisations import choose_between_players, decision_menu, display_message
import pygame as pg


class GirlsMagnet(Player):
    '''Escord - causes cooldown - but can use this power once in 3 turns'''
    def __init__(self, name):
        self.power_cooldown = 0
        super().__init__(name, "Monopoly/assets/character4.png")
    
    def get_power_name(self):
        return "Разсеяй играч"
    
    def reset_power(self):
        if self.used_power:
            self.power_cooldown -= 1
            if self.power_cooldown <= 0:
                self.used_power = False

    def use_power(self):
        self.power_cooldown = 3
        self.used_power = True

    
    def power(self, game):
        if self.has_power():
            chosen = choose_between_players(game, "Кого избирате да разсеяте за един ход?")
            chosen.cooldown = 1
            self.use_power()
        else:
            display_message(game.screen, game.font, 500, 50, f"Изхабилите сте силата си! Още {self.power_cooldown} хода")
            pg.display.flip()
            pg.time.wait(1000)