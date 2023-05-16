import tkinter as tk
from tkinter import filedialog
from LexicalAnalizator import lexical_analizator
from Runtime.Language_.language import Language
from tkinter import scrolledtext

def open_window_1():
    window_1 = tk.Toplevel(root)
    window_1.title("Window 1")
    window_1.geometry("1000x1000")

    text_labels = ["Исходный код на C#", "Результат работы лексич. анализатора", "R", "W", "O", "I", "C", "N"]
    text_entries = []

    def open_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                lexical_analizator(file_path)
                content = file.read()
                text_entries[0].delete("1.0", tk.END)  # Удаление предыдущего текста
                text_entries[0].insert(tk.END, content)

    def execute_function():
        tokens_info = ""
        with open("tokens.txt", "r") as file:
            tokens = file.read()
            text_entries[1].delete("1.0", tk.END)  # Удаление предыдущего текста
            text_entries[1].insert(tk.END, tokens)
        for name in text_labels[2:8]:
            with open('%s.json' % name, 'r') as read_file:
                tokens_info = read_file.read()
                text_entries[text_labels.index(name)].delete("1.0", tk.END)
                text_entries[text_labels.index(name)].insert(tk.END, tokens_info)

    # Создание верхней панели с кнопками
    frame_buttons = tk.Frame(window_1)
    frame_buttons.pack(side=tk.TOP)

    button_load_file = tk.Button(frame_buttons, text="Загрузить файл", command=open_file)
    button_load_file.pack(side=tk.LEFT)

    button_execute_function = tk.Button(frame_buttons, text="Лексический анализатор", command=execute_function)
    button_execute_function.pack(side=tk.LEFT)

    button_open_window_2 = tk.Button(frame_buttons, text="Перейти к ОПЗ", command=open_window_2)
    button_open_window_2.pack(side=tk.LEFT)

    # Создание заголовков над текстовыми блоками
    frame_labels = tk.Frame(window_1)
    frame_labels.pack()
    for label_text in text_labels[0:2]:
        label = tk.Label(frame_labels, text=label_text)
        label.pack(side=tk.LEFT)

    # Создание первой строки с двумя текстовыми блоками
    frame_row1 = tk.Frame(window_1)
    frame_row1.pack()
    for _ in range(2):
        text_box = scrolledtext.ScrolledText(frame_row1, width=60, height=15)
        text_box.pack(side=tk.LEFT)
        text_entries.append(text_box)

    # Создание второй строки с тремя текстовыми блоками
    frame_labels = tk.Frame(window_1)
    frame_labels.pack()
    for label_text in text_labels[2:5]:
        label = tk.Label(frame_labels, text=label_text)
        label.pack(side=tk.LEFT)

    frame_row2 = tk.Frame(window_1)
    frame_row2.pack()
    for _ in range(3):
        text_box = scrolledtext.ScrolledText(frame_row2, width=20, height=20)
        text_box.pack(side=tk.LEFT)
        text_entries.append(text_box)

    # Создание третьей строки с тремя текстовыми блоками
    frame_labels = tk.Frame(window_1)
    frame_labels.pack()
    for label_text in text_labels[5:8]:
        label = tk.Label(frame_labels, text=label_text)
        label.pack(side=tk.LEFT)

    frame_row3 = tk.Frame(window_1)
    frame_row3.pack()
    for _ in range(3):
        text_box = scrolledtext.ScrolledText(frame_row3, width=20, height=20)
        text_box.pack(side=tk.LEFT)
        text_entries.append(text_box)


def open_window_2():
    window_2 = tk.Toplevel()
    window_2.title("Window 2")
    window_2.geometry("1000x800")
    text_labels = ["Исходный код на C#", "ОПЗ"]
    text_entries = []

    def opz_function():
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                lexical_analizator(file_path)
                content = file.read()
                text_entries[0].delete("1.0", tk.END)  # Удаление предыдущего текста
                text_entries[0].insert(tk.END, content)

        with open("tokens.txt", "r") as file:
            tokens = file.read()
            text_entries[0].delete("1.0", tk.END)  # Удаление предыдущего текста
            text_entries[0].insert(tk.END, tokens)
            text_entries[1].delete("1.0", tk.END)

        print(content)
        (Language.using_rpn(content))
        with open('opz.txt', 'r') as file:
            opz_text = file.read()
            text_entries[1].insert(tk.END, opz_text)

    frame_buttons = tk.Frame(window_2)
    frame_buttons.pack(side=tk.TOP)

    button_load_file = tk.Button(frame_buttons, text="Загрузить файл с исходным кодом", command=opz_function)
    button_load_file.pack(side=tk.LEFT)

    # Создание заголовков над текстовыми блоками
    frame_labels = tk.Frame(window_2)
    frame_labels.pack()
    for label_text in text_labels[0:2]:
        label = tk.Label(frame_labels, text=label_text)
        label.pack(side=tk.LEFT)

    # Создание первой строки с двумя текстовыми блоками
    frame_row1 = tk.Frame(window_2)
    frame_row1.pack()
    for _ in range(2):
        text_box = scrolledtext.ScrolledText(frame_row1, width=60, height=40)
        text_box.pack(side=tk.LEFT)
        text_entries.append(text_box)


def open_window_3():
    window_3 = tk.Toplevel(root)
    window_3.title("Window 3")
    window_3.geometry("1000x1000")
    text_labels = ["Исходный код на C#", "Код на Python"]
    text_entries = []

    def opz_function():
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                lexical_analizator(file_path)
                content = file.read()
                text_entries[0].delete("1.0", tk.END)  # Удаление предыдущего текста
                text_entries[0].insert(tk.END, content)
                text_entries[1].delete("1.0", tk.END)

        print(content)
        (Language.get_python_code(content))
        with open('py_code.py', 'r') as file:
            py_code = file.read()
            text_entries[1].insert(tk.END, py_code)

    frame_buttons = tk.Frame(window_3)
    frame_buttons.pack(side=tk.LEFT)

    button_load_file = tk.Button(frame_buttons, text="Загрузить файл \n с исходным кодом на C#", command=opz_function, height=6, width=30, background="#7b68ee")
    button_load_file.pack(side=tk.LEFT)

    # Создание заголовков над текстовыми блоками
    frame_labels = tk.Frame(window_3)
    frame_labels.pack()
    label = tk.Label(frame_labels, text=text_labels[0])
    label.pack(side=tk.LEFT)

    # Создание первой строки с двумя текстовыми блоками
    frame_row1 = tk.Frame(window_3)
    frame_row1.pack()
    for _ in range(1):
        text_box = scrolledtext.ScrolledText(frame_row1, width=70, height=30)
        text_box.pack(side=tk.LEFT)
        text_entries.append(text_box)

    # Создание заголовков над текстовыми блоками
    frame_labels = tk.Frame(window_3)
    frame_labels.pack()
    label = tk.Label(frame_labels, text=text_labels[1])
    label.pack(side=tk.LEFT)

    # Создание первой строки с двумя текстовыми блоками
    frame_row1 = tk.Frame(window_3)
    frame_row1.pack()
    for _ in range(1):
        text_box = scrolledtext.ScrolledText(frame_row1, width=70, height=30)
        text_box.pack(side=tk.LEFT)
        text_entries.append(text_box)

    # frame_labels = tk.Frame(window_3)
    # frame_labels.pack()
    # label = tk.Label(frame_labels, text=text_labels[2])
    # label.pack(side=tk.LEFT)
    #
    # # Создание первой строки с двумя текстовыми блоками
    # frame_row1 = tk.Frame(window_3)
    # frame_row1.pack()
    # for _ in range(2):
    #     text_box = scrolledtext.ScrolledText(frame_row1, width=60, height=40)
    #     text_box.pack(side=tk.LEFT)
    #     text_entries.append(text_box)


# Создание главного окна
root = tk.Tk()
root.title("Main Window")
root.geometry("400x400")

# Кнопки для открытия окон
button_open_window_1 = tk.Button(root, text="Лексический анализатор", command=open_window_1, height=6, width=50, background="white")
button_open_window_1.pack()

button_open_window_2 = tk.Button(root, text="ОПЗ", command=open_window_2, height=6, width=50, background="#00fa9a")
button_open_window_2.pack()

button_open_window_3 = tk.Button(root, text="Транслятор", command=open_window_3, height=6, width=50, background="#0bda51")
button_open_window_3.pack()

button_open_window_4 = tk.Button(root, text="Синтаксический анализатор", command=open_window_3, height=6, width=50, background="#8000ff")
button_open_window_4.pack()
# Запуск главного цикла обработки событий
root.mainloop()
