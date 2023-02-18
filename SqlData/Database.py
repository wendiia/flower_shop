import sqlite3 as sql
import aiosqlite
import os


class Database:
    """Класс Database создает базу данных, если она была не создана, наполняет ее шаблонными данными
        Основная задача - применение запросов к базе данных Db.db
    """
    def __init__(self):
        self.max_date = ""
        self.min_date = ""
        self.db = "./SqlData/Db.db"
        self.connection = sql.connect(self.db)
        self.cur = self.connection.cursor()
        sql_files_list = sorted(os.listdir("./SqlData/sql_files/create_tables/"))
        for i in sql_files_list:
            with open("./SqlData/sql_files/create_tables/" + i, 'r') as sql_file:
                sql_script = sql_file.read()
                try:
                    self.cur.executescript(sql_script)
                    self.connection.commit()
                except sql.Error as e:
                    self.error = f"Ошибка выполнения запроса {e} Имя файла: {sql_file.name}"  # убрать
        if self.connection:
            self.connection.close()

    async def flowers_flavors_data(self, tbl_name):
        """Составляет и выполняет запрос на взятие данных с таблицы flowers и flavors"""
        query = "SELECT * FROM {}".format(tbl_name)

        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query) as cursor:
                return await cursor.fetchall()

    async def composition_data(self, id_flavor):
        """Составляет и выполняет запрос на взятие данных с таблицы composition"""
        query = "SELECT id, flowers.name, count FROM composition JOIN flowers USING(id_flower) WHERE id_flavor={} ".format(id_flavor)

        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query) as cursor:
                return await cursor.fetchall()

    async def save_data(self, data, name_tbl):
        """Составляет и выполняет запрос на сохранение данных в таблицу"""
        if name_tbl == "flowers":
            query = "INSERT INTO {} VALUES (?, ?)".format(name_tbl)
        elif name_tbl == "composition":
            query = "INSERT INTO {} VALUES (?, ?, ?, ?)".format(name_tbl)
        else:
            query = "INSERT INTO {} VALUES (?, ?, ?)".format(name_tbl)

        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cursor:
                if name_tbl == "composition":
                    del_query = "DELETE FROM {} WHERE id_flavor = {}".format(name_tbl, data[0][1])
                else:
                    del_query = "DELETE FROM {}".format(name_tbl)

                if name_tbl == "flavors":
                    id_flavors = [i[0] for i in data]
                    id_flavors = ", ".join(id_flavors)
                    del_query1 = "DELETE FROM composition WHERE id_flavor NOT IN ({})".format(id_flavors)
                    await cursor.execute(del_query1)  # удаление старых данных с таблицы sql

                await cursor.execute(del_query)  # удаление старых данных с таблицы sql
                await cursor.executemany(query, data)  # вставка новых данных в таблицу sql
            await db.commit()
            return cursor.rowcount

    async def last_id(self, tbl_name):
        """Составляет и выполняет запрос получение последнего id из таблицы"""
        query = "SELECT * FROM {} ORDER BY 1 DESC LIMIT 1".format(tbl_name)
        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query) as cursor:
                return await cursor.fetchone()

    async def orders_data(self):
        """Составляет и выполняет запрос на взятие данных с таблицы orders"""
        query = "SELECT id_main, surname, orders.name, phone, flavors.name, date_begin, date_end, cost " \
                "FROM orders INNER JOIN flavors USING (id_flavor)"
        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query) as cursor:
                return await cursor.fetchall()

    async def save_data_order(self, data):
        """Составляет и выполняет запрос на сохранение данных в таблицу orders"""
        query = """INSERT INTO orders (id_main, surname, name, phone, id_flavor, date_begin, date_end)
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cursor:
                await cursor.execute("DELETE FROM orders")  # удаление старых данных с таблицы sql
                await cursor.executemany(query, data)  # вставка новых данных в таблицу sql
            await db.commit()
            return cursor.rowcount

    async def list_flowers(self, flower, min_date, max_date):
        """Составляет и выполняет запрос на взятие суммарного количество цветов по взятым параметрам"""
        list_flowers = []
        data = [min_date, max_date]

        if flower == "Все цветы":
            with open("./SqlData/sql_files/queries/get_list_flowers.sql", 'r') as sql_file:
                query = sql_file.read()
        else:
            with open("./SqlData/sql_files/queries/get_list_flowers_filter.sql", 'r') as sql_file:
                query = sql_file.read()
            data.append(flower)
        length_data = len(data)
        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query, data) as cursor:
                async for i in cursor:
                    if length_data == 3:
                        result_str = f"{i[0]}{'-' * (25 - len(i[1]))}{i[2]} шт"
                    else:
                        result_str = f"{i[0]}{'-' * (25 - len(i[0]))}{i[1]} шт"
                    list_flowers.append(result_str)
            return list_flowers

    async def all_money(self):
        """Составляет и выполняет запрос на получение суммарной прибыли"""
        with open("./SqlData/sql_files/queries/get_all_money.sql", 'r') as sql_file:
            async with aiosqlite.connect(self.db) as db:
                async with db.execute(sql_file.read()) as cursor:
                    return await cursor.fetchone()

    async def min_max_dates(self):
        """Составляет и выполняет запрос на получение ранней и поздней дат"""
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cur:
                await cur.execute("SELECT MIN(date_begin), MAX(date_begin) FROM orders")
                return await cur.fetchone()

    async def get_flowers(self):
        """Составляет и выполняет запрос на получение всего спискса цветов"""
        async with aiosqlite.connect(self.db) as db:
            async with db.cursor() as cur:
                await cur.execute("SELECT name FROM flowers")
                return [" ".join(x) for x in await cur.fetchall()]

    async def flavor_flowers_id(self, query_data):
        """Выполняет запрос на получение названий букетов либо цветов и формирует из данных словарь"""
        query = "SELECT {}, name FROM {}".format(query_data[0], query_data[1])
        dict_id = {}
        async with aiosqlite.connect(self.db) as db:
            async with db.execute(query) as cursor:
                async for i in cursor:
                    dict_id[i[1]] = i[0]
            return dict_id

    async def last_id_orders(self):
        """Составляет и выполняет запрос получение последнего id из таблицы orders"""
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT id_main FROM orders ORDER BY id_main DESC LIMIT 1") as cursor:
                return await cursor.fetchone()
