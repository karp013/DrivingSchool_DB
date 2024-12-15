# Импортируем необходимые библиотеки:
# - customtkinter используется для создания современного интерфейса.
# - ttk и messagebox из tkinter предоставляют стандартные элементы интерфейса и всплывающие сообщения.
# - psycopg2 — библиотека для работы с базой данных PostgreSQL.
import customtkinter as ctk
from tkinter import ttk, messagebox
import psycopg2

# Класс для реализации графического интерфейса управления автошколой.
class DrivingSchoolGUI:
    def __init__(self, root):
        # Конструктор класса, где происходит инициализация приложения.
        self.root = root
        self.root.title("Driving School Management")  # Устанавливаем заголовок окна.

        # Подключаемся к базе данных PostgreSQL.
        self.conn = psycopg2.connect(
            host     = "localhost",          # Хост сервера базы данных.
            dbname   = "DrivingSchool",    # Имя базы данных.
            user     = "postgres",           # Имя пользователя для подключения.
            password = "postgres"        # Пароль для подключения.
        )
        self.cursor = self.conn.cursor()  # Создаем объект курсора для выполнения SQL-запросов.

        # Словарь для хранения виджетов Treeview для каждой таблицы.
        self.trees = {}

        # Словарь для хранения виджетов Entry (текстовых полей) для каждой таблицы.
        self.entries = {}

        # Вызываем метод для создания вкладок.
        self.create_tabs()

    def create_tabs(self):
        # Создаем объект вкладок с помощью customtkinter.
        tab_control = ctk.CTkTabview(self.root)

        # Добавляем вкладки для каждой таблицы.
        self.student_tab    = tab_control.add("Students")
        self.instructor_tab = tab_control.add("Instructors")
        self.group_tab      = tab_control.add("Groups")
        self.car_tab        = tab_control.add("Cars")
        self.lesson_tab     = tab_control.add("Lessons")
        self.exam_tab       = tab_control.add("Exams")

        # Устанавливаем размещение вкладок в основном окне.
        tab_control.pack(expand=True, fill="both")

        # Вызываем методы для создания интерфейса для каждой вкладки.
        self.create_student_tab()
        self.create_instructor_tab()
        self.create_group_tab()
        self.create_car_tab()
        self.create_lesson_tab()
        self.create_exam_tab()

    # Метод для создания интерфейса вкладки "Students".
    def create_student_tab(self):
        self.create_crud_ui(self.student_tab, "students", [
            "student_id", "first_name", "last_name", "patronymic", "group_id", "registration_date", "phone"
        ])

    # Метод для создания интерфейса вкладки "Instructors".
    def create_instructor_tab(self):
        self.create_crud_ui(self.instructor_tab, "instructors", [
            "instructor_id", "last_name", "first_name", "patronymic", "category", "car_id", "phone"
        ])

    # Метод для создания интерфейса вкладки "Groups".
    def create_group_tab(self):
        self.create_crud_ui(self.group_tab, "groups", [
            "group_id", "name", "start_date", "end_date", "instructor_id"
        ])

    # Метод для создания интерфейса вкладки "Cars".
    def create_car_tab(self):
        self.create_crud_ui(self.car_tab, "cars", [
            "car_id", "number", "model", "year"
        ])

    # Метод для создания интерфейса вкладки "Lessons".
    def create_lesson_tab(self):
        self.create_crud_ui(self.lesson_tab, "lessons", [
            "lesson_id", "student_id", "group_id", "instructor_id", "type", "car_id", "date"
        ])

    # Метод для создания интерфейса вкладки "Exams".
    def create_exam_tab(self):
        self.create_crud_ui(self.exam_tab, "exams", [
            "exam_id", "student_id", "date", "type", "scores", "summary"
        ])

    # Общий метод для создания CRUD-интерфейса для таблицы.
    def create_crud_ui(self, parent, table_name, fields):
        # Создаем фрейм для размещения всех элементов интерфейса.
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True)

        # Создаем форму ввода данных с помощью текстовых полей (Entry).
        self.entries[table_name] = {}  # Инициализируем словарь для текстовых полей.
        for idx, field in enumerate(fields):
            # Создаем метку для каждого поля.
            label = ctk.CTkLabel(frame, text=field)
            label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)  # Слева выравниваем метки.

            # Создаем текстовое поле для ввода значений.
            entry = ctk.CTkEntry(frame, width=200)
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")  # Текстовое поле растягивается по горизонтали.
            self.entries[table_name][field] = entry  # Сохраняем текстовое поле в словарь.

        # Настраиваем адаптивную ширину колонок.
        frame.grid_columnconfigure(0, weight=1)  # Левый столбец (метки).
        frame.grid_columnconfigure(1, weight=2)  # Правый столбец (текстовые поля).

        # Создаем фрейм для кнопок управления.
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=10, sticky="ew")

        # Добавляем кнопки для CRUD-операций.
        ctk.CTkButton(btn_frame, text="Create", command=lambda: self.create_entry(table_name, fields)).grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="Read", command=lambda: self.read_entries(table_name, fields)).grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="Update", command=lambda: self.update_entry(table_name, fields)).grid(row=0, column=2, padx=5, sticky="ew")
        ctk.CTkButton(btn_frame, text="Delete", command=lambda: self.delete_entry(table_name, fields)).grid(row=0, column=3, padx=5, sticky="ew")

        # Делаем кнопки одинаковой ширины.
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        btn_frame.grid_columnconfigure(3, weight=1)

        # Создаем таблицу (Treeview) для отображения данных из базы.
        tree = ttk.Treeview(frame, columns=fields, show="headings")
        for field in fields:
            tree.heading(field, text=field)  # Устанавливаем заголовки столбцов.
            tree.column(field, width=100)   # Устанавливаем ширину столбцов.
        tree.grid(row=len(fields)+1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Настраиваем растяжение таблицы при изменении размера окна.
        frame.grid_rowconfigure(len(fields)+1, weight=1)

        self.trees[table_name] = tree  # Сохраняем таблицу в словарь.

    # Метод для создания новой записи в таблице.
    def create_entry(self, table_name, fields):
        # Получаем данные из текстовых полей.
        values = [
            None if self.entries[table_name][field].get().strip() == "" else self.entries[table_name][field].get()
            for field in fields
        ]
        try:
            # Формируем запрос INSERT.
            placeholders = ", ".join(["%s"] * len(values))
            query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
            self.cursor.execute(query, values)  # Выполняем запрос.
            self.conn.commit()  # Подтверждаем изменения в базе.
            messagebox.showinfo("Success", "Entry created successfully")  # Уведомляем об успехе.
            self.read_entries(table_name, fields)  # Обновляем данные в таблице.
        except Exception as e:
            self.conn.rollback()  # Откатываем изменения в случае ошибки.
            messagebox.showerror("Error", f"Failed to create entry: {str(e)}")  # Уведомляем об ошибке.

    # Метод для чтения и отображения данных из таблицы.
    def read_entries(self, table_name, fields):
        try:
            # Формируем запрос SELECT.
            query = f"SELECT {', '.join(fields)} FROM {table_name}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()  # Получаем все строки.

            # Очищаем текущие данные в Treeview.
            tree = self.trees[table_name]
            for i in tree.get_children():
                tree.delete(i)

            # Добавляем новые строки в Treeview.
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))  # Уведомляем об ошибке.

    # Метод для обновления записи в таблице.
    def update_entry(self, table_name, fields):
        values = [
            None if self.entries[table_name][field].get().strip() == "" else self.entries[table_name][field].get()
            for field in fields
        ]
        try:
            # Формируем запрос UPDATE.
            set_clause = ", ".join([f"{field} = %s" for field in fields[1:]])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {fields[0]} = %s"
            self.cursor.execute(query, values[1:] + [values[0]])
            self.conn.commit()  # Подтверждаем изменения.
            messagebox.showinfo("Success", "Entry updated successfully")
            self.read_entries(table_name, fields)  # Обновляем данные.
        except Exception as e:
            self.conn.rollback()  # Откатываем изменения в случае ошибки.
            messagebox.showerror("Error", str(e))  # Уведомляем об ошибке.

    # Метод для удаления записи из таблицы.
    def delete_entry(self, table_name, fields):
        try:
            # Получаем значение первичного ключа.
            pk_value = self.entries[table_name][fields[0]].get()
            # Формируем запрос DELETE.
            query = f"DELETE FROM {table_name} WHERE {fields[0]} = %s"
            self.cursor.execute(query, (pk_value,))
            self.conn.commit()  # Подтверждаем изменения.
            messagebox.showinfo("Success", "Entry deleted successfully")
            self.read_entries(table_name, fields)  # Обновляем данные.
        except Exception as e:
            self.conn.rollback()  # Откатываем изменения в случае ошибки.
            messagebox.showerror("Error", f"Failed to delete entry: {str(e)}")  # Уведомляем об ошибке.

# Точка входа в приложение.
if __name__ == "__main__":
    ctk.set_appearance_mode("Light")  # Устанавливаем светлую тему.
    ctk.set_default_color_theme("blue")  # Устанавливаем синюю цветовую тему.

    root = ctk.CTk()  # Создаем главное окно приложения.
    app = DrivingSchoolGUI(root)  # Создаем экземпляр класса интерфейса.
    root.mainloop()  # Запускаем цикл обработки событий.



