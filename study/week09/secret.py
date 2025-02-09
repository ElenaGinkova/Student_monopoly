class RuinedNikuldenDinnerError(Exception):
    pass


def validate_recipe(filename):
    
    # Списък на специалните думи, които се търсят в текста
    special_words = ['риба', 'рибена', 'шаран', 'сьонга']

    try:
        # Опит за отваряне и четене на файла
        with open(filename, 'r', encoding='utf-8') as file:
            # Четене на цялото съдържание на файла и преобразуване в малки букви
            content = file.read().lower()

            # Проверка дали някоя от специалните думи се съдържа в текста
            for word in special_words:
                if word in content:
                    return True  # Ако е намерена поне една дума, връща True

            return False  # Ако никоя дума не е намерена, връща False

    except (OSError, IOError):
        # Хвърляне на специфична грешка, ако има проблем с отварянето на файла
        raise RuinedNikuldenDinnerError("Неуспешно четене на файла с рецепта.")