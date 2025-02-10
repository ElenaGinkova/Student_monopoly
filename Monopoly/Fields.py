import random
import pygame as pg
from Button import Button
from Button import display_message, ok_button, decision_menu, visualise
import sys

TYPE_LIST = ["Property", "Sanction"] # str repr


class Field:
    def __init__(self, indx, name, position, action):
        self.indx = indx # in the board
        self.name = name
        self.position = position
        self.action_str = action # str repr of act
        #extra rules

    def get_name(self):
        return self.name
    
    def action(self, player, screen):
        pass

    def get_position(self):
        return self.position
    
    def get_indx(self):
        return self.indx

class Property(Field):
    def __init__(self, indx, name, position, action, price, color_group, owner = None):
        super().__init__(indx, name, position, action)
        self.owner = owner
        self.price = price
        self.color_group = color_group
        self.mortaged = False
        self.houses = []
        self.hotel = False

    def has_hotel(self):
        return self.hotel
    
    def has_houses(self):
        return len(self.houses)
    
    def get_house_count(self):
        return len(self.houses)
    
    def get_house_money(self):
        self.houses.pop()
        return self.house_price // 2 # 50%
    
    def can_it_be_mortaged(self):
        return not self.mortaged and not self.has_hotel() and not self.has_houses()
    
    def is_mortage(self):
        return self.mortage
    
    def mortage_reward(self):
        return self.price / 2
    
    def get_mortage_money(self):
        self.mortage = True
        return self.mortage_reward()
    
    def unmortage_price(self):
        return int(self.price * 0.55)
    
    def unmortage(self):
        self.mortage = False
#
    def rent(self, screen, game):
        if self.mortaged:
            display_message(screen, game.font, 300, 100, "Тази собственост е ипотекирана! Бесплатен престой!")
            return 0
        base_rent = self.price // 10  # 10%
        if not self.houses and not self.hotel:
            return base_rent  # Default rent
        elif self.houses > 0:
            return base_rent * (2 ** self.houses)  # increase rent 2x
        elif self.hotel:
            return base_rent * (20 ** self.hotel)  # increase 20x
        return base_rent
    
    def change_owner(self, owner):
        self.owner = owner

    @property
    def house_price(self):
        return self.price // 2  # House price 50% of value
    
    @property
    def hotel_price(self):
        return self.house_price * 5

    def handle_build_house(self, screen, game):
        if self.houses < 4 and not self.hotel:
            mess = "Искате ли да построите къща?"
            dec = decision_menu(screen, mess, [["Да", (300, 370), (150, 50)], ["Не", (500, 370), (150, 50)]], game)
            if dec == "Да":
                paid = game.get_player().pay_amount(self.house_price, screen, game)
                if paid:
                    self.houses += 1
                    mess = f"Построи къща на {self.name}. Нов наем: ${self.rent}"
                    display_message(screen, game.font, 500, 40, mess)
                else:
                    mess = f"Не можа да построи къща!"
                    display_message(screen, game.font, 500, 40, mess)
            else:
                mess = f"Не пожела да строи къща!"
                display_message(screen, game.font, 500, 40, mess)
        elif self.houses == 4 and not self.hotel:
            mess = "Искате ли да построите хотел?"
            dec = decision_menu(screen, mess, [["Да", (300, 370), (150, 50)], ["Не", (500, 370), (150, 50)]], game)
            if dec == "Да":
                paid = game.get_player().pay_amount(self.hotel_price, screen, game)
                if paid:
                    self.hotel = True
                    self.houses = 0
                    mess = f"Построи хотел на {self.name}. Нов наем: ${self.rent}"
                    display_message(screen, game.font, 500, 40, mess)
                else:
                    mess = f"Не можа да построи хотел!"
                    display_message(screen, game.font, 500, 40, mess)
            else:
                mess = f"Не пожела да стои хотел!"
                display_message(screen, game.font, 500, 40, mess)
        else:
            mess = f"Не може да строите повече на {self.name}."
            display_message(screen, game.font, 500, 40, mess)
        pg.display.update()
        pg.time.wait(2000)
    
    @property
    def field_type(self):
        return TYPE_LIST[0]
    
    def get_price(self):
        return self.price
    
    def __repr__(self):
        return f"{self.name} ({self.field_type}) на {self.position} - наем: ${self.rent}"
    
    def auction(self, screen, game):
        visualise(screen, game)
        auc_message = f"Търгът за {self.get_name()} започва!"
        display_message(screen, game.font, 500, 40, auc_message)
        auction_price = 1
        active_players = game.get_players().copy()
        active_players.remove(game.get_player())
        
        while len(active_players) > 1:
            buttons = [["Залагам", (300, 370), (150, 50)], ["Пас", (500, 370), (150, 50)]]
            last_bidder = None
            # Process bid or pass
            for player in list(active_players):
                curr_bid_mess = f"Залог: ${auction_price} за {self.get_name()}"
                pl_mess = f"{curr_bid_mess}. {player.name} + $10 залагате ли?"
                decision = decision_menu(screen, pl_mess, buttons, game)
                if decision == "Залагам":
                    if player.can_pay(auction_price + 10):
                        auction_price += 10
                        last_bidder = player
                        bid_message = f"{player.name} заложи ${auction_price}."
                        display_message(screen, game.font, 500, 40, bid_message)
                    else:
                        bid2_message = f"{player.name} не може да залагате толкова високо! Дисквалифициран!"
                        display_message(screen, game.font, 500, 40, bid2_message)
                        active_players.remove(player)
                elif decision == "Пас":
                    active_players.remove(player)
                    pass_message = f"{player.name} пасува."
                    display_message(screen, game.font, 500, 40, pass_message)
                pg.display.update()
                pg.time.wait(2000)
                if len(active_players) == 1: break

            if len(active_players) == 1 and last_bidder != active_players[0]:
                # If only one player remains, let them place a final bid
                final_player = active_players[0]
                final_bid_mess = f"{final_player.name}, искате ли да купите за ${auction_price}?"
                final_decision = decision_menu(screen, final_bid_mess, [["Да", (300, 370), (150, 50)], ["Не", (500, 370), (150, 50)]], game)
                if final_decision == "Да":
                    last_bidder = final_player  # They bid at the current auction price
                else:
                    active_players.remove(final_player)  # No one wins
                        
            if last_bidder:
                winner_message = f"{active_players[0].name} купи {self.get_name()} за {auction_price}."
                original_price = self.price
                self.price = auction_price
                active_players[0].buy_property(self, screen, game)
                self.price = original_price
                visualise(screen, game)
                display_message(screen, game.font, 500, 40, winner_message)
            else:
                message = f"Никой не победи в търга за {self.name}! Собствеността остава за никого."
                visualise(screen, game)
                display_message(screen, game.font, 500, 40, message)
            pg.display.update()
            pg.time.wait(4000)
    
    #to implement
    def handle_unmortage(self, screen, game):
        pass

    def action(self, screen, game):
        visualise(screen, game)
        if not self.owner:
            '''option 1'''
            message = f"{game.get_player().name}, искате ли да купите {self.name} за ${self.price}?"
            yes_or_no = decision_menu(screen, message, [["Да", (300, 300),(100, 50)], ["Не",(450, 300), (100, 50)]], game)
            if yes_or_no == "Да":
                success = game.get_player().buy_property(self, screen, game)
                if success:
                    self.owner = game.get_player()
                    return
            self.auction(screen, game)
            #turg tuk
        elif self.owner == game.get_player():
            '''option 2 -> Player owns this property, allow property management'''
            if self.mortaged:
                message = f"{self.owner.get_name()} ипотекирана собственост!"
                display_message(screen, game.font, 500, 40, message)
                pg.display.update()
                self.handle_unmortage(screen, game)
            else:
                message = f"{game.get_player().name}, притежавате {self.name}. Искате ли да построите къща?"
                display_message(screen, game.font, 500, 40, message)
                self.handle_build_house(screen, game)
        else:
            '''option 3 -> Property is owned by someone else, pay rent'''
            if self.mortaged:
                message = f"{self.owner.get_name()} е ипотекирана собственост! Безплатен престой!"
                display_message(screen, game.font, 500, 40, message)
            else:
                rent = self.rent(screen, game)
                pg.display.update()
                message = f"{game.get_player().name}, трябва да платите ${rent} на {self.owner.get_name()}!"
                yes_or_no = decision_menu(screen, message, [["ОК", (300, 300),(100, 50)]], game)
                game.get_player().needs_to_pay(rent, screen, game, self.owner) 


#should impolement execute/play
def Sanction(Field):
    def __init__(self, indx, name, position, action, sanction):
        super().__init__(indx, name, position, action)
        self.sanction = sanction
    @property
    def field_type(self):
        return TYPE_LIST[1]
    
    def __repr__(self):
        return f"{self.name} ({self.field_type}) на {self.position} - санцкия: ${self.sanction}"
    
    def action(self, screen, game):
        message = f"{game.get_player().name}, трябва да платите санкция ${self.sanction}?"
        ok_button(message, screen, game)
        game.get_player().pay_amount(self.sanction, screen, game)