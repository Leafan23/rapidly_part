# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import API, GUI


class MainString:  # Класс главной строки
    def __init__(self, id):
        self.name = ""  # Наименование
        self.format = ""  # Формат листа
        self.note = ""  # Примечание
        self.sub_name = ""  # Обозначение

def dimension_to_string(dim):
    n = int(dim)
    print(int(n * 10) % 10, 'wqwqwqwqw')
    str(round(dim, 3))
    print(str(round(dim, 3)))

if __name__ == "__main__":
    kompas_api = API.KompasAPI()

    # Получение габаритных размеров
    gabarit_x, gabarit_y, gabarit_z,  = kompas_api.get_gabarit()
    gabarit = [str(round(gabarit_x, 3)), str(round(gabarit_y, 3)), str(round(gabarit_z, 3))]

    print(kompas_api.get_mass())  # Заменить на запись свойства в примечание
    print(kompas_api.get_property_value("Наименование"))  # Значение свойства поз. 1
    dimension_to_string(gabarit_x)
    app = GUI.App(gabarit)
    app.mainloop()
    print('End')


