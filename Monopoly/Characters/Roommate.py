from ..Players import Player
from ..Visualisations import decision_menu, display_message, choose_between_players
import pygame as pg


class Roommate(Player):
    '''Manipulates a player, decides that they want to "reorder the furniture" and they switch places with the player'''
    def __init__(self, name):
        super().__init__(name, "Monopoly/assets/character1.png")
    
    def get_power_name(self):
        return "Пренареди обстановката"

    def power(self, game):
        if self.has_power():
            chosen = choose_between_players(game, "Kого ще манипулирате да размените позициите си?")
            pos_indx = chosen.get_pos_indx()
            game.board.move_to_indx(chosen, self.get_pos_indx(), game)
            game.board.move_to_indx(self, pos_indx, game)
            self.use_power()
        else:
            display_message(game.screen, game.font, 500, 50, f"Изхабилите сте силата си! Още {self.power_cooldown} хода")
            pg.display.flip()
            pg.time.wait(1000)