import pygame as pg
from Button import visualise, decision_menu, display_message, GREEN_COLOR
import sys


FIELD_COUNT = 34
GO_MONEY = 200
SPRITE_SCALE = (80, 130) # Resize all sprites to 100x100
HIGTH = 100
SCREEN_COLOR = (30, 30, 30)
BACKGROUND = pg.image.load('Monopoly/assets/BoardUNI.png')
BACKGROUND = pg.transform.smoothscale(BACKGROUND, (1100, 600) )

class Player():

    def __init__(self, name, image_p):
        self.name = name
        self.image_p = image_p
        self.image = pg.image.load(image_p)
        w = self.width
        self.image = pg.transform.scale(self.image, (w, HIGTH))
        self.rect = self.image.get_rect()
        self.position = [1000, 560] # starting position # this should be indx
        self.money = 3000 # the starting amount of money
        self.life = 100 # in percents
        self.properties = []
        self.pos_indx = 0
        self.jail = False
        self.active = True#or bankrupt
        self.add_out_of_jail_card = 0
    
    def get_name(self):
        return self.name
    
    def get_money(self):
        return self.money
    
    def get_properties(self):
        return self.properties
    
    def recieve_money(self, screen, game, money):
        message = f"{self.name} recieved {money}!"
        self.money += money
        display_message(screen, game.font, 500, 40, message)
        pg.display.update()
        pg.time.wait(2000)

    def get_life(self):
        return self.life
    
    def can_pay(self, amount):
        return self.money >= amount
    
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
    
    def get_propertries_count(self):
        house_count = 0
        hotel_count = 0
        for pr in self.properties:
            house_count += pr.get_house_count()
            if pr.has_hotel():
                hotel_count += 1
        return house_count, hotel_count
    
    def add_out_of_j_card(self):
        self.out_of_jail_card += 1

    def move(self, field, screen, game):
        self.position = field.get_position()
        self.pos_indx = field.get_indx()
        visualise(screen, game)
        #self.draw(screen)

    @property
    def is_in_jail(self):
        return self.jail
    
    def go_to_jail(self):
        self.jail = True
        
    def get_pos_indx(self):
        return self.pos_indx
    
    def draw(self, screen):
        rect = self.image.get_rect()
        rect.topleft = self.position
        back_rect = rect.inflate(0, 0)
        pg.draw.rect(screen, (200, 200, 200), back_rect, border_radius = 20)
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
        image = pg.transform.scale(image, (w, HIGTH + 20))
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
            message = f"Успешно закупихте {property.get_name()}"
            display_message(screen, game.font, 500, 40, message)
            return True
        buttons = [["Съберете пари", (300, 300), (100, 50)], ["Не купувайте", (450, 300), (200, 50)]]
        message = "Искате ли да съберете пари?"
        visualise(screen, game)
        dec = decision_menu(screen, message, buttons, game)
        if dec == "Съберете пари":
            raised = self.try_to_raise_money(property.get_price(), screen, game)
            if raised >= property.get_price():
                return self.buy_property(property, screen, game)
            else:
                return False
        elif dec == "Не купувайте":
            return False
        return False  # Default return if no valid action is taken

    #to to 
    def declare_bankruptcy(self, screen, game, creditor=None):
        if creditor:
            message = f"{self.name} дава всичко на {creditor.get_name()}!"
            display_message(screen, game.font, 500, 40, message)
            pg.display.update()
            pg.time.wait(2000)
            for property in self.properties:
                property.change_owner(creditor)  # Transfer ownership
                creditor.gain_property(property)
            creditor.money += self.money  # Transfer remaining money
        else:
            message = f"{self.name} банкрутира и е вън от играта! Всичко се връща на банката."
            display_message(screen, game.font, 500, 40, message)
            pg.display.update()
            pg.time.wait(2000)
            for property in self.owned_properties:
                property.owner = None  # Reset ownership
        self.active = False  # Flag for elimination
        game.remove_player(self)
        return False

    #takes the whole screen
    def handle_mortage(self, screen, game):
        money = 0
        if self.has_what_to_mortage():
            visualise(screen, game)
            pg.draw.rect(screen, GREEN_COLOR, (150, 250, 800, 300))
            message = f"Какво искате да ипотекирате?"
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
            buttons.append(["Отказ", (700, 400), (100, 50)])
            decision = decision_menu(screen, message, buttons, game)
            if decision == "Отказ":
                return False
            to_mortage = names_map[decision]
            money = to_mortage.get_mortage_money()
            display_message(screen, game.font, 500, 40, f"Събрахте {money}!")
            self.money += money
        else:
            message = f"Нямате какво да ипотекирате!"
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
            message = f"Коя къща желаете да продадете?"
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
            buttons.append("Отказ", (700, 400), (100, 50))
            decision = decision_menu(screen, message, buttons, game)
            if decision == "Отказ":
                return False
            house_to_sell = names_map(decision)
            money = house_to_sell.get_house_money()
            display_message(screen, game.font, 500, 40, f"Събрахте {money}!")
            self.money += money
        else:
            message = f"Нямате налични къщи!"
            display_message(screen, game.font, 500, 40, message)
        pg.time.wait(2000) # 2 sec
        return money

    def try_to_raise_money(self, amount, screen, game):
        raised = 0
        while self.money < amount:
            message = f"{self.name}, как искате да съберете пари?"
            decision = decision_menu(screen, message, [["Ипотекиране на собственост", (300, 300),(100, 50)], ["Продаване на къща",(450, 300), (100, 50)], ["Отказ",(600, 300), (100, 50)]], game)
            #("Trade with Player", (600, 590), (200, 50)) -> to add
            #sell hotel
            if decision == "Отказ":
                break
            elif decision == "Ипотекиране на собственост":
                raised += self.handle_mortage(screen, game)
            elif decision == "Продаване на къща":
                raised += self.handle_mortage(screen, game)
           # elif decision == "Declare Bankruptcy":#or when we catn pay???? in the prev func
             #   pass#bankrupcy = true
        return raised
    
    def needs_to_pay(self, amount, screen, game, creditor=None):
        if self.money >= amount:
            self.money -= amount
            if creditor:
                creditor.recieve_money(screen, game, amount)
            return True
        raised = self.try_to_raise_money(amount, screen, game)
        visualise(screen, game)
        message = f"Събрани {raised} от {amount} нужни"
        display_message(screen, game.font, 500, 40, message)
        while raised < amount:
            visualise(screen, game)
            message = f"Събрани {raised} от {amount} нужни"
            buttons = [["Съберете още", (300, 300),(100, 50)],  ["Банкрутирайте",(400, 300), (100, 50)]]
            dec = decision_menu(screen, message, buttons, game)
            if dec == "Съберете още":
                raised += self.try_to_raise_money(amount, screen, game)
            elif dec == "Банкрутирайте":
                self.declare_bankruptcy(screen, game, creditor)
                return False
        #success
        self.money -= amount
        if creditor:
            creditor.recieve_money(screen, game, amount)
        message = f"Честито! Събрахте {raised} от {amount} нужни"
        display_message(screen, game.font, 500, 40, message)
        pg.display.update()
        pg.time.wait(2000)
        return True
    
    #only in some functions go bankrupt so we wont offer here
    def pay_amount(self, amount, screen, game):
        if self.money >= amount:
            self.money -= amount
            return True
        raised = self.try_to_raise_money(amount, screen, game)

        visualise(screen, game)
        message = f"Събрани {raised} от {amount} нужни"
        display_message(screen, game.font, 500, 40, message)

        while raised < amount:
            visualise(screen, game)
            message = f"Събрани {raised} от {amount} нужни"
            buttons = [["Съберете още", (300, 300),(100, 50)],  ["Отказ",(400, 300), (100, 50)]]
            dec = decision_menu(screen, message, buttons, game)
            if dec == "Съберете още":
                raised += self.try_to_raise_money(amount, screen, game)
            elif dec == "Отказ":
                return False
        return True
    
    def gain_property(self, property):
        self.properties.append(property)