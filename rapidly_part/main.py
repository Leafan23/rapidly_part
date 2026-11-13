import API
import GUI
import serialization
from models import PartData, format_number
from formatting import format_dimension, format_mass, to_drawing

PROPERTY_NAME = r'property_for_rapidly_part'

if __name__ == "__main__":
    kompas_api = API.KompasAPI()

    if kompas_api.check_part():
        # 1. Получаем габариты (используем format_number вместо dimension_to_string)
        gx, gy, gz = kompas_api.get_gabarit()
        gabarit = [format_number(gx), format_number(gy), format_number(gz)]

        # 2. Читаем сохраненные данные
        stored_data = kompas_api.get_property_value(PROPERTY_NAME)
        name_prop = kompas_api.get_property_value('Наименование')

        # 3. Определяем, откуда брать PartData
        if stored_data:
            part_data = serialization.parse_part_data(stored_data)
        elif name_prop and '@/' in name_prop:
            part_data = serialization.parse_name_property(name_prop)
            part_data.show_it_grade = True
            part_data.show_tolerance = True
        else:
            part_data = serialization.parse_part_data("")
            kompas_api.add_property(PROPERTY_NAME)

        # 4. Запуск GUI
        app = GUI.App(gabarit, part_data)
        app.mainloop()

        # 5. Обработка результата
        if app.result is not None:
            result_data = app.result

            kompas_api.set_property('Форматы листов документа', 'БЧ')
            # Используем format_mass вместо smart_round
            kompas_api.set_property('Примечание', format_mass(kompas_api.get_mass() / 1000))

            part_name = to_drawing(kompas_api.get_property_value('Наименование'))
            material = kompas_api.get_property_value('Материал')
            part_name += '@/' + material

            dims_str_list = []
            for dim in result_data.dimensions:
                if dim.visible:
                    formatted_dim = format_dimension(dim, result_data.show_it_grade, result_data.show_tolerance)
                    if formatted_dim.strip():
                        dims_str_list.append(formatted_dim)

            if dims_str_list:
                part_name += '@/' + ' '.join(dims_str_list)

            if result_data.end_processing:
                part_name += '@/' + 'Обработка торцов ' + '@+171~ ' + result_data.end_processing_value

            kompas_api.set_property('Наименование', part_name)
            kompas_api.set_property(PROPERTY_NAME, serialization.serialize_part_data(result_data))

        else:
            # Пользователь нажал "Чертежная деталь"
            kompas_api.set_property('Форматы листов документа', '')
            kompas_api.set_property('Примечание', '')
            part_name = to_drawing(kompas_api.get_property_value('Наименование'))
            kompas_api.set_property('Наименование', part_name)