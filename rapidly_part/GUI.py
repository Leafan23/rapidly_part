import customtkinter


class App(customtkinter.CTk):  # Main window of app
    def __init__(self, gabarit=' '):
        super().__init__()

        self.main_string = []  # [формат листа, наименование, Примечание(масса)]
        self.gabarit = gabarit
        self.title("Rapidly part")
        self.geometry("750x700")
        self.row = 6  # row for new dimension
        self.my_list = []  # list for field
        self.i = 0  # count for list
        self.tolerance_check = customtkinter.BooleanVar()
        self.tolerance_check.set(True)
        self.end_butt = customtkinter.BooleanVar()
        self.end_butt_string = customtkinter.StringVar()

        '''
        self.lable_0 = customtkinter.CTkLabel(self, text=" ", fg_color="transparent")
        self.lable_0.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        
        self.lable_1 = customtkinter.CTkLabel(self, text=" ", fg_color="transparent")
        self.lable_1.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")
        '''

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="Показывать квалитет")
        self.checkbox_1.grid(row=1, column=3, padx=20, pady=(10, 20))

        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="Показывать допуск", variable=self.tolerance_check)
        self.checkbox_2.grid(row=1, column=4, padx=20, pady=(10, 20))

        self.checkbox_3 = customtkinter.CTkCheckBox(self, text="Обработка торцов", command=self.end_butt_func, variable=self.end_butt)
        self.checkbox_3.grid(row=1, column=1, padx=20, pady=(10, 20))

        self.field_add = customtkinter.CTkButton(self, text="Добавить размер", command=self.button_event)
        self.field_add.grid(row=self.row, column=0, padx=20, pady=20)

        self.field_delete = customtkinter.CTkButton(self, text="Убрать размер", command=self.button_event_delete,
                                                    state="disabled")
        self.field_delete.grid(row=self.row, column=1, padx=20, pady=20, sticky="we")

        self.lable_2 = customtkinter.CTkLabel(self, text=" ", fg_color="transparent")
        self.lable_2.grid(row=self.row + 3, column=0, padx=20, pady=(0, 20), sticky="w")

        self.button_send = customtkinter.CTkButton(self, text="Чертежная деталь", command=self.undo_button)
        self.button_send.grid(row=self.row + 4, column=3, padx=20, pady=20, sticky="w", columnspan=1)

        self.button_send_bch = customtkinter.CTkButton(self, text="БЧ деталь", command=self.do_button,
                                                       fg_color="#ffa500", text_color="black")
        self.button_send_bch.grid(row=self.row + 4, column=4, padx=20, pady=20, sticky="w", columnspan=1)

        self.button_event()  # Добавление строки с размерами

    def do_button(self):  # Кнопка для БЧ детали
        self.main_string.append('БЧ')
        for self.m in range(len(self.my_list)):
            self.main_string.append(self.my_list[self.m].return_dim())
        self.main_string.append(self.checkbox_1.get())  # "Показывать квалитет"
        self.main_string.append(self.checkbox_2.get())  # "Показывать допуск"
        self.main_string.append(self.checkbox_3.get())  # "Обработка торцов"
        self.destroy()

    def undo_button(self):  # Кнопка для чертежной детали
        self.main_string = ['']
        self.destroy()

    def end_butt_func(self):
        print(self.end_butt.get())
        if self.end_butt.get():
            self.entry_end_butt = customtkinter.CTkEntry(self, placeholder_text="Обработка торцов Ra 12,5", textvariable=self.end_butt_string)
            self.entry_end_butt.grid(row=1, padx=20, pady=(10, 16))
        else:
            self.entry_end_butt.destroy()


    def button_event(self):  # Кнопка для добавления строки с размерами
        self.my_list.append(DimensionField(master=self, gabarit=self.gabarit))
        self.my_list[self.i].grid(row=self.row, column=0, padx=20, pady=20, sticky="we", columnspan=5)
        self.i += 1
        self.row += 1
        self.field_add.grid(row=self.row + 1)
        self.field_delete.grid(row=self.row + 1)
        self.field_delete.configure(state="normal")
        if self.row > 8:
            self.field_add.configure(state="disabled")

    def button_event_delete(self):  # Кнопка для удаления строки с размерами
        self.my_list[self.i - 1].destroy()
        self.my_list.pop(self.i - 1)
        self.i -= 1
        self.row -= 1
        self.field_add.grid(row=self.row + 1)
        self.field_delete.grid(row=self.row + 1)
        if self.row < 7:
            self.field_delete.configure(state="disabled")
        self.field_add.configure(state="normal")


class DimensionField(customtkinter.CTkFrame):  # Рамка ополнительных полей с размерами
    def __init__(self, master, gabarit, **kwargs):
        super().__init__(master, **kwargs)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="L = ")
        self.entry.insert(0, "L = ")
        self.entry.grid(row=1, column=0, padx=20, sticky="w", columnspan=1)

        self.entry_2 = customtkinter.CTkComboBox(self, values=gabarit)
        if gabarit == ' ':
            self.entry_2.set('Размер')
        self.entry_2.grid(row=1, column=1, padx=20, sticky="w", columnspan=1)

        self.button = customtkinter.CTkButton(self, text="Квалитет", command=self.button_callback)
        self.button.grid(row=1, column=2, padx=20, pady=20, sticky="w", columnspan=1)

        self.entry_3 = customtkinter.CTkEntry(self, placeholder_text="Верхний допуск")
        self.entry_3.grid(row=0, column=3, padx=20, sticky="w", columnspan=1)

        self.entry_4 = customtkinter.CTkEntry(self, placeholder_text="Нижний допуск")
        self.entry_4.grid(row=2, column=3, padx=20, sticky="w", columnspan=1)

    def button_callback(self):
        self.tolerance = Tolerance(self)  # create window if its None or destroyed

    def return_dim(self):
        if self.button._text == 'Квалитет':
            self.button.configure(text='')

        return [self.entry.get(), self.entry_2.get(), self.button._text, self.entry_3.get(), self.entry_4.get()]

    def change_button_value(self, value):
        self.button.configure(text=value)


class Tolerance(customtkinter.CTkToplevel):  # Класс окна квалитета
    def __init__(self, master):
        super().__init__(master)
        self.title("Tolerance")
        self.geometry("+400+400")
        self.id = id  # id of field
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
                self.x[k] = self.toletance[k]+str(self.row+9)
            self.button.append(customtkinter.CTkSegmentedButton(self.tabview.tab("Вал (h14)"),
                                                            width=50,
                                                            corner_radius=0,
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

    def segmented_button_callback(self, value):  # Кнопка записи квалитета
        self.destroy()
        self.master.change_button_value(value)
        self.master.master.checkbox_1.select()