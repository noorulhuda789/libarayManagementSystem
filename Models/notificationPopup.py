from PyQt5.QtWidgets import QMessageBox


class NotificationPopup(QMessageBox):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok)

        self.setStyleSheet(
            """
            QMessageBox {
                background-color: #ffffff;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 1);
                
            }
            QMessageBox QLabel {
                color: #000000;
                background-color: rgba(0, 0, 0, 0);
                
            }
            QMessageBox QPushButton {
                color: #000000;
                background-color: rgba(0, 0, 0, 0);
            }
            QMessageBox QFrame {
                background-color: rgba(0, 0, 0, 0);
            }
            """
        )
