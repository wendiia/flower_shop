from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow
import asyncio
import SqlData
from GuiApp import *
from asyncqt import asyncSlot
from Singleton import Singleton


@Singleton()
class OrderSystem(QMainWindow):
    """Класс OrderSystem содержит набор функций, импортируемых классов и модулей,
    при помощи которых реализована логика работы приложения

    Note:
        Возможны проблемы с кодировкой в Linux
    """

    def __init__(self, app):
        self.app = app
        QMainWindow.__init__(self)
        self.ui = UiMainWindow(self)
        self.ui.setup_ui()
        self.tables = {1: ["flowers", self.ui.tbl_flowers], 2: ["flavors", self.ui.tbl_flavors],
                       3: ["composition", self.ui.tbl_composition]}
        self.db = SqlData.ex_db
        self.window_size = 0
        self.all_money = ""
        self.dict_flavor_id = {}
        self.dict_flower_id = {}
        self.widgets_mas = []
        self.composition_widgets = []
        self.flowers = []
        self.min_date, self.max_date = ("", "")
        self.one_row_flag = True
        self.last_row = 0
        self.animation = None
        self.click_position = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        QtWidgets.QSizeGrip(self.ui.size_grip)
        self.ui.main_header.mouseMoveEvent = self.move_window
        self.ui.btn_toggle.clicked.connect(lambda: self.slide_left_menu())
        self.ui.stacked_widget.setCurrentWidget(self.ui.orders_page)
        self.settings_ui_btns()
        self.async_init()
        self.show()

    def move_window(self, e):
        """Позволяет перемещать рабочее окно приложения
        Parameters
        ----------
        e : QMouseEvent
            класс события мыши
        """
        if not self.isMaximized():
            if e.buttons() == Qt.LeftButton:
                self.move(self.pos() + e.globalPos() - self.click_position)
                self.click_position = e.globalPos()
                e.accept()

    @asyncSlot()
    async def async_init(self):
        """
        Точка входа в асинхронность
        """
        result = await asyncio.gather(self.db.min_max_dates(), self.db.get_flowers(),
                                      self.db.flavor_flowers_id(["id_flavor", "flavors"]),
                                      self.db.flavor_flowers_id(["id_flower", "flowers"]))
        self.min_date, self.max_date = result[0][0], result[0][1]
        self.flowers = result[1]
        self.dict_flavor_id = result[2]
        self.dict_flower_id = result[3]

        self.ui.date_begin_flowers.setDate(QDate.fromString(self.min_date, "yyyy-MM-dd"))
        self.ui.date_end_flowers.setDate(QDate.fromString(self.max_date, "yyyy-MM-dd"))
        self.ui.combo_flowers.addItems(self.flowers)

        self.ui.combo_tbls.addItems(self.dict_flavor_id)

        await self.load_data_order()
        await self.load_data_flowers_flavors(self.tables[1])
        await self.load_data_flowers_flavors(self.tables[2])
        await self.load_data_composition()
        await self.clicked_btn()
        await self.list_flowers()

    async def clicked_btn(self):
        """Присваивание функций кнопкам, которые связаны с управлением таблицей, списком ингредиентов"""
        self.ui.btn_load.clicked.connect(self.load_data_order)
        self.ui.btn_add.clicked.connect(self.add_new_row_orders)
        self.ui.btn_del.clicked.connect(self.delete_row)
        self.ui.btn_save.clicked.connect(self.save_data_order)
        self.ui.btn_products.clicked.connect(self.list_flowers)

        self.ui.btn_load_flower.clicked.connect(lambda: self.load_data_flowers_flavors(self.tables[1]))
        self.ui.btn_add_flower.clicked.connect(lambda: self.add_new_row(self.tables[1]))
        self.ui.btn_del_flower.clicked.connect(lambda: self.delete_row_flowers_flavors(self.tables[1]))
        self.ui.btn_save_flower.clicked.connect(lambda: self.save_data_flowers_flavors(self.tables[1]))

        self.ui.btn_load_flavor.clicked.connect(lambda: self.load_data_flowers_flavors(self.tables[2]))
        self.ui.btn_add_flavor.clicked.connect(lambda: self.add_new_row(self.tables[2]))
        self.ui.btn_del_flavor.clicked.connect(lambda: self.delete_row_flowers_flavors(self.tables[2]))
        self.ui.btn_save_flavor.clicked.connect(lambda: self.save_data_flowers_flavors(self.tables[2]))

        self.ui.btn_load_composition.clicked.connect(lambda: self.load_data_composition())
        self.ui.btn_add_composition.clicked.connect(lambda: self.add_new_row(self.tables[3]))
        self.ui.btn_del_composition.clicked.connect(lambda: self.delete_row_flowers_flavors(self.tables[3]))
        self.ui.btn_save_composition.clicked.connect(lambda: self.save_data_flowers_flavors(self.tables[3]))

    def mousePressEvent(self, event):
        """Срабатывает при нажатии ЛКМ в приложении
        Основное применение - отслеживание координат мыши
        Parameters
        ----------
        event : QMouseEvent
            класс событий мыши
        """
        self.click_position = event.globalPos()

    def slide_left_menu(self):
        """
        Выдвижение левой боковой панели при нажатии на btn_toggle
        """
        width = self.ui.left_side_menu.width()
        if width == 50:
            new_width = 160
        else:
            new_width = 50
        self.animation = QPropertyAnimation(self.ui.left_side_menu, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def settings_ui_btns(self):
        """
        Присваивание функций кнопкам GUI
        """
        self.ui.btn_min.clicked.connect(lambda: self.showMinimized())
        self.ui.btn_restore.clicked.connect(lambda: self.restore_maximize_win())
        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.ui.btn_flowers_menu.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.flowers_page))  # !!!!!!! flowers_page
        self.ui.btn_flavors_menu.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.flavor_page))  # !!!!!!! flavor_page
        self.ui.btn_composition_menu.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.composition_page))  # !!!!!!! composition_page
        self.ui.btn_orders_menu.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.orders_page))
        self.ui.btn_products_menu.clicked.connect(
            lambda: self.ui.stacked_widget.setCurrentWidget(self.ui.products_page))
        self.ui.combo_tbls.activated.connect(self.on_combobox_changed)

    def restore_maximize_win(self):
        """
        Расширение окна и уменьшение до нормального размера
        """
        win_status = self.window_size
        if win_status == 0:
            self.window_size = 1
            self.showMaximized()
        else:
            self.window_size = 0
            self.showNormal()

    def on_combobox_changed(self):
        self.load_data_composition()

    @asyncSlot()
    async def load_data_composition(self):
        """
        Загрузка данных с таблицы composition из бд sql Db.db. Срабатывает при нажатии на кнопку 'Загрузить' на вкладке
        "Композиции".
        """
        self.dict_flower_id = await self.db.flavor_flowers_id(["id_flower", "flowers"])
        cur_tbl = self.ui.tbl_composition
        combo_item = self.ui.combo_tbls.currentText()
        data_composition = await self.db.composition_data(self.dict_flavor_id[combo_item])
        cur_tbl.setRowCount(0)
        self.composition_widgets.clear()

        for row_number, row_data in enumerate(data_composition):
            cur_tbl.insertRow(row_number)
            for col_number, col_data in enumerate(row_data):
                if col_number == 1:
                    self.composition_widgets.append(ComboPickFlavor(self, self.dict_flower_id))
                    cur_tbl.setCellWidget(row_number, col_number, self.composition_widgets[row_number])
                    self.composition_widgets[row_number].setCurrentText(col_data)

                item = QtWidgets.QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignHCenter)
                cur_tbl.setItem(row_number, col_number, item)

        self.ui.lbl_info_tbl.setText("Данные загружены")
        self.one_row_flag = True

    @asyncSlot()
    async def load_data_flowers_flavors(self, tbl):
        """
        Загрузка данных с таблицы flowers или flavors из бд sql Db.db. Срабатывает при нажатии на кнопку 'Загрузить'
        на вкладке "Цваеты" или "Букеты".
        """
        cur_tbl = tbl[1]
        data_flowers = await self.db.flowers_flavors_data(tbl[0])
        cur_tbl.setRowCount(0)

        for row_number, row_data in enumerate(data_flowers):
            cur_tbl.insertRow(row_number)
            for col_number, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                item.setTextAlignment(Qt.AlignHCenter)
                cur_tbl.setItem(row_number, col_number, item)

        self.ui.lbl_info_tbl.setText("Данные загружены")
        self.one_row_flag = True

    @asyncSlot()
    async def add_new_row(self, tbl):
        """
        Добавление новой строки.Срабатывает при нажатии на кнопку 'Добавить'
        Без сохранения данных можно добавить только одну строку, за это отвечает one_row_flag
        """
        cur_tbl = tbl[1]

        if self.one_row_flag:
            row_position = cur_tbl.rowCount()
            self.last_row = (await self.db.last_id(tbl[0]))[0]
            res = str((await self.db.last_id(tbl[0]))[0] + 1)
            cur_tbl.insertRow(row_position)
            cur_tbl.setItem(row_position, 0, QtWidgets.QTableWidgetItem(res))

            if tbl[0] == "composition":
                self.composition_widgets.append(ComboPickFlavor(self, self.dict_flower_id))
                cur_tbl.setCellWidget(row_position, 1, self.composition_widgets[-1])

            self.one_row_flag = False
        else:
            self.ui.lbl_info_tbl.setText('Сохраните таблицу')

    @asyncSlot()
    async def delete_row_flowers_flavors(self, tbl):
        """Удаление выбранной строки из таблицы flowers или flavors. Срабатывает при нажатии на кнопку 'Удалить'"""
        if tbl[1].rowCount() > 0 and tbl[1].currentRow() != -1:
            current_row = tbl[1].currentRow()
            if tbl[0] == "composition":
                del self.composition_widgets[current_row]
            tbl[1].removeRow(current_row)

    @asyncSlot()
    async def save_data_flowers_flavors(self, tbl):
        """Сохранение данных из таблицы flowers или flavors в таблицу sql.
        Срабатывает при нажатии на кнопку 'Сохранить'"""
        try:
            data = []

            for row in range(tbl[1].rowCount()):
                data.append([])
                if not tbl[1].item(row, 0).text().isdigit():
                    self.ui.lbl_info_tbl.setText('ID должен быть числом')
                    raise Exception

                data[row].append(tbl[1].item(row, 0).text())
                if tbl[0] == "flowers" or tbl[0] == "flavors":
                    data[row].append(tbl[1].item(row, 1).text())
                if tbl[0] == "flavors":
                    data[row].append(tbl[1].item(row, 2).text())
                elif tbl[0] == "composition":
                    data[row].append(self.dict_flavor_id[self.ui.combo_tbls.currentText()])
                    data[row].append(self.dict_flower_id[self.composition_widgets[row].currentText()])
                    data[row].append(tbl[1].item(row, 2).text())

            save_rows_count = await self.db.save_data(data, tbl[0])

            if tbl[0] == "flowers":
                await self.load_data_composition()
                self.flowers = await self.db.get_flowers()
                self.ui.combo_flowers.clear()
                self.ui.combo_flowers.addItems(self.flowers)
            elif tbl[0] == "flavors":
                await self.load_data_order()
                self.dict_flavor_id = await self.db.flavor_flowers_id(["id_flavor", "flavors"])
                self.ui.combo_tbls.clear()
                self.ui.combo_tbls.addItems(self.dict_flavor_id)
                await self.load_data_composition()

            self.ui.lbl_info_tbl.setText(f"Данные были сохранены: (кол-во: {save_rows_count})")
            self.one_row_flag = True

        except AttributeError:
            self.ui.lbl_info_tbl.setText('Заполните все поля корректно')

    @asyncSlot()
    async def load_data_order(self):
        """
        Загрузка данных з таблицы orders из бд sql Db.db. Срабатывает при нажатии на кнопку 'Загрузить'.
        """
        self.dict_flavor_id = await self.db.flavor_flowers_id(["id_flavor", "flavors"])
        self.widgets_mas.clear()
        data_orders = await self.db.orders_data()
        all_money = await self.db.all_money()
        all_money = f"Итоговая прибыль: {all_money[0]} руб."
        self.ui.lbl_cost.setText(all_money)
        self.ui.tbl.setRowCount(0)

        for row_number, row_data in enumerate(data_orders):
            self.ui.tbl.insertRow(row_number)
            self.widgets_mas.append([ComboPickFlavor(self, self.dict_flavor_id), DateEdit(self),
                                     DateEdit(self)])

            for col_number, col_data in enumerate(row_data):
                if col_number not in [4, 5, 6]:
                    self.ui.tbl.setItem(row_number, col_number, QtWidgets.QTableWidgetItem(str(col_data)))
                elif col_number == 4:
                    self.ui.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][0])
                    self.widgets_mas[row_number][0].setCurrentText(col_data)
                elif col_number == 5:
                    date = QDate.fromString(col_data, "yyyy-MM-dd")
                    self.ui.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][1])
                    self.widgets_mas[row_number][1].setDate(QDate(date))
                elif col_number == 6:
                    date = QDate.fromString(col_data, "yyyy-MM-dd")
                    self.ui.tbl.setCellWidget(row_number, col_number, self.widgets_mas[row_number][2])
                    self.widgets_mas[row_number][2].setDate(QDate(date))

        self.ui.lbl_info_tbl.setText("Данные загружены")
        self.one_row_flag = True

    @asyncSlot()
    async def list_flowers(self):
        """
        Формирование всего списка цветов для добавления в comboBox на вкладке "Фильтр"
        """
        self.min_date = self.ui.date_begin_flowers.date().toPyDate().strftime('%Y-%m-%d')
        self.max_date = self.ui.date_end_flowers.date().toPyDate().strftime('%Y-%m-%d')
        self.ui.list_flowers.clear()
        result_list = await self.db.list_flowers(self.ui.combo_flowers.currentText(), self.min_date, self.max_date)
        self.ui.list_flowers.addItems(result_list)

    @asyncSlot()
    async def save_data_order(self):
        """Сохранение данных из таблицы orders в таблицу sql. Срабатывает при нажатии на кнопку 'Сохранить'"""
        try:
            data = []

            for row in range(self.ui.tbl.rowCount()):
                data.append([])
                two_date = [self.widgets_mas[row][1].date().toPyDate().strftime('%Y-%m-%d'),
                            self.widgets_mas[row][2].date().toPyDate().strftime('%Y-%m-%d')]
                if not self.ui.tbl.item(row, 0).text().isdigit():
                    self.ui.lbl_info_tbl.setText('ID должен быть числом')
                    raise Exception
                if not two_date[0] <= two_date[1]:
                    self.ui.lbl_info_tbl.setText('Первая дата не может быть больше второй')
                    raise Exception

                data[row].append(self.ui.tbl.item(row, 0).text())
                data[row].append(self.ui.tbl.item(row, 1).text())
                data[row].append(self.ui.tbl.item(row, 2).text())
                data[row].append(self.ui.tbl.item(row, 3).text())
                data[row].append(self.dict_flavor_id[self.widgets_mas[row][0].currentText()])

                data[row].append(two_date[0])
                data[row].append(two_date[1])

            save_rows_count = await self.db.save_data_order(data)
            self.ui.lbl_info_tbl.setText(f"Данные были сохранены: (кол-во: {save_rows_count})")
            self.one_row_flag = True

        except AttributeError:
            self.ui.lbl_info_tbl.setText('Заполните все поля корректно')

    @asyncSlot()
    async def add_new_row_orders(self):
        """
        Добавление новой строки в таблицу orders.Срабатывает при нажатии на кнопку 'Добавить'
        Без сохранения данных можно добавить только одну строку, за это отвечает one_row_flag
        """
        if self.one_row_flag:
            row_position = self.ui.tbl.rowCount()
            res = str((await self.db.last_id_orders())[0] + 1)

            self.ui.tbl.insertRow(row_position)
            self.widgets_mas.append([ComboPickFlavor(self, self.dict_flavor_id), DateEdit(self), DateEdit(self)])

            self.ui.tbl.setItem(row_position, 0, QtWidgets.QTableWidgetItem(res))
            self.ui.tbl.setCellWidget(row_position, 4, self.widgets_mas[row_position][0])
            self.ui.tbl.setCellWidget(row_position, 5, self.widgets_mas[row_position][1])
            self.ui.tbl.setCellWidget(row_position, 6, self.widgets_mas[row_position][2])
            self.ui.tbl.setItem(row_position, 7, QtWidgets.QTableWidgetItem("-"))

            self.one_row_flag = False
        else:
            self.ui.lbl_info_tbl.setText('Сохраните таблицу')

    def delete_row(self):
        """Удаление выбранной строки. Срабатывает при нажатии на кнопку 'Удалить'"""
        if self.ui.tbl.rowCount() > 0 and self.ui.tbl.currentRow() != -1:
            current_row = self.ui.tbl.currentRow()
            self.ui.tbl.removeRow(current_row)
            del self.widgets_mas[current_row]
