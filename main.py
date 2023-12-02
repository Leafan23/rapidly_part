# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import API
import GUI
from func import *


if __name__ == "__main__":
    kompas_api = API.KompasAPI()

    # Получение габаритных размеров
    gabarit_x, gabarit_y, gabarit_z = kompas_api.get_gabarit()
    gabarit = [dimension_to_string(gabarit_x), dimension_to_string(gabarit_y), dimension_to_string(gabarit_z)]

    app = GUI.App(gabarit)
    app.mainloop()
    if app.main_string[0] == 'БЧ':
        kompas_api.set_property('Форматы листов документа', 'БЧ')
        kompas_api.set_property('Примечание', smart_round(kompas_api.get_mass()/1000))
        part_name = to_drawing(kompas_api.get_property_value('Наименование'))
        temp_part_name = ''
        for i in app.main_string:
            if type(i) == list:
                print(i)
                temp_part_name += convert_data_to_string(i) + ' '
            print('Временное имя: ', temp_part_name)
        part_name += '@/' + kompas_api.get_property_value('Материал') + '@/' + temp_part_name
        print(part_name)
        kompas_api.set_property('Наименование', part_name)

    else:
        kompas_api.set_property('Форматы листов документа', '')
        kompas_api.set_property('Примечание', '')
        part_name = to_drawing(kompas_api.get_property_value('Наименование'))
        kompas_api.set_property('Наименование', part_name)
        print('Не БЧ')


