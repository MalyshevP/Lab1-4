import tkinter as tk
from tkinter import ttk
from turtle import width
import requests
from xlsxwriter.workbook import Workbook
from copy import deepcopy

SERVER_URL = "http://localhost:8000/"

# окно ввода данных 
class popupWindow(object):
    def __init__(self,master):
        top=self.top=tk.Toplevel(master)
        self.top.title("Добавление")
        self.l_id=tk.Label(top,text="Персональный ID")
        self.l_id.pack()
        self.e_id=tk.Entry(top)
        self.e_id.pack()

        self.l_f=tk.Label(top,text="Фамилия")
        self.l_f.pack()
        self.e_f=tk.Entry(top)
        self.e_f.pack()

        self.l_i=tk.Label(top,text="Имя")
        self.l_i.pack()
        self.e_i=tk.Entry(top)
        self.e_i.pack()

        self.l_o=tk.Label(top,text="Отчество")
        self.l_o.pack()
        self.e_o=tk.Entry(top)
        self.e_o.pack()

        self.l_age=tk.Label(top,text="Age")
        self.l_age.pack()
        self.e_age=tk.Entry(top)
        self.e_age.pack()

        self.l_sex=tk.Label(top,text="Sex")
        self.l_sex.pack()
        self.e_sex=tk.Entry(top)
        self.e_sex.pack()

        self.b=tk.Button(self.top,text='Добавить',command=self.cleanup)
        self.b.pack()

    # сохранение значений полей и закрытие окна
    def cleanup(self):
        self.id=self.e_id.get()
        self.f=self.e_f.get()
        self.i=self.e_i.get()
        self.o=self.e_o.get()
        self.age=self.e_age.get()
        self.sex=self.e_sex.get()
        self.top.destroy()

# главное окно
class App(object):
    def __init__(self, master):
        self.window = master
        self.window.title("DB Explorer")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(1, minsize=800, weight=1)
        self.fr_data = tk.Frame(self.window, bg="#FFFFFF")
        self.fr_buttons = tk.Frame(self.window)

        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.fr_data.grid(row=0, column=1, sticky="nsew")

        # Кнопки
        self.btn_refresh = tk.Button(self.fr_buttons, text="Обновить", command=self.refresh)
        self.btn_add = tk.Button(self.fr_buttons, text="Добавить", command=self.add)
        self.btn_delete = tk.Button(self.fr_buttons, text="Удалить", command=self.remove)
        self.btn_purge = tk.Button(self.fr_buttons, text="Очистить", command=self.purge)
        self.btn_export = tk.Button(self.fr_buttons, text="Экспорт", command=self.export)

        # Порядок кнопок
        self.btn_refresh.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_add.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.btn_delete.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.btn_purge.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.btn_export.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

        # строки таблицы
        self.rows = list()
        # id в БД строк таблицы
        self.db_id_row_map = None
        self.create_scroll_table()

    # создание таблицы
    def create_scroll_table(self):
        data_scroll = tk.Scrollbar(self.fr_data)
        data_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.data_table = ttk.Treeview(
            self.fr_data, yscrollcommand=data_scroll.set)

        self.data_table.pack()

        data_scroll.config(command=self.data_table.yview)
        data_scroll.config(command=self.data_table.xview)

        # Столбцы таблицы
        self.data_table['columns'] = ('ID', 'F', 'I', "O", "Age", "Sex")

        # форматирование столбцов
        self.data_table.column("#0", width=0,  stretch=tk.NO)
        self.data_table.column("ID", anchor=tk.CENTER, width=50)
        self.data_table.column("F", anchor=tk.CENTER)
        self.data_table.column("I", anchor=tk.CENTER)
        self.data_table.column("O", anchor=tk.CENTER)
        self.data_table.column("Age", anchor=tk.CENTER, width=60)
        self.data_table.column("Sex", anchor=tk.CENTER, width=50)

        # Заголовки столбцов
        self.data_table.heading("#0", text="", anchor=tk.CENTER)
        self.data_table.heading("ID", text="ID", anchor=tk.CENTER)
        self.data_table.heading("F", text="Фамилия", anchor=tk.CENTER)
        self.data_table.heading("I", text="Имя", anchor=tk.CENTER)
        self.data_table.heading("O", text="Отчество", anchor=tk.CENTER)
        self.data_table.heading("Age", text="Возраст", anchor=tk.CENTER)
        self.data_table.heading("Sex", text="Пол", anchor=tk.CENTER)

    # добавление данных в таблицу
    def add_data(self):
        for i in range(len(self.rows)):
            self.data_table.insert(parent='', index='end', iid=i, text='',
                                   values=self.rows[i])
        self.data_table.pack()

    # отчистка таблицы
    def clear_table(self):
        self.data_table.delete(*self.data_table.get_children())

    # получение данных и обновление таблицы 
    def refresh(self):
        response = requests.get(SERVER_URL+"read")
        if response.status_code == 200:
            data = response.json()
            self.rows = list()
            self.db_id_row_map = list()
            for el in data["collection"]:
                self.rows.append((el['id'], el['last_name'], el['first_name'],
                                 el['middle_name'], el['age'], el['sex']))
                self.db_id_row_map.append(el['_id'])
            self.clear_table()
            self.add_data()

    # Добавление данных в БД
    def add(self):
        self.ask=popupWindow(self.window)
        self.btn_add["state"] = "disabled" 
        self.window.wait_window(self.ask.top)

        new_data = {
            "last_name": self.ask.f,
            "first_name": self.ask.i,
            "middle_name": self.ask.o,
            "age": self.ask.age,
            "sex": self.ask.sex,
            "id": self.ask.id
        }
        requests.post(SERVER_URL+"write", json=new_data)

        self.btn_add["state"] = "normal"
        self.refresh()

    # Удаление выделенной строки из БД
    def remove(self):
        selected_item = self.data_table.focus()
        if selected_item:
            selected_index = int(selected_item)
            db_id = self.db_id_row_map[selected_index]
            requests.post(SERVER_URL+"delete", json={"db_id": db_id})
            self.refresh()

    # Отчистка БД
    def purge(self):
        requests.get(SERVER_URL+"purge")
        self.refresh()

    # Экспорт в Excel
    def export(self):
        workbook = Workbook('exported.xlsx')
        worksheet = workbook.add_worksheet()
        self.refresh()
        rows = deepcopy(self.rows)

        rows.insert(0, ("ID", "Фамилия", "Имя", "Отчество", "Возраст", "Пол"))
        for r, row in enumerate(rows):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
        workbook.close()


if __name__ == "__main__":
    root=tk.Tk()
    app=App(root)
    root.mainloop()
