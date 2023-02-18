--
-- ���� ������������ � ������� SQLiteStudio
--
-- �������������� ��������� ������: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: orders
CREATE TABLE IF NOT EXISTS orders (
    id_main    INTEGER PRIMARY KEY NOT NULL,
    surname    STRING (40),
    name       STRING (40),
    phone      STRING (40),
    id_flavor    INTEGER REFERENCES flavors (id_flavor) ON DELETE CASCADE ON UPDATE CASCADE,
    date_begin DATE,
    date_end   DATE
);

INSERT INTO orders (id_main,
                          surname,
                          name,
                          phone,
                          id_flavor,
                          date_begin,
                          date_end
                      )
                      VALUES
                      (
                          1,
                          '������',
                          '�����',
                          '8(977)626-57-18',
                          3,
                          '2022-05-01',
                          '2022-05-02'
                      ),
                      (
                          2,
                          '�������',
                          '���������',
                          '8(435)136-53-73',
                          1,
                          '2022-05-02',
                          '2022-05-12'
                      ),
                      (
                          3,
                          '��������',
                          '������',
                          '8(456)346-74-11',
                          2,
                          '2022-06-07',
                          '2022-06-10'
                      ),
                      (
                          4,
                          '�����',
                          '�������',
                          '8(745)734-84-46',
                          3,
                          '2022-06-25',
                          '2022-06-29'
                      ),
                      (
                          5,
                          '�������',
                          '�������',
                          '8(845)923-84-58',
                          2,
                          '2022-07-07',
                          '2022-07-14'
                      ),
                      (
                          6,
                          '�����',
                          '������',
                          '8(192)323-33-55',
                          4,
                          '2022-08-11',
                          '2022-08-18'
                      ),
                      (
                          8,
                          '�����',
                          '����',
                          '8(453)738-22-35',
                          1,
                          '2022-08-21',
                          '2022-08-26'
                      ),
                      (
                          9,
                          '�������',
                          '������',
                          '8(837)436-29-99',
                          2,
                          '2022-11-04',
                          '2022-11-14'
                      ),
                      (
                          10,
                          '������',
                          '������',
                          '8(923)483-82-74',
                          3,
                          '2022-11-07',
                          '2022-11-12'
                      ),
                      (
                          11,
                          '������',
                          '������',
                          '8(115)929-93-44',
                          2,
                          '2022-11-13',
                          '2022-11-15'
                      );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
