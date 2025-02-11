from FieldTypes.Fields import Field
from Button import decision_menu, display_message
import random
import pygame as pg


CARD_COUNT = 18


# to do to make them good visualisation card like
# add more cards
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
    def __init__(self, text, field_indx):
        super().__init__(text)
        self.field_indx = field_indx

    def action(self, game):
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)
        field = game.board.get_field_from_indx(self.field_indx)
        game.get_player().move(game, field, game.screen, game)
        field.action(game.screen, game)


class CardGoToJail(Card):
    def __init__(self, text):
        super().__init__(text)

    def action(self, game):
        mess = f"{self.text}"
        decision_menu(game.screen, mess, [["Ехх", (300, 370), (150, 50)]], game)
        game.go_to_jail()


class CardGetOutOfJailFree(Card):
    def __init__(self, text):
        super().__init__(text)

    def action(self, game):
        mess = f"{self.text} Вече можете да се отървате от жълтата книжка!"
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)
        game.get_player().add_out_of_j_card()


class CardPayPerHouseHotel(Card):
    def __init__(self, text, house_fee, hotel_fee):
        super().__init__(text)
        self.house_fee = house_fee
        self.hotel_fee = hotel_fee

    def action(self, game):
        player = game.get_player()
        house_count, hotel_count = player.get_propertries_count()
        house_cost = house_count * self.house_fee
        hotel_cost = hotel_count * self.hotel_fee
        mess = f"Трябва да платите {house_cost} за {house_count} къщи и {hotel_cost} за {hotel_count} хотели."
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)
        decision_menu(game.screen, mess, [["Плати", (300, 370), (150, 50)]], game)
        player.needs_to_pay(house_cost + hotel_cost, game.screen, game)


class CardNearestBus(Card):
    def __init__(self, text):
        super().__init__(text)

    def action(self, game):
        player = game.get_player()
        decision_menu(game.screen, self.text, [["Добре иди!", (300, 370), (150, 50)]], game)
        field = game.board.get_next_bus_field(player.pos_indx)
        player.move(field, game.screen, game)
        field.action(game.screen, game)


class CardPayAllPlayers(Card):
    def __init__(self, text, amount):
        super().__init__(text)
        self.amount = amount

    def action(self, game):
        decision_menu(game.screen, self.text, [["Добре", (300, 370), (150, 50)]], game)
        players = game.get_players().copy()
        player = game.get_player()
        players.remove(player)
        for pl in players:
            decision_menu(game.screen, f"Плати на {pl.get_name()}", [["Добре", (300, 370), (150, 50)]], game)
            succ = player.needs_to_pay(self.amount, game.screen, game, pl)
            if not succ:
                break


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
             CardPayPerHouseHotel("Платете $25 за всяка къща и $100 за всеки хотел!", 25, 100),
             CardLoseMoney("Крадци ограбиха вашата къща! Загубихте $200!", 200),
             CardLoseMoney("Вашата фирма банкрутира! Загубихте $400!", 400),

             CardPayAllPlayers("Платете на всички играчи по $50 за вашето празненство!", 50),

             CardMoveForward("Напреднете до ДЖОБНИ ОТ ДОМА и вземете $200!", 0),

             CardGoToJail("Идете в ЗАТВОРА! Не минавате през СТАРТ!"),

             CardGetOutOfJailFree("Излезте от ЗАТВОРА безплатно! (Задръжте тази карта)"),
             CardNearestBus("Напреднете до най-близката ЖП станция. Ако е свободна, може да я купите. Ако не - плащате наем!"),
             ]
    #CardMoveForward("Напреднете до следващата жп станция. Ако е свободна, може да я купите. Ако не - плащате наема!", "next_station"),
    #CardMoveBack("Взехте грешен самолетен билет! Преместете се 3 полета назад!", 3)

    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        card_num = random.randint(0, CARD_COUNT - 1)
        card = self.CARDS[card_num]
        card.action(game)


#to do
# class CardMoveBack(Card):
#     def __init__(self, text, spaces):
#         super().__init__(text)
#         self.spaces = spaces

#     def action(self, game):
#         decision_menu(game.screen, self.text, [["Ok", (300, 370), (150, 50)]], game)
#         game.get_player().move_back(game, self.spaces)