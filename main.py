import tkinter as tk
from PIL import Image, ImageTk
from pynput import mouse, keyboard as pykeyboard
import threading

# Путь к вашей картинке
IMAGE_PATH = "image.png"  # Замените на свой путь

# Флаг, чтобы избежать множественного открытия окон
image_shown = False


def show_image():
    global image_shown
    if image_shown:
        return
    image_shown = True

    root = tk.Tk()
    root.title("Image Overlay")

    # Открытие и изменение размера изображения (если нужно)
    img = Image.open(IMAGE_PATH)
    # img = img.resize((400, 300))  # Можно изменить размер
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=photo)
    label.image = photo  # Сохраняем ссылку, чтобы изображение не исчезло
    label.pack()

    # Настройки окна: поверх всех окон, без рамки
    root.attributes("-topmost", True)
    root.overrideredirect(True)  # Без рамки и заголовка

    # Центрирование окна
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = img.width
    window_height = img.height
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def close_window(event=None):
        root.destroy()
        global image_shown
        image_shown = False

    # Закрытие при клике по окну или Esc
    root.bind("<Escape>", close_window)
    root.bind("<Button-1>", close_window)

    root.mainloop()


# Обработчик нажатий клавиш
def on_key_press(key):
    try:
        if key == pykeyboard.Key.f9:  # Нажата F9
            show_image()
    except AttributeError:
        pass


# Обработчик кликов мыши
def on_click(x, y, button, pressed):
    if pressed:  # Только при нажатии (not release)
        show_image()


# Запуск листенеров в потоках
def start_keyboard_listener():
    with pykeyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


def start_mouse_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == "__main__":
    print("Программа запущена. Нажмите F9 или кликните мышкой, чтобы показать изображение.")

    # Запускаем слушателей в отдельных потоках
    threading.Thread(target=start_keyboard_listener, daemon=True).start()
    threading.Thread(target=start_mouse_listener, daemon=True).start()

    # Основной цикл для поддержания работы программы
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nПрограмма остановлена.")