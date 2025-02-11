from FieldTypes.Property import Property
from Button import decision_menu
import pygame as pg


class BusProperty(Property):
    def __init__(self, indx, name, position, price, color_group, owner = None):
        super().__init__(indx, name, position, price, color_group, owner)

    def rent(self, screen, game):
        count = self.owner.count_color_group(9)
        return 25 * count