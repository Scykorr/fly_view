import sys
import keyboard
import pyautogui
from PySide6 import QtWidgets, QtGui, QtCore
# from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QTimer, QObject, Slot, QMetaObject


# Путь к вашей картинке
IMAGE_PATH = r"marker.png"

last_window = None


def show_image_at_mouse():
    global last_window

    x, y = pyautogui.position()

    app = QtWidgets.QApplication.instance()
    if not app:
        return

    if last_window:
        last_window.close()
        last_window = None

    window = QtWidgets.QWidget()
    window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    window.setAttribute(Qt.WA_TranslucentBackground)

    label = QtWidgets.QLabel(window)
    pixmap = QtGui.QPixmap(IMAGE_PATH)

    if pixmap.isNull():
        print("❌ Не удалось загрузить изображение")
        return

    label.setPixmap(pixmap)
    window.resize(pixmap.size())

    screen_width, screen_height = pyautogui.size()
    pos_x = max(0, min(x - pixmap.width() // 2, screen_width - pixmap.width()))
    pos_y = max(0, min(y - pixmap.height() // 2, screen_height - pixmap.height()))

    window.move(pos_x, pos_y)

    def close_window():
        window.close()
        global last_window
        last_window = None

    def mouse_event(event):
        close_window()

    def key_event(event):
        if event.key() == Qt.Key_Escape:
            close_window()

    window.mousePressEvent = mouse_event
    window.keyPressEvent = key_event

    window.show()
    QtCore.QTimer.singleShot(1000, close_window)  # Автоматическое закрытие через 1 секунды

    last_window = window


class GlobalHotkeyHandler(QtCore.QObject):
    @Slot()
    def on_f2(self):
        QMetaObject.invokeMethod(self, "show_image", Qt.QueuedConnection)

    @Slot()
    def show_image(self):
        show_image_at_mouse()


def exit_on_esc():
    print("🚪 Нажата клавиша Esc. Завершение работы.")
    app = QtWidgets.QApplication.instance()
    if app:
        app.quit()


# Основной запуск
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # ⬅️ Вот ключевой момент!

    # Создаем и прячем основное окно, чтобы GUI не закрылся сам
    main_window = QtWidgets.QWidget()
    main_window.hide()

    handler = GlobalHotkeyHandler()

    print("🟢 Программа запущена. Нажмите F2 для показа изображения.")
    print("ℹ️ Нажмите Esc для завершения работы.")

    keyboard.add_hotkey('F2', handler.on_f2)
    keyboard.add_hotkey('Esc', exit_on_esc)

    try:
        sys.exit(app.exec())
    except Exception as e:
        print("🔴 Ошибка:", e)