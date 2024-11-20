from PyQt6.QtWidgets import QLineEdit, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator

class CurrencyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)  # Alinear a la derecha
        self.setValidator(QDoubleValidator(0, 1_000_000_000, 2, self))  # Solo números y dos decimales
        self.textChanged.connect(self.format_currency)
        self.setText("0.00")  # Valor inicial formateado

    def format_currency(self):
        # Guardar la posición actual del cursor
        cursor_position = self.cursorPosition()
        
        # Eliminar caracteres no numéricos
        text = self.text().replace(",", "").replace("$", "").strip()
        if text:
            try:
                value = float(text)
                self.blockSignals(True)  # Evitar bucles recursivos
                formatted_text = f"${value:,.2f}"  # Formatear como moneda
                self.setText(formatted_text)
                self.blockSignals(False)
                
                # Ajustar la posición del cursor
                new_position = cursor_position + (len(formatted_text) - len(self.text()))
                self.setCursorPosition(max(0, min(len(formatted_text), new_position)))
            except ValueError:
                pass

    def focusInEvent(self, event):
        """Quitar el formato de moneda al enfocar, para edición más fácil."""
        text = self.text().replace(",", "").replace("$", "").strip()
        self.setText(text)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """Reaplicar el formato de moneda al perder el foco."""
        self.format_currency()
        super().focusOutEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    widget = CurrencyLineEdit()
    widget.setWindowTitle("Campo de Moneda")
    widget.show()
    app.exec()
