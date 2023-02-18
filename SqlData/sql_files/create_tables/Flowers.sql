--
-- Файл сгенерирован с помощью SQLiteStudio
--
-- Использованная кодировка текста: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: flowers
CREATE TABLE IF NOT EXISTS flowers (
    id_flower INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR (40)
);

INSERT INTO flowers (
                            id_flower,
                            name
                        )
                        VALUES (
                            1,
                            'нежно розовые пионы'
                        ),
                        (
                            2,
                            'эвкалипт'
                        ),
                        (
                            3,
                            'роза Одилия'
                        ),
                        (
                            4,
                            'роза Лиана'
                        ),
                        (
                            5,
                            'роза Файер Флеш'
                        ),
                        (
                            6,
                            'астра розовая'
                        ),
                        (
                            7,
                            'астра белая'
                        ),
                        (
                            8,
                            'верба'
                        ),
                        (
                            9,
                            'гвоздика'
                        ),
                        (
                            10,
                            'гиперикум'
                        ),
                        (
                            11,
                            'гиацинт'
                        ),
                        (
                            12,
                            'гладиолус'
                        ),
                        (
                            13,
                            'гортензия'
                        ),
                        (
                            14,
                            'илекс'
                        ),
                        (
                            15,
                            'ирис'
                        ),
                        (
                            16,
                            'лаванда'
                        ),
                        (
                            17,
                            'ландыш'
                        ),
                        (
                            18,
                            'лилия'
                        );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
