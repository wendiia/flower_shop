--
-- Файл сгенерирован с помощью SQLiteStudio
--
-- Использованная кодировка текста: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: flavors
CREATE TABLE IF NOT EXISTS flavors (
    id_flavor INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR (50),
    cost INTEGER
);

INSERT INTO flavors (
                     id_flavor,
                     name,
                     cost
                 )
                 VALUES (
                     1,
                     'Ароматы лета',
                     8200
                 ),
                 (
                     2,
                     'Разноцветье',
                     6000
                 ),
                 (
                     3,
                     'Шелковый путь',
                     5400
                 ),
                 (
                     4,
                     'Салют',
                     7500
                 );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
