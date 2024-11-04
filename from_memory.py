# виджет treeview
# Выровнял размер окна root

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sq
import random, os, sys


class Main:
    def __init__(self, root):
        self.root = root
        self.db = db        # Экземпляр класса DB для sql запросов.
        self.count = 0
        self.ls_translates = []
        self.tupple_lists = self.random_lists()     # Кортеж двух списков перемешанных значений
        self.init_main()

    # Графика окна root
    def init_main(self):
        self.ls_word = self.tupple_lists[0]     # список: иностранные слова
        self.ls_answer = self.tupple_lists[1]   # список: правильный перевод
        self.label_translate = tk.Label(self.root, text='Перевод')
        self.label_translate.place(x=30, y=21)
        # Принимает перевод пользователя, виджет настроен на клавишу Enter.
        self.entry_translate = ttk.Entry(self.root, width=30)
        self.entry_translate.place(x=120, y=50)
        self.entry_translate.focus()

        # Подача иностранного слова/выражения для перевода.
        while self.count < len(self.ls_word):
            self.label_word = tk.Label(self.root, text=self.ls_word[self.count], font='Arial 11 bold')
            self.label_word.place(x=120, y=20)
            break

        # Отправка перевода пользователя в виджет Treeview (key_translate_func).
        # Настроена на клавишу Enter. Также можно отправить кнопкой "да".
        btn_yes = tk.Button(self.root, text='да')
        btn_yes.place(x=120, y=80)
        btn_yes.bind('<Button-1>', lambda event: self.key_translate_func(self.entry_translate,))
        self.entry_translate.bind('<Return>', lambda event: self.key_translate_func(self.entry_translate,))

        # Кнопка "Начать снова" (new_start)
        btn_new_start = tk.Button(self.root, text='Начать снова', command=self.new_start)
        btn_new_start.place(x=282, y=80)

        # Кнопка "Стоп" (stop_translate). Можно посмотреть результаты теста в процессе
        # подачи иностранных слов. По закрытии "окна результатов (виджет Treeview)" можно
        # продолжить тест с места остановки.
        btn_stop = tk.Button(self.root, text='Стоп', command=self.stop_translate)
        btn_stop.place(x=190, y=80)

    # Отправка перевода пользователя в виджет Treeview.
    def key_translate_func(self, event):
        try:
            self.ls_translates.append(self.ls_word[self.count])
            self.ls_translates.append(self.entry_translate.get())
            self.ls_translates.append(self.ls_answer[self.count])
            self.count += 1
            if self.count < len(self.ls_word):
                self.label_word.destroy()
                self.entry_translate.delete(0, tk.END)

                self.init_main()
            # Если закончился список иностранных слов, автоматически открывается
            # "окно результатов (виджет Treeview)"
            else:
                self.view_results()
        except IndexError:
            print('вопросы закончились')

    # Функция перемешивает словарь "иностранный - перевод" и возвращает два списка:
    # "слово", "перевод"
    def random_lists(self):
        # sql запрос
        self.db.cur.execute('''SELECT word, meaning FROM dictionary''')
        self.dictionary = self.db.cur.fetchall()
        random.shuffle(self.dictionary)     # перемешивание
        self.ls_key_dictionary = []
        self.ls_value_dictionary = []
        for item in self.dictionary:    # новый список кортежей
            # Условие фильтрует строку: "начало новой буквы" (буква и точка).
            if len(item[0]) > 1 and len(item[1]) > 1:
                self.ls_key_dictionary.append(item[0])
                self.ls_value_dictionary.append(item[1])
        
        return self.ls_key_dictionary, self.ls_value_dictionary

    # Старт нового теста из окна root (динамический перезапуск программы).
    def new_start(self):
        self.root.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    # Открытие "окна результатов (виджет Treeview)" класс ViewResults
    def view_results(self):
        ViewResults(self.ls_translates)     # ls_translates - "список переводов"

    # Открытие "окна результатов (виджет Treeview)" класс ViewResults
    def stop_translate(self):
        self.view_results()


# Класс DB, создаёт/открывает базу данных (БД)
class DB:
    with sq.connect('dictionary.db') as conn:
        cur = conn.cursor()


# Класс ViewResults - показать результаты. Класс наследуется от объекта Toplevel, создаёт
# дочернее окно. Использует виджет TreeView. Принимает "список переводов"
# (иностранное слово, перевод пользователя, правильный перевод).
class ViewResults(tk.Toplevel):
    def __init__(self, translates):
        super().__init__()
        self.ls_translates = translates     # (иностранное слово, перевод пользователя, правильный перевод)
        self.title = ('Перевод по памяти')
        self.geometry('915x950+600+0')
        self.start_print()      # Открывает таблицу.

        self.grab_set()

    # Открывает таблицу с результатами теста.
    def start_print(self):
        self.message = tk.Label(self, text='')  # Просто отступ от заголовка.
        self.message.grid(row=1, column=0, columnspan=3, sticky=tk.W + tk.E)
        # Переопределяем слов и переводов в список кортежей
        count = 0
        step = 3
        self.ls_tupples = []
        while count < len(self.ls_translates):
            word = self.ls_translates[count]
            my_tr = self.ls_translates[count + 1]
            tr = self.ls_translates[count + 2]
            tupple_translate = (word, my_tr, tr)
            self.ls_tupples.append(tupple_translate)
            count += step

        self.tree = ttk.Treeview(self, columns=('word', 'my_tr', 'tr'), height=45, show='headings')

        self.tree.column('word', width=300)
        self.tree.column('my_tr', width=300)
        self.tree.column('tr', width=300)
        self.tree.heading('word', text='слово')
        self.tree.heading('my_tr', text='мой перевод')
        self.tree.heading('tr', text='перевод')

        self.tree.grid(row=2, column=0, columnspan=3)

        self.scroll = tk.Scrollbar(self, command=self.tree.yview)
        self.scroll.grid(row=2, column=4, sticky='ns')
        self.tree.configure(yscrollcommand=self.scroll.set)

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.ls_tupples]


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    root.title("Перевод по памяти")
    root.geometry('500x180+450+200')
    root.mainloop()
