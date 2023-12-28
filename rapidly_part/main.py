# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import API
import GUI
from func import *


if __name__ == "__main__":
    # Подключение к API компаса
    kompas_api = API.KompasAPI()

    # Проверка документа на деталь
    if kompas_api.check_part():
        # Получение габаритных размеров
        gabarit_x, gabarit_y, gabarit_z = kompas_api.get_gabarit()
        gabarit = [dimension_to_string(gabarit_x), dimension_to_string(gabarit_y), dimension_to_string(gabarit_z)]

        # Прочитать данные с документа
        if kompas_api.get_property_value(r'property_for_rapidly_part') == False:
            data = r'False$Ra 12,5$False$True$L = $$Квалитет$$$H = $$Квалитет$$$W = $$Квалитет$$$'
            kompas_api.add_property(r'property_for_rapidly_part')
            kompas_api.set_property(r'property_for_rapidly_part', data)
        else:
            data = kompas_api.get_property_value(r'property_for_rapidly_part')

        # Запуск графического приложения
        app = GUI.App(gabarit, data)
        app.mainloop()

        # Обработка введенных значений и запись данных в компас
        if app.main_string != [] and app.main_string[0] == 'БЧ':
            kompas_api.set_property('Форматы листов документа', 'БЧ')
            kompas_api.set_property('Примечание', smart_round(kompas_api.get_mass()/1000))
            part_name = to_drawing(kompas_api.get_property_value('Наименование'))
            temp_part_name = ''
            it_flag = app.main_string[-3]
            tolerance_flag = app.main_string[-2]
            for i in app.main_string:
                if type(i) == list:
                    temp_part_name += convert_data_to_string(i, it_flag, tolerance_flag) + ' '
            part_name += '@/' + kompas_api.get_property_value('Материал') + '@/' + temp_part_name
            if app.main_string[-1] == 1:
                part_name = part_name + '@/' + 'Обработка торцов ' + '@+171~ ' + app.end_butt_string.get()
            kompas_api.set_property('Наименование', part_name)
            #m = app.main_string
            #m.extend(app.main_string[1])
            #s = app.end_butt_string.get()
            s = data_convert(app.main_string, app.end_butt_string.get())
            print(s)
            print(app.main_string, app.end_butt_string.get())
        elif app.main_string != [] and app.main_string[0] == '':
            kompas_api.set_property('Форматы листов документа', '')
            kompas_api.set_property('Примечание', '')
            part_name = to_drawing(kompas_api.get_property_value('Наименование'))
            kompas_api.set_property('Наименование', part_name)


