from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui import Ui_MainWindow
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ---- TF2 figure prices ----
        self.red_prices = {
            "Scout": 285,
            "Soldier": 150,
            "Pyro": 250,
            "Demoman": 220,
            "Heavy": 150,
            "Engineer": 170,
            "Medic": 300,
            "Sniper": 230,
            "Spy": 135
        }

        self.blu_prices = {
            "Scout": 230,
            "Soldier": 110,
            "Pyro": 200,
            "Demoman": 180,
            "Heavy": 130,
            "Engineer": 150,
            "Medic": 240,
            "Sniper": 200,
            "Spy": 120
        }

        # connect signals
        self.ui.combo_class.currentIndexChanged.connect(self.update_price)
        self.ui.radio_red.clicked.connect(self.update_price)
        self.ui.radio_blu.clicked.connect(self.update_price)
        self.ui.radio_new.clicked.connect(self.update_price)
        self.ui.radio_used.clicked.connect(self.update_price)
        self.ui.input_budget.textChanged.connect(self.update_price)

        # set RED & NEW defaults
        self.ui.radio_red.setChecked(True)
        self.ui.radio_new.setChecked(True)

        # apply styling
        self.apply_style()

        # initialize price
        self.update_price()

    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f2f2f2;
            }

            QLabel {
                font-size: 14px;
            }

            QLineEdit, QComboBox {
                background: white;
                border: 1px solid #c4c4c4;
                border-radius: 6px;
                padding: 4px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #d64646;
                color: white;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #bb3a3a;
            }
        """)

    def update_price(self):
        class_name = self.ui.combo_class.currentText()

        # choose team
        use_red = self.ui.radio_red.isChecked()
        price = self.red_prices[class_name] if use_red else self.blu_prices[class_name]

        # used discount
        if self.ui.radio_used.isChecked():
            price = price / 2

        # show price in price box
        self.ui.input_price.setText(f"${price:.2f}")

        # check budget
        try:
            budget = float(self.ui.input_budget.text())
        except:
            self.ui.label_result.setText("Enter a valid budget.")
            return

        if budget >= price:
            self.ui.label_result.setText("YES, you can afford it!")
        else:
            self.ui.label_result.setText("NO, it's not in your budget.")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
