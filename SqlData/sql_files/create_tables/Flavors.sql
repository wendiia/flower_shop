--
-- ���� ������������ � ������� SQLiteStudio
--
-- �������������� ��������� ������: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: flavors
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
                     '������� ����',
                     8200
                 ),
                 (
                     2,
                     '�����������',
                     6000
                 ),
                 (
                     3,
                     '�������� ����',
                     5400
                 ),
                 (
                     4,
                     '�����',
                     7500
                 );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
