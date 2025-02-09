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

#Логика за покупка на имоти: Ако полето е имот, играчът може да го купи, ако е свободен.
class Property(Field):
    def __init__(self, indx, name, position, action, price, color_group, owner = None):
        super().__init__(indx, name, position, action)
        self.owner = owner
        self.price = price
        self.color_group = color_group
        self.mortaged = False
        self.houses = []
        self.hotel = False

#for mortage
    def has_hotel(self):
        return self.hotel
    
    def has_houses(self):
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
    @property
    def rent(self, screen, game):
        if self.mortaged:
            display_message(screen, game.font, 300, 100, "This property is mortaged! Free for you to stay!")
            return 0
        base_rent = self.price // 10  # 10%
        if not self.houses and not self.hotel:
            return base_rent  # Default rent
        elif self.houses > 0:
            return base_rent * (2 ** self.houses)  # increase rent 2x
        elif self.hotel:
            return base_rent * (20 ** self.hotel)  # increase 20x
        return base_rent
    
    @property
    def house_price(self):
        return self.price // 2  # House price 50% of value

    def build_house(self, screen, game):
        if self.mortaged:
            display_message(screen, game.font, 300, 100, "This property is mortaged!")
            return
        if self.houses < 4 and not self.hotel:
            self.houses += 1
            print(f"Built a house on {self.name}. New rent: ${self.rent}")
        elif self.houses == 4 and not self.hotel:
            self.hotel = True
            self.houses = 0
            print(f"Built a hotel on {self.name}. New rent: ${self.rent}")
        else:
            print(f"Cannot build more on {self.name}.")
    
    @property
    def field_type(self):
        return TYPE_LIST[0]
    
    def get_price(self):
        return self.price
    
    def __repr__(self):
        return f"{self.name} ({self.field_type}) at {self.position} - Rent: ${self.rent}"
    
    #to implement
    def auction(self, screen, game):
        visualise(screen, game)
        auc_message = f"Auction starts for {self.get_name()}!"
        display_message(screen, game.font, 500, 40, auc_message)
        auction_price = 1
        active_players = game.get_players().copy()
        active_players.remove(game.get_player())
        
        while len(active_players) > 1:
            buttons = [["Bid", (300, 370), (150, 50)], ["Pass", (500, 370), (150, 50)]]
            last_bidder = None
            # Process bid or pass
            for player in list(active_players):
                curr_bid_mess = f"Current bid: ${auction_price} for {self.get_name()}"
                pl_mess = f"{curr_bid_mess}. {player.name} + $10 Bid?"
                decision = decision_menu(screen, pl_mess, buttons, game)
                if decision == "Bid":
                    if player.can_pay(auction_price + 10):
                        auction_price += 10
                        last_bidder = player
                        bid_message = f"{player.name} bid ${auction_price}."
                        display_message(screen, game.font, 500, 40, bid_message)
                    else:
                        bid2_message = f"{player.name} can't afford to bid higher! Disqualified!"
                        display_message(screen, game.font, 500, 40, bid2_message)
                        active_players.remove(player)
                elif decision == "Pass":
                    active_players.remove(player)
                    pass_message = f"{player.name} passed."
                    display_message(screen, game.font, 500, 40, pass_message)
                pg.display.update()
                pg.time.wait(2000)
                if len(active_players) == 1: break

            if len(active_players) == 1 and last_bidder != active_players[0]:
                # If only one player remains, let them place a final bid
                final_player = active_players[0]
                final_bid_mess = f"{final_player.name}, do you want to buy for ${auction_price}?"
                final_decision = decision_menu(screen, final_bid_mess, [["Yes", (300, 370), (150, 50)], ["No", (500, 370), (150, 50)]], game)
                if final_decision == "Yes":
                    last_bidder = final_player  # They bid at the current auction price
                else:
                    active_players.remove(final_player)  # No one wins
                        
            if last_bidder:
                winner_message = f"{active_players[0].name} bougth {self.get_name()} for {auction_price}."
                original_price = self.price
                self.price = auction_price
                active_players[0].buy_property(self, screen, game)
                self.price = original_price
                visualise(screen, game)
                display_message(screen, game.font, 500, 40, winner_message)
            else:
                message = f"No one won in the auction for {self.name}! The property remains to no one."
                visualise(screen, game)
                display_message(screen, game.font, 500, 40, message)
            pg.display.update()
            pg.time.wait(4000)
                
    def action(self, screen, game):
        if not self.owner:
            '''option 1'''
            message = f"{game.get_player().name}, would you like to buy {self.name} for ${self.price}?"
            yes_or_no = decision_menu(screen, message, [["Yes", (300, 300),(100, 50)], ["No",(450, 300), (100, 50)]], game)
            if yes_or_no == "Yes":
                success = game.get_player().buy_property(self, screen, game)
                if success:
                    return
            self.auction(screen, game)
            #turg tuk
        elif self.owner == game.get_player():
            '''option 2 -> Player owns this property, allow property management'''
            print(f"{game.get_player().name}, you own {self.name}. Would you like to build a house?")
            self.build_house(screen, game)
        else:
            '''option 3 -> Property is owned by someone else, pay rent'''
            rent = self.rent(screen, game)
            print(f"{game.get_player().name} pays ${rent} in rent to {self.owner.name}.")
            game.get_player().pay(rent, self) # calling player to pay if they cant pay
        


#should impolement execute/play
#crazy_jail, GO, Obshtaka 
def Sanction(Field):
    def __init__(self, indx, name, position, action, sanction):
        super().__init__(indx, name, position, action)
        self.sanction = sanction
    @property
    def field_type(self):
        return TYPE_LIST[1]
    
    def __repr__(self):
        return f"{self.name} ({self.field_type}) at {self.position} - Sanction: ${self.sanction}"
    
    def action(self, screen, game):
        message = f"{game.get_player().name}, needs to pay Sanction ${self.sanction}?"
        ok_button(message, screen, game)
        game.get_player().pay_amount(self.sanction, screen, game)