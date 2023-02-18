from PyQt5.QtWidgets import QComboBox


class ComboPickFlavor(QComboBox):
    """Класс ComboPickFlavor переобределяет родительский класс QComboBox , для назначения своих стилей
    parent: OrderSystem.OrderSystem
        класс OrderSystem
    id_flavors: dict
        словарь, в котором ключ: название букета, значение: id букета
    """
    def __init__(self, parent, id_flavors):
        super().__init__(parent)
        self.addItems(list(id_flavors.keys()))
        self.setStyleSheet("""QComboBox {
                            font: 15pt "Microsoft YaHei UI Light";
                            font-weight: bold;
                            background-color: #fff;
                            border: none;
                            }""")
