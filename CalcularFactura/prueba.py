from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QLabel, QComboBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt

class PriceCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Precios con Cuotas")
        self.setGeometry(200, 200, 700, 500)

        # Configuración de recargos por cuota
        self.quota_options = {
            3: 10.0,   # 10% para 3 cuotas
            6: 14.4,  # 14,4% para 6 cuotas
            12: 25.4  # 25,4% para 12 cuotas
        }

        # Crear widgets
        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText("Precio de Contado")
        
        self.cash_payment_input = QLineEdit(self)
        self.cash_payment_input.setPlaceholderText("Monto de Contado")
        
        self.add_quota_button = QPushButton("Agregar Cuota", self)
        self.add_quota_button.clicked.connect(self.add_quota)
        
        self.calculate_button = QPushButton("Calcular Precio Final", self)
        self.calculate_button.clicked.connect(self.calculate_final_price)
        
        self.result_label = QLabel("Precio Final: ", self)
        
        self.quota_table = QTableWidget(0, 4, self)
        self.quota_table.setHorizontalHeaderLabels(["Número de Cuotas", "Monto ($)", "Recargo (%)", "Valor a cobrar ($)"])

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.price_input)
        layout.addWidget(self.cash_payment_input)
        layout.addWidget(self.add_quota_button)
        layout.addWidget(self.quota_table)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.result_label)

        container = QDialog()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_quota(self):
        # Añadir una fila a la tabla para seleccionar cuotas, ingresar monto y mostrar recargo
        row_position = self.quota_table.rowCount()
        self.quota_table.insertRow(row_position)
        
        # Crear un combo box para seleccionar el número de cuotas
        quota_combo = QComboBox()
        for quota in self.quota_options.keys():
            quota_combo.addItem(f"{quota} cuotas", quota)
        quota_combo.currentIndexChanged.connect(lambda: self.update_recargo(row_position))
        self.quota_table.setCellWidget(row_position, 0, quota_combo)

        # Crear un campo para ingresar el monto
        amount_input = QDoubleSpinBox()
        amount_input.setMaximum(1_000_000)  # Valor máximo razonable
        self.quota_table.setCellWidget(row_position, 1, amount_input)

        # Mostrar el recargo correspondiente
        recargo_item = QTableWidgetItem(f"{self.quota_options[3]} %")
        recargo_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.quota_table.setItem(row_position, 2, recargo_item)

        # Mostrar el valor a cobrar
        price_charge_item = QTableWidgetItem(f"$0.00")
        price_charge_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.quota_table.setItem(row_position, 3, price_charge_item)


    def update_recargo(self, row):
        # Actualizar el recargo en la tabla cuando cambie el número de cuotas
        combo = self.quota_table.cellWidget(row, 0)
        if combo is not None:
            quota = combo.currentData()
            recargo = self.quota_options.get(quota, 0)
            self.quota_table.setItem(row, 2, QTableWidgetItem(f"{recargo} %"))
            amount_widget = self.quota_table.cellWidget(row, 1)
            recargo = self.quota_options.get(quota, 0) / 100
            assigned_amount = amount_widget.value()
            quota_value_with_surcharge = assigned_amount * (1 + recargo)
            self.quota_table.setItem(row, 3, QTableWidgetItem(f"${round(quota_value_with_surcharge,4)}"))
            

    def calculate_final_price(self):
        try:
            # Leer los datos de entrada
            price = float(self.price_input.text())
            cash_payment = float(self.cash_payment_input.text())
            if cash_payment > price:
                self.result_label.setText("El monto de contado no puede superar el precio.")
                return

            
            total_financed = price - cash_payment
            assigned_total = 0
            final_price = cash_payment

            # Procesar cada cuota
            for row in range(self.quota_table.rowCount()):
                combo = self.quota_table.cellWidget(row, 0)
                amount_widget = self.quota_table.cellWidget(row, 1)
                if combo is not None and amount_widget is not None:
                    quota = combo.currentData()
                    assigned_amount = amount_widget.value()
                    assigned_total += assigned_amount

                    if assigned_total > total_financed:
                        self.result_label.setText("La suma de los montos asignados excede el total a financiar.")
                        return
                    
                    recargo = self.quota_options.get(quota, 0) / 100
                    quota_value_with_surcharge = assigned_amount * (1 + recargo)
                    price_charge_item = QTableWidgetItem(f"${round(quota_value_with_surcharge,4)}")
                    price_charge_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    self.quota_table.setItem(row, 3,price_charge_item)
                    final_price += quota_value_with_surcharge

            if assigned_total < total_financed:
                faltante = float(total_financed - assigned_total)
                self.result_label.setText(f"Falta de financiar: ${faltante:.2f}")
                return
            
            self.result_label.setText(f"Precio Final: ${final_price:.2f}")
        
        except ValueError:
            self.result_label.setText("Por favor, ingrese valores válidos.")

if __name__ == "__main__":
    app = QApplication([])
    window = PriceCalculator()
    window.show()
    app.exec()
