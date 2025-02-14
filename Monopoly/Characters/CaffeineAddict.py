from ..Players import Player
from ..Visualisations import decision_menu, display_message
import pygame as pg


class CaffeineAddict(Player):
    '''Може да се „зареди“ с допълнителна енергия – да хвърли допълнителен зар'''
    def __init__(self, name):
        super().__init__(name, "Monopoly/assets/character7.png")
    
    def get_power_name(self):
        return "Презареди енергия"

    def power(self, game):
        if self.has_power():
            decision_menu(game.screen, "Пий кафе и играй пак.", [["Добре", (300, 300), (150, 50)]], game)
            self.use_power()
            game.take_turn(self)
        else:
            display_message(game.screen, game.font, 500, 50, f"Изхабилите сте силата си! Още {self.power_cooldown} хода")
            pg.display.flip()
            pg.time.wait(1000)