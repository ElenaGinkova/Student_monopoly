from ..Players import Player
from ..Visualisations import decision_menu, create_buttons, display_message, visualise, choose_between_players
from ..Board import Dice
import pygame as pg


GREEN_COLOR = (100, 140, 100)
PRICES_MAP = {"50" : 50, "100" : 100, "200" : 200, "300" : 300}
PRICES = ["50", "100", "200", "300"]

class BookWorm(Player):
    '''Can start dice roll fight'''
    def __init__(self, name):
        super().__init__(name, "Monopoly/assets/character5.png")
    
    def get_power_name(self):
        return "Борба със \"знания\""
    
    def power(self, game):
        if self.has_power():
            to_fight = choose_between_players(game, "Кого ще предизвикате?")
            
            # 1) gamble price -> player2 chooses
            buttons = create_buttons(len(PRICES), PRICES)
            price = decision_menu(game.screen, f"{to_fight.get_name()} избери сума за залагане.", buttons, game)
            price = PRICES_MAP[price]
            # 2) fight        
            winner, loser = fight(to_fight, game.get_player(), game)
            decision_menu(game.screen, f"{winner.get_name()} получава {price}лв. {loser.get_name()} губи 10 живот.", [["Честито!", (500, 300), (150, 50)]], game)
            if loser.needs_to_pay(price, game.screen, game, winner):
                loser.change_life(-10, game)
            self.use_power()
        else:
            display_message(game.screen, game.font, 500, 50, "Изхабилите сте силата си за този ход!")
            pg.display.flip()
            pg.time.wait(1000)


def fight(player1, player2, game):
    first_roll = take_turn(player1, game)
    
    second_roll = take_turn(player2, game)
    visualise(game.screen, game)
    if first_roll == second_roll:
        decision_menu(game.screen, f"Равенство. Отново!", [["Добре!", (500, 300), (150, 50)]], game)
        return fight(player1, player2, game)
    if first_roll > second_roll:
        return player1, player2
    return player2, player1


def take_turn(player, game):
    visualise(game.screen, game)
    pg.draw.rect(game.screen, GREEN_COLOR, (150, 220, 800, 300))
    display_message(game.screen, pg.font.Font(None, 32), 350, 250, f"{player.get_name()} хвърли заровете")
    dices = Dice((300, 400), (450, 400), (350,300))
    pg.display.flip()

    dice1, dice2 = dices.roll(game.screen)
    return dice1 + dice2
