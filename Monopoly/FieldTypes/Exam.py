from ..FieldTypes.Fields import Field
from ..Visualisations import decision_menu
import pygame as pg
import random


QUESTIONS = [
    "Ако не пиеш кафе можеш да оцелееш?",
    "Числото 561 е просто число?",
    "На две взаимно прости числа то най-големият им общ делител е 1?",
    "Сумата от ъглите във всеки четириъгълник е 360 градуса?",
    "Ако дадена функция има производна, то тя е непрекъсната?",
    "5 книги могат да се наредят по 120 начина?",
    "Ако хвърлим монета 10 пъти, ще получим 5 ези и 5 тура?",
    "В Python list.append(x) добавя елемент x в началото на списъка?",
    "В Python None и False са едно и също нещо?",
    "В Python is и == винаги дават еднакви резултати?",
    "Алгоритъмът на Дейкстра може да работи с отрицателни тегла?",
    "В Python всички класове наследяват object?",
    "В Python можем да заменим (+, -, *) чрез методи като __add__()?",
    "В Python tuple може да бъде променян след създаването му?",
    "Python поддържа множествено наследяване?",
    "В Python можеш да върнеш повече от една стойност от функция?",
    "Python използва garbage collector за управление на паметта?",
    "Python винаги копира списъци при присвояване (list2 = list1)?"
]


ANSWERS = [
    "Да",   
    "Не",  
    "Да",  
    "Да",  
    "Да",  
    "Да",  
    "Не",  
    "Не",  
    "Не",  
    "Не",  
    "Не",  
    "Да",  
    "Да",  
    "Не",  
    "Да",  
    "Да",  
    "Да",  
    "Не"   
]


EXPLANATIONS = [
    "Просто е по-трудно!",
    "561 = 3 × 11 × 17.",
    "Нямат общи делители освен 1.",
    "Сумата на ъглите е 360 градуса.",
    "Ако функцията е диференцируема, тя е непрекъсната.",
    "5! = 120 различни варианта.",
    "Най-вероятният резултат е, но не гарантиран.",
    "Методът добавя в края на списъка.",
    "None означава липса на стойност.",
    "is сравнява по референция, докато == сравнява стойности.",
    "Дейкстра може да даде грешни резултати тогава.",
    "Всички класове в Python наследяват object.",
    "Позволява презаписване на оператори.",
    "Tuple в Python са неизменяеми.",
    "Един клас може да наследява повече от един родител.",
    "Функция връща няколко стойности, като ги групира в tuple.",
    "Garbage collector освобождава неизползваната памет.",
    "list2 = list1 закача референция"
]


QESTION_COUNT = 18


class Exam(Field):
    def __init__(self, indx, name, position):
        super().__init__(indx, name, position)

    def action(self, screen, game):
        question_indx = random.randint(0, QESTION_COUNT - 1)
        dec = decision_menu(game.screen, QUESTIONS[question_indx], [["Да", (300, 370), (150, 50)], ["Не", (600, 370), (150, 50)]], game)
        if dec == ANSWERS[question_indx]:
            mess = f"Браво! Правилен отговор! Взе изпита! + 10 живот."
            game.get_player().change_life(10, game)
            decision_menu(game.screen, mess, [["Супер", (300, 370), (150, 50)]], game)
        else:
            decision_menu(game.screen, f"Отговор: {ANSWERS[question_indx]} {EXPLANATIONS[question_indx]}", [["Добре", (300, 370), (150, 50)]], game)
            mess = f"Скъсаха те! - 10 живот."
            game.get_player().change_life(-10, game)
            decision_menu(game.screen, mess, [["Ужас", (300, 370), (150, 50)]], game)