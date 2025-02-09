import pygame as pg
from Button import Button, visualise, decision_menu, display_message, GREEN_COLOR
import sys


FIELD_COUNT = 34
GO_MONEY = 200
SPRITE_SCALE = (80, 130) # Resize all sprites to 100x100
HIGTH = 130
SCREEN_COLOR = (30, 30, 30)
BACKGROUND = pg.image.load('Monopoly/assets/BoardUNI.png')
BACKGROUND = pg.transform.smoothscale(BACKGROUND, (1100, 600) )
#maybe a map of every field and its coords and the next one

class Player():

    def __init__(self, name, image_p):
        self.name = name
        self.image_p = image_p
        self.image = pg.image.load(image_p)
        w = self.width
        self.image = pg.transform.scale(self.image, (w, HIGTH))
        self.rect = self.image.get_rect()
        self.position = [1000, 560] # starting position # this should be indx
        self.money = 19 # the starting amount of money
        self.life = 100 # in percents
        self.properties = []
        self.pos_indx = 0
        self.jail = False
        self.active = True#or bankrupt
    
    def get_name(self):
        return self.name
    
    def get_money(self):
        return self.money
    
    def get_life(self):
        return self.life
    
    def can_pay(self, amount):
        return self.money >= amount

    def move(self, field, screen, game):
        self.position = field.get_position()
        self.pos_indx = field.get_indx()
        visualise(screen, game)
        #self.draw(screen)

    @property
    def is_in_jail(self):
        return self.jail
    
    def get_pos_indx(self):
        return self.pos_indx
    
    def draw(self, screen):
        self.rect.topleft = self.position
        screen.blit(self.image, self.rect)
    
    @property
    def width(self):
        width, height = self.image.get_size()
        ratio = width / height
        return int(HIGTH * ratio)

    def display_image(self, screen, position):
        image = pg.image.load(self.image_p)
        w = self.width
        image = pg.transform.scale(image, (w, HIGTH))
        rect = image.get_rect()
        rect.topleft = position
        back_rect = rect.inflate(10, 10)  # Increase width and height
        pg.draw.rect(screen, (200, 200, 200), back_rect, border_radius = 20)
        screen.blit(image, rect)

    def excexute_field(self):
        pass

   
    
    

    def buy_property(self, property, screen, game):
        if self.money >= property.get_price():
            self.money -= property.get_price()
            self.properties.append(property)
            message = f"Succesfully bought {property.get_name()}"
            display_message(screen, game.font, 500, 40, message)
            return True
        buttons = [["Raise money", (300, 300), (100, 50)], ["Dont buy", (450, 300), (200, 50)]]
        message = "Do you want to raise money to buy?"
        visualise(screen, game)
        dec = decision_menu(screen, message, buttons, game)
        if dec == "Raise money":
            raised = self.try_to_raise_money(property.get_price(), screen, game)
            if raised >= property.get_price():
                return self.buy_property(property, screen, game)
            else:
                return False
        elif dec == "Dont buy":
            return False
        return False  # Default return if no valid action is taken








        
    def declare_bankruptcy(self, screen, game, creditor=None):
        """Handles bankruptcy: Transfers assets and removes player from game."""
        if creditor:
            print(f"{self.name} is bankrupt and must give everything to {creditor.name}!")
            for property in self.owned_properties:
                property.owner = creditor  # Transfer ownership
            creditor.money += self.money  # Transfer remaining money
        else:
            print(f"{self.name} is bankrupt and out of the game! All assets return to the bank.")
            for property in self.owned_properties:
                property.owner = None  # Reset ownership

        self.active = False  # Flag for elimination
        game.remove_player(self)
        # If the player has nothing to sell, they go bankrupt
        return False  # No possible way to raise money
    
    def has_what_to_mortage(self):
        for pr in self.properties:
            if pr.can_it_be_mortaged():
                return True
        return False
    
    def has_houses(self):
        for pr in self.properties:
            if pr.has_houses():
                return True
        return False
    
    #takes the whole screen
    def handle_mortage(self, screen, game):
        money = 0
        if self.has_what_to_mortage():
            visualise(screen, game)
            pg.draw.rect(screen, GREEN_COLOR, (150, 250, 800, 300))
            message = f"What do you want to mortage?"
            mortagable = [prop for prop in self.properties if prop.can_it_be_mortaged()]
            names_map = {}
            buttons = []
            x = 200
            y = 300
            for prop in mortagable:
                if x > 800:
                    x = 200
                    y = 400
                buttons.append([prop.get_name(), (x, y), (100, 50)])
                names_map[prop.name] = prop
                x += 100
            buttons.append(["Cancel", (700, 400), (100, 50)])
            decision = decision_menu(screen, message, buttons, game)
            if decision == "Cancel":
                return False
            to_mortage = names_map[decision]
            money = to_mortage.get_mortage_money()
            display_message(screen, game.font, 500, 40, f"Raised {money}!")
            self.money += money
        else:
            message = f"There is nothing to mortage!"
            display_message(screen, game.font, 500, 40, message)
        pg.display.update()
        pg.time.wait(2000) # 2 sec
        return money

    #combinate with hotel selling
    def handle_sell_house(self, screen, game):
        money = 0
        if self.has_houses():
            visualise(screen, game)
            pg.draw.rect(screen, GREEN_COLOR, (150, 250, 800, 300))
            message = f"Which house do you want to sell?"
            with_houses = [prop for prop in self.properties if prop.has_houses()]
            names_map = {}
            buttons = []
            x = 200
            y = 300
            for prop in with_houses:
                if x > 800:
                    x = 200
                    y = 400
                buttons.append([prop.get_name(), (x, y), (100, 50)])
                names_map[prop.name] = prop
                x += 100
            buttons.append("Cancel", (700, 400), (100, 50))
            decision = decision_menu(screen, message, buttons, game)
            if decision == "Cancel":
                return False
            house_to_sell = names_map(decision)
            money = house_to_sell.get_house_money()
            display_message(screen, game.font, 500, 40, f"Raised {money}!")
            self.money += money
        else:
            message = f"You dont have houses!"
            display_message(screen, game.font, 500, 40, message)
        pg.time.wait(2000) # 2 sec
        return money

    def try_to_raise_money(self, amount, screen, game):
        raised = 0
        while self.money < amount:
            message = f"{self.name}, how do you want to raise money?"
            decision = decision_menu(screen, message, [["Mortgage Property", (300, 300),(100, 50)], ["Sell House",(450, 300), (100, 50)], ["Cancel",(600, 300), (100, 50)]], game)
            #("Trade with Player", (600, 590), (200, 50)) -> to add
            #sell hotel
            if decision == "Cancel":
                break
            elif decision == "Mortgage Property":
                raised += self.handle_mortage(screen, game)
            elif decision == "Sell House":
                raised += self.handle_mortage(screen, game)
           # elif decision == "Declare Bankruptcy":#or when we catn pay???? in the prev func
             #   pass#bankrupcy = true
        return raised

    #only in some functions go bankrupt so we wont offer here
    def pay_amount(self, amount, screen, game, creditor=None):
        if self.money >= amount:
            self.money -= amount
            if creditor:
                creditor.get_money(amount)
            return True
        raised = self.try_to_raise_money(amount, screen, game)

        visualise(screen, game)
        message = f"Raised {raised} from {amount} needed"
        display_message(screen, game.font, 500, 40, message)

        while raised < amount:
            visualise(screen, game)
            message = f"Raised {raised} from {amount} needed"
            buttons = [["Raise more", (300, 300),(100, 50)],  ["Quit",(400, 300), (100, 50)]]
            dec = decision_menu(screen, message, buttons, game)
            if dec == "Raise more":
                raised += self.try_to_raise_money(amount, screen, game)
            elif dec == "Quit":
                return False
            
        #success
        self.money -= amount
        if creditor:
            creditor.get_money(amount)
        return True
    
    def gain_property(self, property):
        self.properties.append(property)