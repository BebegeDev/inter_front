from PyQt6.QtWidgets import QApplication, QLCDNumber, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        lcd_number = QLCDNumber(self)
        lcd_number.setDigitCount(4)
        layout.addWidget(lcd_number)

        # Установка стилей для изменения цвета цифр
        style_sheet = """
            QLCDNumber {
                color: red;  /* Устанавливаем желаемый цвет цифр */
            }
        """
        lcd_number.setStyleSheet(style_sheet)

        lcd_number.display(1234)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication([])
    window = MyWidget()
    window.show()
    app.exec()