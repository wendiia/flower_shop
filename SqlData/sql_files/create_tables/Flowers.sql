--
-- ���� ������������ � ������� SQLiteStudio
--
-- �������������� ��������� ������: windows-1251
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: flowers
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
                            '����� ������� �����'
                        ),
                        (
                            2,
                            '��������'
                        ),
                        (
                            3,
                            '���� ������'
                        ),
                        (
                            4,
                            '���� �����'
                        ),
                        (
                            5,
                            '���� ����� ����'
                        ),
                        (
                            6,
                            '����� �������'
                        ),
                        (
                            7,
                            '����� �����'
                        ),
                        (
                            8,
                            '�����'
                        ),
                        (
                            9,
                            '��������'
                        ),
                        (
                            10,
                            '���������'
                        ),
                        (
                            11,
                            '�������'
                        ),
                        (
                            12,
                            '���������'
                        ),
                        (
                            13,
                            '���������'
                        ),
                        (
                            14,
                            '�����'
                        ),
                        (
                            15,
                            '����'
                        ),
                        (
                            16,
                            '�������'
                        ),
                        (
                            17,
                            '������'
                        ),
                        (
                            18,
                            '�����'
                        );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
