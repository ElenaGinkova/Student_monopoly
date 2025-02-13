import pygame as pg
from Visualisations import visualise, decision_menu, display_message, GREEN_COLOR
import sys


LIFE = 100
MONEY = 0
START_POSITION = [1000, 600]
FIELD_COUNT = 34
GO_MONEY = 200
SPRITE_SCALE = (80, 130) # Resize all sprites to 100x100
HIGTH = 100
SCREEN_COLOR = (30, 30, 30)
BACKGROUND = pg.image.load('Monopoly/assets/BoardUNI.png')
BACKGROUND = pg.transform.smoothscale(BACKGROUND, (1100, 600))
COLOR_GROUP_COUNT = [2,2,2,2,2,2,2,1,4]


class Player():
    def __init__(self, name, image_p):
        self.name = name
        self.image_p = image_p
        self.image = pg.image.load(image_p)
        w = self.width
        self.image = pg.transform.scale(self.image, (w, HIGTH))
        self.rect = self.image.get_rect()
        self.position = START_POSITION # starting position
        self.money = MONEY # the starting amount of money
        self.life = LIFE
        self.properties = []
        self.pos_indx = 0
        self.jail = False
        self.active = True
        self.out_of_jail_card = 0
        self.jail_days = 0
        self.diploms = 0
        self.cooldown = 0
        self.reverse_moving = False
        self.mystery_shots = 0
        self.used_power = False
        self.reserved_field = None# when we pass go we restart to none

    def get_reserve(self):
        return self.reserved_field
        
    def get_cooldown(self):
        return self.cooldown
    
    def get_name(self):
        return self.name
    
    def get_money(self):
        return self.money
    
    def get_properties(self):
        return self.properties
    
    def get_life(self):
        return self.life
    
    def get_propertries_count(self):
        house_count = 0
        hotel_count = 0
        for pr in self.properties:
            house_count += pr.get_house_count()
            if pr.has_hotel():
                hotel_count += 1
        return house_count, hotel_count
    
    def get_pos_indx(self):
        return self.pos_indx
    
    def has_diploma(self):
        return self.diploms
    
    def has_mystery_shots(self):
        return self.mystery_shots != 0
    
    def has_color_group(self, group_i):
        count = self.count_color_group(group_i)
        return count == COLOR_GROUP_COUNT[group_i - 1]
    
    def has_diploms(self):
        return self.diploms

    def has_what_to_mortage(self):
        for pr in self.properties:
            if pr.can_it_be_mortaged():
                return True
        return False
    
    def has_what_to_unmortage(self):
        for pr in self.properties:
            if pr.is_mortage():
                return True
        return False

    def has_houses(self):
        for pr in self.properties:
            if pr.has_houses():
                return True
        return False

    def has_out_of_jail_card(self):
        return self.out_of_jail_card
    
    def has_power(self):
        return not self.used_power
    
    def use_diploma(self):
        self.diploms -= 1

    def use_mystery_shot(self):
        self.mystery_shots -= 1
    
    def reset_power(self):
        if self.used_power:
            self.power_cooldown -= 1
            if self.power_cooldown <= 0:
                self.used_power = False

    def use_power(self):
        self.power_cooldown = 3
        self.used_power = True

    def reverse_move(self):
        self.reverse_moving = not self.reverse_moving

    def count_color_group(self, group_i):
        count = 0
        for pr in self.properties:
            if pr.color_group == group_i:
                count += 1
        return count
    
    def cool_down(self):
        self.cooldown = 2
    
    def reduce_cooldown(self):
        self.cooldown -= 1
    
    def change_life(self, points, game):
        if self.life == 100 and points > 0: # max life
            return
        self.life += points
        if self.life <= 0:
            self.eliminate(game)

    def eliminate(self, game):
        mess = f"{self.name} - Животът ви свърши! Край на играта за вас!"
        decision_menu(game.screen, mess, [["Добре", (300, 370), (150, 50)]], game)
        self.active = False
        game.eliminate(self)

    def recieve_money(self, screen, game, money):
        visualise(screen, game)
        message = f"{self.name} получи {money}лв.!"
        self.money += money
        display_message(screen, game.font, 500, 40, message)
        pg.display.update()
        pg.time.wait(2000)

    def can_pay(self, amount):
        return self.money >= amount
    
    def recieve_diploma(self):
        self.diploms += 1
    
    def add_out_of_j_card(self):
        self.out_of_jail_card += 1

    @property
    def is_in_jail(self):
        return self.jail
    
    def free_from_jail(self):
        self.jail = False
        
    def go_to_jail(self):
        self.jail = True
        self.jail_days = 0
        
    def day_in_jail(self):
        self.jail_days += 1
        if self.jail_days == 3:
            self.jail = False

    def move(self, field, screen, game):
        self.position = field.get_position()
        next_indx = field.get_indx()
        if self.reserved_field:
            if self.pos_indx > next_indx or (self.pos_indx < self.reserved_field.get_indx() and next_indx > self.reserved_field.indx):
                self.reserved_field.free()
                self.reserved_field = None
                display_message(screen, game.font, 500, 40, "Резервацията е анулирана")
                pg.display.flip()
                pg.time.wait(2000)
        self.pos_indx = next_indx
        visualise(screen, game)

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

    def buy_property(self, property, screen, game):
        if self.money >= property.get_price():
            self.money -= property.get_price()
            self.properties.append(property)
            property.owner = self
            message = f"Успешно закупихте {property.get_name()}"
            display_message(screen, game.font, 500, 40, message)
            return True
        buttons = [["Съберете пари", (200, 300), (200, 50)], ["Не купувайте", (450, 300), (150, 50)]]
        message = "Искате ли да съберете пари?"
        visualise(screen, game)
        dec = decision_menu(screen, message, buttons, game)
        if dec == "Съберете пари":
            raised = self.try_to_raise_money(property.get_price(), screen, game)
            if raised + self.money >= property.get_price():
                dec = decision_menu(screen, "Плащате ли?", [["Да", (200, 300), (150, 50)], ["Не", (450, 300), (150, 50)]], game)
                if dec == "Да":
                    return self.buy_property(property, screen, game)
                else:
                    return False
            else:
                return self.buy_property(property, screen, game)
        elif dec == "Не купувайте":
            return False
        return False  # Default return if no valid action is taken
    
    def buy_reserved(self, game):
        if self.reserved_field:
            if self.buy_property(self.reserved_field, game.screen, game):
                self.reserved_field.free()
                self.reserved_field = None
        else:
            display_message(game.screen, game.font, 500, 40, "Нямате резерве")
            pg.display.flip()
            pg.time.wait(1000)

    def try_to_raise_money(self, amount, screen, game):
        raised = 0
        while self.money < amount:
            message = f"{self.name}, как искате да съберете пари?"
            decision = decision_menu(screen, message, [["Ипотекиране на собственост", (200, 300),(300, 50)], ["Продаване на къща",(550, 300), (200, 50)], ["Отказ",(800, 300), (100, 50)]], game)
            #("Trade with Player", (600, 590), (200, 50)) -> to add
            #sell hotel
            if decision == "Отказ":
                break
            elif decision == "Ипотекиране на собственост":
                raised += self.handle_mortage(screen, game)
            else:
                raised += self.handle_sell_house(screen, game)
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
        while raised + self.money < amount:
            visualise(screen, game)
            message = f"Налични {raised + self.money} от {amount} нужни"
            buttons = [["Съберете още", (300, 300),(150, 50)],  ["Банкрутирайте",(500, 300), (150, 50)]]
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
            buttons = [["Съберете още", (200, 300),(150, 50)],  ["Отказ",(450, 300), (150, 50)]]
            dec = decision_menu(screen, message, buttons, game)
            if dec == "Съберете още":
                raised += self.try_to_raise_money(amount, screen, game)
            elif dec == "Отказ":
                return False
        return True

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
            for property in self.properties:
                property.owner = None  # Reset ownership
        self.active = False  # Flag for elimination
        game.remove_player(self)
        return False

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
                buttons.append([prop.get_name(), (x, y), (150, 50)])
                names_map[prop.name] = prop
                x += 150
            buttons.append(["Отказ", (700, 400), (100, 50)])
            decision = decision_menu(screen, message, buttons, game)
            if decision == "Отказ":
                return False
            to_mortage = names_map[decision]
            money = to_mortage.get_mortage_money()
            message = f"Получихте {money}лв.!"
            display_message(screen, game.font, 500, 40, message)
            self.money += money
        else:
            message = f"Нямате какво да ипотекирате!"
            display_message(screen, game.font, 500, 40, message)
        pg.display.update()
        pg.time.wait(1000) # 1 sec
        return money

    def handle_unmortage(self, screen, game):
        if self.has_what_to_unmortage():
            visualise(screen, game)
            message = f"Какво искате да ипотекирате?"
            mortaged = [prop for prop in self.properties if prop.is_mortage()]
            names_map = {}
            buttons = []
            x = 200
            y = 300
            for prop in mortaged:
                if x > 800:
                    x = 200
                    y = 400
                buttons.append([prop.get_name(), (x, y), (150, 50)])
                names_map[prop.get_name()] = prop
                x += 150
            buttons.append(["Отказ", (700, 400), (100, 50)])
            decision = decision_menu(screen, message, buttons, game)
            if decision == "Отказ":
                return
            to_unmortage = names_map[decision]
            to_pay = to_unmortage.unmortage_price()
            message = f"Платете {to_pay}лв.!"
            dec = decision_menu(screen, message, [["Добре", (200, 300),(300, 50)], ["Отказ",(550, 300), (200, 50)]], game)
            if dec == "Добре":
                if game.get_player().pay_amount(to_pay, screen, game):
                    dec = decision_menu(screen, "Успешно отипотекирахте", [["Добре", (200, 300),(300, 50)]], game)
                    to_unmortage.unmortage()
                    return
            dec = decision_menu(screen, "Неуспешно отипотекиране", [["Добре", (200, 300),(150, 50)]], game)
        else:
            message = f"Нямате какво да отипотекирате!"
            display_message(screen, game.font, 500, 40, message)
        pg.display.update()
        pg.time.wait(1000) # 1 sec

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
        pg.display.update()
        pg.time.wait(2000) # 2 sec
        return money
    
    def gain_property(self, property):
        self.properties.append(property)