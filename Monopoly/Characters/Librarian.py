from Players import Player
from Visualisations import decision_menu, display_message, choose_between_players, visualise
import pygame as pg
from Board import Dice
from Characters.BookWorm import take_turn


GREEN_COLOR = (100, 140, 100)


class Librarian(Player):
    '''Can silence someone, who needs to roll dice. for result 1–6 they loose on eturn because of the strict order. otherwise they continue.'''
    def __init__(self, name):
        super().__init__(name, "Monopoly/assets/character8.png")
    
    def get_power_name(self):
        return "Тишина моля!"

    def power(self, game):
        if self.has_power():
            chosen = choose_between_players(game, "Kого ще нашъшкате?")
            if self.sh(chosen, game):
                chosen.cooldown = 1
                display_message(game.screen, game.font, 500, 50, f"{chosen.get_name()} Бяхте нашъшкани!")
            display_message(game.screen, game.font, 500, 50, f"{chosen.get_name()} спасихте се!")
            pg.display.flip()
            pg.time.wait(1000)
            self.use_power()
        else:
            display_message(game.screen, game.font, 500, 50, f"Изхабилите сте силата си! Още {self.power_cooldown} хода")
            pg.display.flip()
            pg.time.wait(1000)

    def sh(self, player, game):
        rolled = take_turn(player, game)
        if rolled >= 6:
            return True
        return False