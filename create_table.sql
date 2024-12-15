CREATE TABLE students (
	student_id smallint NOT NULL,
	first_name varchar(20) NOT NULL,
	last_name varchar(20) NOT NULL,
	patronymic varchar(20) NOT NULL,
	group_id smallint,
	registration_date date NOT NULL,
	phone varchar(12) NOT NULL,
	CONSTRAINT students_pk PRIMARY KEY (student_id),
	CONSTRAINT phone_number_check CHECK (phone ~ '^\+7[0-9]{10}$'),
	CONSTRAINT unique_student_phone_number UNIQUE (phone)
);

ALTER TABLE students ADD CONSTRAINT group_fk 
FOREIGN KEY (group_id)
REFERENCES groups (group_id);

CREATE TABLE instructors (
	instructor_id smallint NOT NULL,
	last_name varchar(20) NOT NULL,
	first_name varchar(20) NOT NULL,
	patronymic varchar(20) NOT NULL,
	category varchar(1),
	car_id smallint,
	phone varchar(12) NOT NULL,
	CONSTRAINT instructors_pk PRIMARY KEY (instructor_id),
	CONSTRAINT category_check CHECK (category IN ('A', 'B', 'C', 'D', 'M')),
	CONSTRAINT phone_number_check CHECK (phone ~ '^\+7[0-9]{10}$'),
	CONSTRAINT unique_instructor_phone_number UNIQUE (phone)
);

ALTER TABLE instructors ADD CONSTRAINT car_fk 
FOREIGN KEY (car_id)
REFERENCES cars (car_id);

--триггер для проверки уникальности телефонов
CREATE OR REPLACE FUNCTION check_unique_phone()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверка на наличие телефона в таблице студентов
    IF EXISTS (SELECT 1 FROM students WHERE phone = NEW.phone) THEN
        RAISE EXCEPTION 'Телефон % уже существует в таблице студентов', NEW.phone;
    END IF;
    
    -- Проверка на наличие телефона в таблице инструкторов
    IF EXISTS (SELECT 1 FROM instructors WHERE phone = NEW.phone) THEN
        RAISE EXCEPTION 'Телефон % уже существует в таблице инструкторов', NEW.phone;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер для таблицы студентов
CREATE TRIGGER trigger_check_unique_phone_students
BEFORE INSERT ON students
FOR EACH ROW
EXECUTE FUNCTION check_unique_phone();

-- Триггер для таблицы инструкторов
CREATE TRIGGER trigger_check_unique_phone_instructors
BEFORE INSERT ON instructors
FOR EACH ROW
EXECUTE FUNCTION check_unique_phone();



CREATE TABLE groups (
	group_id smallint NOT NULL,
	name varchar(10) NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	instructor_id smallint,
	CONSTRAINT groups_pk PRIMARY KEY (group_id),
	CONSTRAINT group_name_check CHECK (name IN ('A', 'B', 'C', 'D', 'M')),
	CONSTRAINT date_check CHECK (end_date >= start_date)
);

ALTER TABLE groups ADD CONSTRAINT instructor_fk 
FOREIGN KEY (instructor_id)
REFERENCES instructors (instructor_id);

CREATE TABLE public.cars (
    car_id smallint NOT NULL,
    number text NOT NULL,
    model varchar(15) NOT NULL,
    year smallint NOT NULL,
    CONSTRAINT cars_pk PRIMARY KEY (car_id),
    CONSTRAINT number_check CHECK (number ~* '^[АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{2}\d{2,3}$'),
    CONSTRAINT year_check CHECK (year >= EXTRACT(YEAR FROM CURRENT_DATE) - 7),
    CONSTRAINT unique_number_check UNIQUE (number)
);

CREATE TABLE lessons (
    lesson_id smallint NOT NULL,
    student_id smallint,
    group_id smallint,
    instructor_id smallint,
    type varchar(8) NOT NULL,
    car_id smallint,
    date date NOT NULL,
    CONSTRAINT lessons_pk PRIMARY KEY (lesson_id),
    CONSTRAINT chk_car_group_dependency CHECK (
        (type = 'практика' AND car_id IS NOT NULL AND group_id IS NULL) OR
        (type = 'теория' AND car_id IS NULL AND group_id IS NOT NULL)),
    CONSTRAINT chk_valid_type CHECK (type IN ('теория', 'практика'))
);

ALTER TABLE lessons ADD CONSTRAINT group_fk 
FOREIGN KEY (group_id)
REFERENCES groups (group_id);

ALTER TABLE lessons ADD CONSTRAINT student_fk 
FOREIGN KEY (student_id)
REFERENCES students (student_id);

ALTER TABLE lessons ADD CONSTRAINT instructor_fk 
FOREIGN KEY (instructor_id)
REFERENCES instructors (instructor_id);

ALTER TABLE lessons ADD CONSTRAINT car_fk 
FOREIGN KEY (car_id)
REFERENCES cars (car_id);

-- Создаем функцию для проверки даты занятия
CREATE OR REPLACE FUNCTION check_lesson_date()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, чтобы дата занятия не была раньше даты регистрации студента
    IF NEW.date < (SELECT registration_date FROM students WHERE student_id = NEW.student_id) THEN
        RAISE EXCEPTION 'Дата занятия % не может быть раньше даты регистрации студента для студента с ID %', NEW.lesson_id, NEW.student_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создаем триггер для таблицы lessons
CREATE TRIGGER trigger_check_lesson_date
BEFORE INSERT OR UPDATE ON lessons
FOR EACH ROW
EXECUTE FUNCTION check_lesson_date();

CREATE TABLE exams (
    exam_id smallint NOT NULL,
    student_id smallint,
    date date NOT NULL,
    type varchar(8) NOT NULL,
    scores smallint,
    summary varchar(10),
    CONSTRAINT exams_pk PRIMARY KEY (exam_id),
    CONSTRAINT chk_valid_type CHECK (type IN ('теория', 'практика')),
    CONSTRAINT summary_check CHECK (summary IN ('сдал', 'не сдал')),
    CONSTRAINT scores_check CHECK (scores >= 0 AND scores <= 100)
);

ALTER TABLE exams ADD CONSTRAINT student_id 
FOREIGN KEY (student_id)
REFERENCES students (student_id);

-- Создаем функцию для триггера
CREATE OR REPLACE FUNCTION update_exam_summary()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем значение scores и выставляем summary
    IF NEW.scores > 80 THEN
        NEW.summary := 'сдал';
    ELSE
        NEW.summary := 'не сдал';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- Создаем триггер для таблицы exams
CREATE TRIGGER trigger_update_exam_summary
BEFORE INSERT OR UPDATE ON exams
FOR EACH ROW
EXECUTE FUNCTION update_exam_summary();

-- Создаем функцию для проверки даты экзамена
CREATE OR REPLACE FUNCTION check_exam_date()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем, чтобы дата экзамена не была раньше даты регистрации студента
    IF NEW.date < (SELECT registration_date FROM students WHERE student_id = NEW.student_id) THEN
        RAISE EXCEPTION 'Дата экзамена не может быть раньше даты регистрации студента';
    END IF;
    -- Проверяем, чтобы дата экзамена была позже максимальной даты урока студента
    IF NEW.date <= (SELECT MAX(date) FROM lessons WHERE student_id = NEW.student_id) THEN
        RAISE EXCEPTION 'Дата экзамена должна быть позже даты последнего урока студента';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- Создаем триггер для таблицы exams
CREATE TRIGGER trigger_check_exam_date
BEFORE INSERT OR UPDATE ON exams
FOR EACH ROW
EXECUTE FUNCTION check_exam_date();