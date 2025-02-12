import pygame as pg
from Button import Button

class Menu:
    def __init__(self, x, y):
        x, y = 10, 10
        icon_button = Button(text="≡", position=(10, 10), size=(40, 40), color=(150, 150, 150))
        option1 = Button(text="Опция 1", position=(20, 60), size=(160, 40), color=(0, 128, 255))
        option2 = Button(text="Опция 2", position=(20, 110), size=(160, 40), color=(0, 128, 255))
        option3 = Button(text="Опция 3", position=(20, 160), size=(160, 40), color=(0, 128, 255))

        option1.callback = lambda: option_callback("Опция 1")
        option2.callback = lambda: option_callback("Опция 2")
        option3.callback = lambda: option_callback("Опция 3")
        option_buttons = [option1, option2, option3]
        expanded_size=(200, 250)

        self.x = x
        self.y = y
        self.icon_button = icon_button      # Иконата, показвана когато менюто е затворено
        self.option_buttons = option_buttons  # Опциите, показвани когато менюто е отворено
        self.expanded_rect = pg.Rect(x, y, expanded_size[0], expanded_size[1])
        self.expanded = False  # Начално състояние – менюто е затворено

    def draw(self, screen):
        if self.expanded:
            # Рисуваме фон за разширеното меню (по желание)
            pg.draw.rect(screen, (220, 220, 220), self.expanded_rect)
            # Рисуваме бутоните за опциите
            for button in self.option_buttons:
                button.draw(screen)
        else:
            # Рисуваме само иконата
            self.icon_button.draw(screen)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.expanded:
                # Ако менюто е разширено, проверяваме дали сме кликнали върху някой от бутоните
                for button in self.option_buttons:
                    if button.is_clicked(event):
                        # Ако бутонът има зададена callback функция, я извикваме
                        if hasattr(button, 'callback') and callable(button.callback):
                            button.callback()
                        self.expanded = False  # Затваряме менюто след избор на опция
                        return
                # Ако кликнем извън разширеното меню, го затваряме
                if not self.expanded_rect.collidepoint(event.pos):
                    self.expanded = False
            else:
                # Ако менюто е затворено, проверяваме дали е кликната иконата
                if self.icon_button.is_clicked(event):
                    self.expanded = True




# -------------------------------
# Примерна callback функция за опциите
# -------------------------------
def option_callback(option):
    print(f"Избрана опция: {option}")
 
def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Меню с иконка и разширени опции")
    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            menu.handle_event(event)

        screen.fill((0, 100, 0))
        menu.draw(screen)

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    main()
