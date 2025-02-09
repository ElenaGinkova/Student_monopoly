from Fields import Field
from Button import decision_menu, display_message
from random import random
import pygame as pg


CARD_COUNT = 30


class Card:
    def __init__(self, text):
        self.text = text


class CardWinMoney(Card):
    def __init__(self, text, money):
        super().__init__(text)
        self.money = money
    
    def action(self, game):
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)
        decision_menu(game.screen, f"Печелите {self.money}!", [["Добре", (300, 370), (150, 50)]], game)
        game.get_player().recieve_money(game.screen, game, self.money)


class CardLoseMoney(Card):
    def __init__(self, text, money):
        super().__init__(text)
        self.money = money

    def action(self, game):
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)
        decision_menu(game.screen, f"Губите {self.money}!", [["Добре", (300, 370), (150, 50)]], game)
        game.get_player().needs_to_pay(self.money, game.screen, game)


class CardMoveForward(Card):
    def __init__(self, text, field):
        super().__init__(text)
        self.field = field

    def action(self, game):
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)
        game.get_player().move(game, self.field, game.screen, game)
        self.field.action(game.screen, game)


#to do
# class CardMoveBack(Card):
#     def __init__(self, text, spaces):
#         super().__init__(text)
#         self.spaces = spaces

#     def action(self, game):
#         decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
#         game.get_player().move_back(game, self.spaces)


#to do
class CardGoToJail(Card):
    def __init__(self, text):
        super().__init__(text)

    def action(self, game):
        display_message(self.screen, self.font,500,50,"Беше ви връчена жълта книжка!")
        pg.display.update()
        pg.time.wait(2000)
        game.go_to_jail()



# to do
class CardGetOutOfJailFree(Card):
    def __init__(self, text):
        super().__init__(text)

    def action(self, game):
        decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
        game.get_player().add_get_out_of_jail_card(self)


#to do
class CardPayPerHouseHotel(Card):
    def __init__(self, text, house_fee, hotel_fee):
        super().__init__(text)
        self.house_fee = house_fee
        self.hotel_fee = hotel_fee

    def action(self, game):
        player = game.get_player()
        total_cost = (player.count_houses() * self.house_fee) + (player.count_hotels() * self.hotel_fee)
        decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
        decision_menu(game.screen, f"You owe ${total_cost}!", [["Ok", (300, 370), (150, 50)]], game)
        player.pay_money(game.screen, game, total_cost)


#to do
class CardNearestRailroad(Card):
    def __init__(self, text):
        super().__init__(text)

    def action(self, game):
        decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
        game.get_player().move_to_next_railroad(game)



#to do
class CardPayAllPlayers(Card):
    def __init__(self, text, amount):
        super().__init__(text)
        self.amount = amount

    def action(self, game):
        decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
        game.get_player().pay_all_players(game, self.amount)


#Пробвай се - преработи, добави
class Chance(Field):
    CARDS = [
             CardWinMoney("Банката ви връща надвзети данъци. Вземете $200!", 200),
             CardWinMoney("Продадохте стари акции с печалба. Вземете $150!", 150),
             CardWinMoney("Спечелихте от лотарията! Вземете $100!", 100),
             CardWinMoney("Вашето имущество се увеличава. Вземете $50!", 50),
             CardWinMoney("Участвахте в риалити шоу и спечелихте! Вземете $500!", 500),
             CardWinMoney("Вашите акции скочиха! Вземете $300!", 300),
             CardWinMoney("Получавате бонус за лоялен клиент в банката. Вземете $250!", 250),
             CardWinMoney("Спечелихте спортен турнир! Вземете $200!", 200),

             CardLoseMoney("Платете глоба за неправилно паркиране. Дължите $50!", 50),
             CardLoseMoney("Платете данъци върху имотите си. Дължите $100!", 100),
             CardPayPerHouseHotel("Извънреден ремонт на имоти! Платете $25 за всяка къща и $100 за всеки хотел!", 25, 100),
             CardLoseMoney("Крадци ограбиха вашата къща! Загубихте $200!", 200),
             CardLoseMoney("Вашата фирма банкрутира! Загубихте $400!", 400),

             CardPayAllPlayers("Платете на всички играчи по $50 за вашето празненство!", 50),

             CardMoveForward("Напреднете до ДЖОБНИ ОТ ДОМА и вземете $200!", 0),
             #CardMoveForward("Напреднете до следващата жп станция. Ако е свободна, може да я купите. Ако не - плащате наема!", "next_station"),
             #CardMoveBack("Взехте грешен самолетен билет! Преместете се 3 полета назад!", 3),

             CardGoToJail("Идете в ЗАТВОРА! Не минавате през СТАРТ!"),

             CardGetOutOfJailFree("Излезте от ЗАТВОРА безплатно! (Задръжте тази карта)"),
             CardNearestRailroad("Напреднете до най-близката ЖП станция. Ако е свободна, може да я купите. Ако не - плащате наем!"),
             ]
    
    def __init__(self, indx, name, position, action):
        super().__init__(indx, name, position, action)

    def action(self, game):
        card_num = random.randint(0, CARD_COUNT - 1)
        card = self.CARDS[card_num]
        card.action(game)

