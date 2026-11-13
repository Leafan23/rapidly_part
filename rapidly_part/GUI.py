import customtkinter
from models import PartData, Dimension, Deviation
from serialization import parse_float, parse_deviation


class App(customtkinter.CTk):
    def __init__(self, gabarit: list[str], part_data: PartData):
        super().__init__()

        # Сохраняем данные
        self.part_data = part_data
        self.gabarit = gabarit

        # Сюда мы запишем результат при нажатии кнопки
        self.result: PartData | None = None

        self.title("Rapidly part")
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("blue")
        self.geometry("750x700")

        self.row = 6
        self.my_list = []
        self.i = 0

        # Чекбоксы инициализируем из part_data
        self.checkbox_1_check = customtkinter.BooleanVar(value=part_data.show_it_grade)
        self.tolerance_check = customtkinter.BooleanVar(value=part_data.show_tolerance)
        self.end_butt = customtkinter.BooleanVar(value=part_data.end_processing)
        self.end_butt_string = customtkinter.StringVar(value=part_data.end_processing_value)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="Показывать квалитет", variable=self.checkbox_1_check)
        self.checkbox_1.grid(row=1, column=3, padx=20, pady=(10, 20))

        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="Показывать допуск", variable=self.tolerance_check)
        self.checkbox_2.grid(row=1, column=4, padx=20, pady=(10, 20))

        self.checkbox_3 = customtkinter.CTkCheckBox(self, text="Обработка торцов", command=self.end_butt_func,
                                                    variable=self.end_butt)
        self.checkbox_3.grid(row=1, column=1, padx=20, pady=(10, 20))

        if self.end_butt.get():
            self.end_butt_func()

        self.field_add = customtkinter.CTkButton(self, text="Добавить размер", command=self.button_event)
        self.field_add.grid(row=self.row, column=0, padx=20, pady=20)

        self.field_delete = customtkinter.CTkButton(self, text="Убрать размер", command=self.button_event_delete,
                                                    state="disabled")
        self.field_delete.grid(row=self.row, column=1, padx=20, pady=20, sticky="we")

        self.button_send = customtkinter.CTkButton(self, text="Чертежная деталь", command=self.undo_button)
        self.button_send.grid(row=self.row + 4, column=3, padx=20, pady=20, sticky="w")

        self.button_send_bch = customtkinter.CTkButton(self, text="БЧ деталь", command=self.do_button,
                                                       fg_color="#ffa500", text_color="black")
        self.button_send_bch.grid(row=self.row + 4, column=4, padx=20, pady=20, sticky="w")

        # Добавляем поля для размеров, которые уже есть в part_data
        for dim in part_data.dimensions:
            if dim.visible:
                self.button_event(dim)

        self.version_lable = customtkinter.CTkLabel(self, text="v0.3(Build 18) 2024.01",
                                                    text_color=('gray60', 'gray30'))
        self.version_lable.grid(row=16, column=4, padx=20, pady=20, sticky="se")

    def do_button(self):
        """Собирает PartData и закрывает окно."""
        dims = [field.return_dim() for field in self.my_list]
        self.result = PartData(
            dimensions=dims,
            show_it_grade=self.checkbox_1.get(),
            show_tolerance=self.checkbox_2.get(),
            end_processing=self.checkbox_3.get(),
            end_processing_value=self.end_butt_string.get()
        )
        self.destroy()

    def undo_button(self):
        """Возвращает None (сигнал для main.py вернуть чертежную деталь)."""
        self.result = None
        self.destroy()

    def end_butt_func(self):
        if self.end_butt.get():
            self.entry_end_butt = customtkinter.CTkEntry(self, placeholder_text="Обработка торцов Ra 12,5",
                                                         textvariable=self.end_butt_string)
            self.entry_end_butt.grid(row=1, padx=20, pady=(10, 16))
        else:
            if hasattr(self, 'entry_end_butt'):
                self.entry_end_butt.destroy()

    def button_event(self, dim_data: Dimension | None = None):
        """Добавляет строку. Если передать dim_data, заполняет поля из неё."""
        new_field = DimensionField(master=self, gabarit=self.gabarit, dim=dim_data)
        self.my_list.append(new_field)
        new_field.grid(row=self.row, column=0, padx=20, pady=20, sticky="we", columnspan=5)

        self.i += 1
        self.row += 1
        self.field_add.grid(row=self.row + 1)
        self.field_delete.grid(row=self.row + 1)
        self.field_delete.configure(state="normal")
        if self.row > 8:
            self.field_add.configure(state="disabled")

    def button_event_delete(self):
        self.my_list[self.i - 1].destroy()
        self.my_list.pop(self.i - 1)
        self.i -= 1
        self.row -= 1
        self.field_add.grid(row=self.row + 1)
        self.field_delete.grid(row=self.row + 1)
        if self.row < 7:
            self.field_delete.configure(state="disabled")
        self.field_add.configure(state="normal")


class DimensionField(customtkinter.CTkFrame):
    def __init__(self, master, gabarit: list[str], dim: Dimension | None = None, **kwargs):
        super().__init__(master, **kwargs)

        self.dimension = []
        # Добавляем значение из сохраненных данных (если есть) в начало списка
        if dim and dim.value is not None:
            self.dimension.append(dim.value_str)
        # Добавляем габариты
        self.dimension.extend(gabarit)

        # 1. Поле префикса (например, "L = ")
        self.entry = customtkinter.CTkEntry(self, placeholder_text="L = ")
        if dim:
            self.entry.insert(0, dim.prefix)
        self.entry.grid(row=1, column=0, padx=20, sticky="w")

        # 2. Поле значения размера
        self.entry_2 = customtkinter.CTkComboBox(self, values=self.dimension)
        if dim:
            if dim.value is not None:
                self.entry_2.set(dim.value_str)
            else:
                self.entry_2.set('Размер')
        else:
            self.entry_2.set('Размер')
        self.entry_2.grid(row=1, column=1, padx=20, sticky="w")

        # 3. Кнопка квалитета
        it_grade = dim.it_grade if dim and dim.it_grade else 'Квалитет'
        self.button = customtkinter.CTkButton(self, text=it_grade, command=self.button_callback)
        self.button.grid(row=1, column=2, padx=20, pady=20, sticky="w")

        # 4. Поля допусков
        self.entry_3 = customtkinter.CTkEntry(self, placeholder_text="Верхний допуск")
        if dim and dim.upper_dev:
            self.entry_3.insert(0, str(dim.upper_dev))
        self.entry_3.grid(row=0, column=3, padx=20, sticky="w")

        self.entry_4 = customtkinter.CTkEntry(self, placeholder_text="Нижний допуск")
        if dim and dim.lower_dev:
            self.entry_4.insert(0, str(dim.lower_dev))
        self.entry_4.grid(row=2, column=3, padx=20, sticky="w")

    def button_callback(self):
        self.tolerance = Tolerance(self)

    def return_dim(self) -> Dimension:
        """Собирает данные из полей в объект Dimension."""
        if self.button._text == 'Квалитет':
            self.button.configure(text='')

        return Dimension(
            visible=True,
            prefix=self.entry.get(),
            value=parse_float(self.entry_2.get()),
            it_grade=self.button._text,
            upper_dev=parse_deviation(self.entry_3.get()),
            lower_dev=parse_deviation(self.entry_4.get())
        )

    def change_button_value(self, value):
        self.button.configure(text=value)


class Tolerance(customtkinter.CTkToplevel):
    # (Этот класс остался без изменений, я его не трогал)
    def __init__(self, master):
        super().__init__(master)
        self.title("Tolerance")
        self.geometry("+400+400")
        self.attributes("-topmost", True)
        self.row = 0
        self.toletance = ["n", "m", "k", "js", "h", "g", "f", "e", "d", "c"]
        self.x = ["n", "m", "k", "js", "h", "g", "f", "e", "d", "c"]

        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.add("Вал (h14)")
        self.tabview.add("Отверстие (H14)")
        self.tabview.grid(row=0, column=0, padx=0, pady=(0, 0), sticky="we")
        self.button, self.button1 = [], []

        for i in range(9):
            for k in range(len(self.toletance)):
                self.x[k] = self.toletance[k] + str(self.row + 9)
            self.button.append(customtkinter.CTkSegmentedButton(self.tabview.tab("Вал (h14)"),
                                                                width=50, corner_radius=0,
                                                                selected_hover_color=("red", "gray"),
                                                                selected_color=("red", "#4c4a48"),
                                                                values=self.x,
                                                                command=self.segmented_button_callback))
            for z in range(len(self.x)):
                self.x[z] = self.x[z].upper()
            self.button1.append(customtkinter.CTkSegmentedButton(self.tabview.tab("Отверстие (H14)"),
                                                                 corner_radius=0,
                                                                 selected_hover_color=("red", "gray"),
                                                                 selected_color=("red", "#4c4a48"),
                                                                 values=self.x,
                                                                 command=self.segmented_button_callback))
            self.button[self.row].grid(row=self.row, column=1, padx=0, pady=0)
            self.button1[self.row].grid(row=self.row, column=1, padx=0, pady=0)
            self.row += 1

    def segmented_button_callback(self, value):
        self.destroy()
        self.master.change_button_value(value)
        self.master.master.checkbox_1.select()

if __name__ == '__main__':
    windows = App()