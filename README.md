# Приложение для управления базой данных автошколы

## Описание
Вашему вниманию представляется графический интерфейс, разработанный для управления базой данных автошколы. Программа позволяет выполнять CRUD-операции (создание, чтение, обновление, удаление) для различных сущностей, таких как студенты, инструкторы, группы, автомобили, уроки и экзамены, данные которых хранятся в базе данных PostgreSQL.

Приложение написано на Python с использованием следующих библиотек:
- **customtkinter**: Для создания современных и эстетичных интерфейсов.
- **tkinter.ttk**: Для стандартных элементов интерфейса.
- **psycopg2**: Для работы с базой данных PostgreSQL.

## Возможности
- **Многовкладочный интерфейс**: Отдельные вкладки для управления разными сущностями (студенты, инструкторы, группы, автомобили, уроки, экзамены).
- **CRUD-операции**: Легкое добавление, просмотр, обновление и удаление записей в каждой таблице.
- **Интеграция с PostgreSQL**: Надежное и эффективное хранение данных.
- **Современный дизайн**: Чистый и удобный пользовательский интерфейс.

## Установка
### Предварительные требования
1. Установленный Python.
2. Сервер базы данных PostgreSQL, установленный и запущенный.
3. Установка необходимых библиотек Python:
   ```bash
   pip install customtkinter psycopg2
   ```

### Настройка базы данных
1. Создайте базу данных PostgreSQL с именем `DrivingSchool`.
2. Настройте необходимые таблицы (например, `students`, `instructors` и т.д.) с помощью SQL-скриптов.
3. При необходимости измените параметры подключения в коде (например, хост, имя базы данных, имя пользователя и пароль).

### Запуск приложения
1. Запуститу файл с расширением `.py`.
   ```bash
   python main.py
   ```

## Использование
1. Запустите приложение, чтобы открыть главное окно.
2. Переключайтесь между вкладками для управления конкретными сущностями.
3. Используйте предоставленные формы и кнопки для выполнения CRUD-операций.
4. Все изменения будут мгновенно сохраняться в базе данных PostgreSQL.