from Players import Player
from Visualisations import choose_between_players, decision_menu, display_message
import pygame as pg


class CleaningLady(Player):
    '''Can move a player one field forward or backwards'''
    def __init__(self, name):
        super().__init__(name, "Monopoly/assets/character0.png")

    def get_power_name(self):
        return "Премести играч"
    
    
    def power(self, game):
        if self.has_power():
            chosen = choose_between_players(game, "Кого избирате да преместите?")
            forward_or_back = decision_menu(game.screen, "Едно поле напред или назад?", [["Напред", (200, 300), (150, 50)], ["Назад", (400, 300), (150, 50)]], game)
            if forward_or_back == "Напред":
                game.board.move(chosen, 1, game.screen, game) 
            else:
                chosen.reverse_move()
                game.board.move(chosen, 1, game.screen, game)
            self.use_power()
        else:
            display_message(game.screen, game.font, 500, 50, "Изхабилите сте силата си за този ход!")
            pg.display.flip()
            pg.time.wait(1000)