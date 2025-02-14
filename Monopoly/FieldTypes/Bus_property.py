from ..FieldTypes.Property import Property
from ..Visualisations import decision_menu, visualise
import pygame as pg


class BusProperty(Property):
    def __init__(self, indx, name, position, price, color_group, owner = None):
        super().__init__(indx, name, position, price, color_group, owner)

    def rent(self, screen, game):
        count = self.owner.count_color_group(9)
        return 25 * count
    
    def action(self, screen, game):
        visualise(screen, game)
        if not self.owner:
            message = f"{game.get_player().name}, искате ли да купите {self.name} за {self.price}лв.?"
            yes_or_no = decision_menu(screen, message, [["Да", (300, 300),(100, 50)], ["Не",(450, 300), (100, 50)]], game)
            if yes_or_no == "Да":
                success = game.get_player().buy_property(self, screen, game)
                if success:
                    self.owner = game.get_player()
                    return
            self.auction(screen, game)
        elif self.owner is not game.get_player():
            if self.mortaged:
                message = f"{self.owner.get_name()} е ипотекирана собственост! Безплатен престой!"
                decision_menu(screen, message, [["ОК", (300, 300),(100, 50)]], game)
            else:
                rent = self.rent(screen, game)
                if game.effect:
                    rent = self.handle_effect(rent, game)
                if rent == 0: return
                pg.display.update()
                message = f"{game.get_player().name}, трябва да платите {rent}лв. на {self.owner.get_name()}!"
                yes_or_no = decision_menu(screen, message, [["ОК", (300, 300),(100, 50)]], game)
                game.get_player().needs_to_pay(rent, screen, game, self.owner) 