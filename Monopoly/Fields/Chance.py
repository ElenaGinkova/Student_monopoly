from Fields import Field
from Button import decision_menu
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
        decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
        decision_menu(game.screen, f"You win {self.money}!", [["Ok", (300, 370), (150, 50)]], game)
        game.get_player().recieve_money(game.screen, game, self.money)


class CardLoseMoney(Card):
    def __init__(self, text, money):
        super().__init__(text)
        self.money = money

    def action(self, game):
        decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
        decision_menu(game.screen, f"You lose {self.money}!", [["Ok", (300, 370), (150, 50)]], game)
        game.get_player().needs_to_pay(self.money, game.screen, game)


class CardMoveForward(Card):
    def __init__(self, text, field):
        super().__init__(text)
        self.field = field

    def action(self, game):
        decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
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
        decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
        #game.send_to_jail(game.get_player())


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


#Пробвай се
class Chance(Field):
    CARDS = [
             CardWinMoney("Банката ви връща надвзети данъци. Вземете $200!", 200),
             CardWinMoney("Продадохте стари акции с печалба. Вземете $150!", 150),
             CardWinMoney("Спечелихте от лотарията! Вземете $100!", 100),
             CardWinMoney("Вашето имущество се увеличава. Вземете $50!", 50),

             CardLoseMoney("Платете глоба за неправилно паркиране. Дължите $50!", 50),
             CardLoseMoney("Платете данъци върху имотите си. Дължите $100!", 100),
             CardPayPerHouseHotel("Извънреден ремонт на имоти! Платете $25 за всяка къща и $100 за всеки хотел!", 25, 100),

             CardPayAllPlayers("Платете на всички играчи по $50 за вашето празненство!", 50),

             CardMoveForward("Напреднете до СТАРТ и вземете $200!", 0),
             CardMoveForward("Напреднете до следващата жп станция. Ако е свободна, може да я купите. Ако не - плащате наема!", "next_station"),
             CardMoveForward("Напреднете до следващата електрическа или водна компания. Ако е свободна, може да я купите. Ако не - плащате такса!", "next_utility"),

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

