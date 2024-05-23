import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, \
    QMessageBox, QFileDialog, QDialog, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
import numpy as np
import matplotlib.pyplot as plt
import csv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ввод данных для графика")
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                font-size: 14px;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QVBoxLayout()

        self.x_label = QLabel("Введите данные для оси X (через запятую):")
        layout.addWidget(self.x_label)

        self.x_edit = QLineEdit()
        layout.addWidget(self.x_edit)

        self.y_label = QLabel("Введите данные для оси Y (через запятую):")
        layout.addWidget(self.y_label)

        self.y_edit = QLineEdit()
        layout.addWidget(self.y_edit)

        self.plot_button = QPushButton("Построить график")
        self.plot_button.clicked.connect(self.accept)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def get_data(self):
        return self.x_edit.text(), self.y_edit.text()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Графическое приложение")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #e6e6e6;
                font-family: Arial, sans-serif;
            }
            QMenuBar {
                background-color: #333;
                color: white;
                font-size: 16px;
            }
            QMenuBar::item {
                background-color: #333;
                color: white;
            }
            QMenuBar::item::selected {
                background-color: #555;
            }
            QMenu {
                background-color: #333;
                color: white;
            }
            QMenu::item::selected {
                background-color: #555;
            }
        """)

        self.create_menu()
        self.show_message()

    def set_view(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

    def show_message(self):
        welcome_label = QLabel(
            "Qt домашка по уппрпо!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 18px; color: #333; padding: 20px;")
        self.setCentralWidget(welcome_label)

    def create_menu(self):
        main_menu = self.menuBar()

        file_menu = main_menu.addMenu("Файл")
        graph_menu = main_menu.addMenu("Готовые графики")
        custom_graph_menu = main_menu.addMenu("Построить график")
        additional_menu = main_menu.addMenu("Дополнительно")

        plot_linear_action = QAction("Линейный график", self)
        plot_linear_action.triggered.connect(self.plot_linear_graph)
        graph_menu.addAction(plot_linear_action)

        plot_sin_action = QAction("График синуса", self)
        plot_sin_action.triggered.connect(self.plot_sin_graph)
        graph_menu.addAction(plot_sin_action)

        plot_cos_action = QAction("График косинуса", self)
        plot_cos_action.triggered.connect(self.plot_cos_graph)
        graph_menu.addAction(plot_cos_action)

        plot_quad_action = QAction("Квадратичный график", self)
        plot_quad_action.triggered.connect(self.plot_quadratic_graph)
        graph_menu.addAction(plot_quad_action)

        plot_exp_action = QAction("Экспоненциальный график", self)
        plot_exp_action.triggered.connect(self.plot_exponential_graph)
        graph_menu.addAction(plot_exp_action)

        plot_log_action = QAction("Логарифмический график", self)
        plot_log_action.triggered.connect(self.plot_logarithmic_graph)
        graph_menu.addAction(plot_log_action)

        plot_scatter_action = QAction("Точечный график", self)
        plot_scatter_action.triggered.connect(self.plot_scatter_graph)
        graph_menu.addAction(plot_scatter_action)

        save_action = QAction(QIcon("save.png"), "Сохранить график", self)
        save_action.triggered.connect(self.save_graph)
        file_menu.addAction(save_action)

        export_data_action = QAction("Экспортировать данные в CSV", self)
        export_data_action.triggered.connect(self.export_data_to_csv)
        file_menu.addAction(export_data_action)

        load_image_action = QAction("Загрузить график", self)
        load_image_action.triggered.connect(self.load_image)
        file_menu.addAction(load_image_action)

        custom_plot_action = QAction("По своим данным", self)
        custom_plot_action.triggered.connect(self.show_custom_plot_dialog)
        custom_graph_menu.addAction(custom_plot_action)

        random_plot_action = QAction("Случайный график", self)
        random_plot_action.triggered.connect(self.plot_random_graph)
        additional_menu.addAction(random_plot_action)

        reset_view_action = QAction("Сбросить вид", self)
        reset_view_action.triggered.connect(self.show_message)
        additional_menu.addAction(reset_view_action)

    def show_custom_plot_dialog(self):
        dialog = DataInputDialog(self)
        if dialog.exec_():
            x_data, y_data = dialog.get_data()
            self.plot_custom_graph(x_data, y_data)

    def plot_custom_graph(self, x_data, y_data):
        self.set_view()
        try:
            x_list = [float(x) for x in x_data.split(",")]
            y_list = [float(y) for y in y_data.split(",")]
            if len(x_list) != len(y_list):
                QMessageBox.warning(self, "Ошибка", "Длины списков данных для X и Y должны быть одинаковыми.")
                return
            self.plot_graph(x_list, y_list, "Ваш график", color='b')  # Синий цвет
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите числовые данные через запятую.")

    def plot_linear_graph(self):
        self.set_view()
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        self.plot_graph(x, y, "Линейный график", color='r')  # Красный цвет

    def plot_sin_graph(self):
        self.set_view()
        x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        y = np.sin(x)
        self.plot_graph(x, y, "График синуса", color='g')  # Зеленый цвет

    def plot_cos_graph(self):
        self.set_view()
        x = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        y = np.cos(x)
        self.plot_graph(x, y, "График косинуса", color='b')  # Синий цвет

    def plot_quadratic_graph(self):
        self.set_view()
        x = np.linspace(-10, 10, 100)
        y = x ** 2
        self.plot_graph(x, y, "Квадратичный график", color='m')  # Пурпурный цвет

    def plot_exponential_graph(self):
        self.set_view()
        x = np.linspace(0, 10, 100)
        y = np.exp(x)
        self.plot_graph(x, y, "Экспоненциальный график", color='c')  # Голубой цвет

    def plot_logarithmic_graph(self):
        self.set_view()
        x = np.linspace(0.1, 10, 100)
        y = np.log(x)
        self.plot_graph(x, y, "Логарифмический график", color='y')  # Желтый цвет

    def plot_scatter_graph(self):
        self.set_view()
        x = np.random.rand(100)
        y = np.random.rand(100)
        self.plot_scatter(x, y, "Точечный график", color='k')  # Черный цвет

    def plot_random_graph(self):
        self.set_view()
        x = np.linspace(0, 10, 100)
        y = np.random.rand(100)
        self.plot_graph(x, y, "Случайный график", color='orange')  # Оранжевый цвет

    def plot_graph(self, x, y, title, color='b'):
        self.set_view()
        self.scene.clear()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, color=color)  # Изменение цвета графика
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)

        canvas = FigureCanvas(fig)
        canvas.draw()

        self.scene.addWidget(canvas)

    def plot_scatter(self, x, y, title, color='b'):
        self.set_view()
        self.scene.clear()

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(x, y, color=color)  # Изменение цвета точек
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(title)

        canvas = FigureCanvas(fig)
        canvas.draw()

        self.scene.addWidget(canvas)

    def save_graph(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить график", "",
                                                   "PNG files (*.png);;JPEG files (*.jpg *.jpeg)")
        if file_name:
            plt.savefig(file_name)
            QMessageBox.information(self, "Успех", "График успешно сохранен!")

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить график", "", "Image files (*.png *.jpg *.jpeg)")
        if file_name:
            self.set_view()
            pixmap = QPixmap(file_name)
            label = QLabel()
            label.setPixmap(pixmap)
            self.scene.addWidget(label)
            QMessageBox.information(self, "Успех", "График успешно загружен!")

    def export_data_to_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Экспортировать данные", "",
                                                   "CSV files (*.csv)")
        if file_name:
            x = np.linspace(0, 10, 100)
            y = np.random.rand(100)
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["X", "Y"])
                writer.writerows(zip(x, y))
            QMessageBox.information(self, "Успех", "Данные успешно экспортированы в CSV!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Set the Fusion style for a modern look
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
