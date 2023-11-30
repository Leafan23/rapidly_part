import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("my app")
        self.geometry("750x700")

        self.new_window = []
        self.int = customtkinter.IntVar()
        self.int.set(0)

        self.lable = customtkinter.CTkLabel(self, text=self.int.get())
        self.lable.pack()

        self.button = customtkinter.CTkButton(self, text="Создать окно", command=self.add_window)
        #  self.field_delete.configure(state="disabled")
        self.button.pack()

    def add_window(self):
        self.new_window.append(NewWindow(self))


class NewWindow(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.button = customtkinter.CTkButton(self, text="Добавить", command=self.add_int)
        self.button.pack()

    def add_int(self):
        #  self.i = self.master.int.get()
        self.button_in_main = customtkinter.CTkButton(self.master, text="Новая кнопка", command=None)
        self.button_in_main.pack()


