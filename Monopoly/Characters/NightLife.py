from ..Players import Player
from ..Visualisations import decision_menu, display_message
import pygame as pg


class NightLife(Player):
    '''Can gain mystery shots'''
    def __init__(self, name):
        super().__init__(name, "Monopoly/assets/character6.png")

    def get_power_name(self):
        return "Получи mystery shot"

    def power(self, game):
        if self.has_power():
            decision_menu(game.screen, "Получаваш Mystery shot за бурната вечер!", [["Добре!", (500, 300), (150, 50)]],game)
            self.use_power()
            self.mystery_shots += 1
        else:
            display_message(game.screen, game.font, 500, 50, f"Изхабилите сте силата си! Още {self.power_cooldown} хода")
            pg.display.flip()
            pg.time.wait(1000)