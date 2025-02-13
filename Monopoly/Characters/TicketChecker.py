from Players import Player
from Visualisations import decision_menu, display_message, choose_between_players
import pygame as pg


class TicketChecker(Player):
    '''Can charge you 50lv because you dont have bus card'''
    def __init__(self, name):
        super().__init__(name, "Monopoly/assets/character3.png")

    def get_power_name(self):
        return "Глоби играч"

    def power(self, game):
        if self.has_power():
            chosen = choose_between_players(game, "Kого ще глобите 50лв. днес?")
            chosen.needs_to_pay(50, game.screen, game, self)
            self.use_power()
        else:
            display_message(game.screen, game.font, 500, 50, f"Изхабилите сте силата си! Още {self.power_cooldown} хода")
            pg.display.flip()
            pg.time.wait(1000)