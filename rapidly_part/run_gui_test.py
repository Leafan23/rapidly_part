import rapidly_part.GUI
import rapidly_part.serialization
from rapidly_part.models import PartData, Dimension, Deviation

if __name__ == "__main__":
    # 1. Фейковые габариты (как будто из Kompas)
    gabarit = ["100,5", "50", "20"]

    # 2. Тестовые данные (парсим дефолтную строку)
    part_data = rapidly_part.serialization.parse_part_data(rapidly_part.serialization.DEFAULT_DATA_STRING)

    # (Опционально) Вы можете вручную добавить размер с допуском, чтобы проверить,
    # как он выглядит в полях ввода:
    part_data.dimensions[0] = Dimension(
        visible=True,
        prefix="L = ",
        value=100.5,
        it_grade="h14",
        upper_dev=Deviation(0.1, '+'),
        lower_dev=Deviation(0.1, '-')
    )

    # 3. Запускаем GUI
    app = rapidly_part.GUI.App(gabarit, part_data)
    app.mainloop()

    # 4. Смотрим результат после закрытия
    if app.result is not None:
        print("\n=== Результат (нажата кнопка 'БЧ деталь') ===")
        print(f"Показывать квалитет: {app.result.show_it_grade}")
        print(f"Показывать допуск: {app.result.show_tolerance}")
        print(f"Обработка торцов: {app.result.end_processing} ({app.result.end_processing_value})")
        for i, dim in enumerate(app.result.dimensions):
            print(f"Размер {i+1}: {dim.prefix}{dim.value_str} {dim.it_grade} {dim.upper_dev} {dim.lower_dev}")
    else:
        print("\n=== Нажата кнопка 'Чертежная деталь' (result = None) ===")