# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import API
import GUI


class MainString:  # Класс главной строки
    def __init__(self, id):
        self.name = ""  # Наименование
        self.format = ""  # Формат листа
        self.note = ""  # Примечание
        self.sub_name = ""  # Обозначение


def dimension_to_string(dim):  # Преобразование Float размера в string с округленным значением и ',' вместо '.'
    string = str(round(dim, 3)).replace(".", ",")
    if string[-2:] == ',0':
        string = string[:-2]
        return string
    return string


def smart_round(part_mass):
    if part_mass < 0.1:
        part_mass *= 1000
        return replacer(round(part_mass, 1)) + " г"
    elif 0.1 <= part_mass <= 10:
        return replacer(round(part_mass, 2)) + " кг"
    elif 10 <= part_mass <= 100:
        return replacer(round(part_mass, 1)) + " кг"
    else:
        return replacer(round(part_mass, 0)) + " кг"


def replacer(number):
    return str(number).replace('.', ',')


if __name__ == "__main__":
    kompas_api = API.KompasAPI()

    # Получение габаритных размеров
    gabarit_x, gabarit_y, gabarit_z = kompas_api.get_gabarit()
    gabarit = [dimension_to_string(gabarit_x), dimension_to_string(gabarit_y), dimension_to_string(gabarit_z)]

    print(kompas_api.get_mass())  # Заменить на запись свойства в примечание
    print(kompas_api.get_property_value("Наименование"))  # Значение свойства поз. 1
    kompas_api.set_property("Наименование", '123')
    app = GUI.App(gabarit)
    app.mainloop()


