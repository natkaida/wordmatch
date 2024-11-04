# wordmatch + scroll + поиск в правой колонке
# окно entry, выделяет красным

from tkinter import ttk
from tkinter import *
import random, os
import sqlite3
from tkinter import messagebox


class Match:
    db_name = 'dictionary.db'

    def __init__(self, window):

        self.wind = window
        self.wind.title('Учим слова')
        self.eng, self.trans = str(), str()
        # Виджет для ввода поиска в правой колонке,
        # запуск поиска настроен на клавишу "Enter"
        self.entry_search = Entry(background='white')
        self.entry_search.grid(row=1, column=1)
        self.entry_search.bind('<Return>', lambda event: self.search_translate(self.entry_search))

        self.message = Label(text='', fg='red')
        self.message.grid(row=1, column=0, sticky=W + E)
        # правая и левая колонки
        self.left = Listbox(height=44, exportselection=False, activestyle='none', selectbackground='yellow')
        self.left.grid(row=2, column=0)
        self.right = Listbox(height=44, activestyle='none')
        self.right.grid(row=2, column=1)
        self.scroll = Scrollbar(orient=VERTICAL)
        self.scroll.grid(row=2, column=2, sticky='ns')
        self.scroll.config(command=self.right.yview)
        self.right.config(yscrollcommand=self.scroll.set)

        self.right.bind("<<ListboxSelect>>", self.callback_right)
        self.left.bind("<<ListboxSelect>>", self.callback_left)
        # назначение команд кнопкам программы и х-кнопке окна
        ttk.Button(text="Начать сначала", command=self.restart_program).grid(row=4, column=1, sticky=W + E)
        ttk.Button(text="Редактировать", command=self.run_edit).grid(row=4, column=0, sticky=W + E)
        self.wind.protocol("WM_DELETE_WINDOW", self.on_exit)
        # заполняем колонки словами
        self.get_words()

    #  закрытие программы по клику кнопки 'х'
    def on_exit(self):
        if messagebox.askyesno("Выйти", "Закрыть программу?"):
            self.wind.destroy()

    #  подключение к базе и передача запроса
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # запрос на извлечение всех существующих записей из базы в алфавитном порядке
    def get_words(self):
        query = 'SELECT * FROM dictionary ORDER BY word DESC'
        db_rows = self.run_query(query)
        # формирование словаря из перемешанных в случайном порядке слов и их значений
        lst_left, lst_right = [], []
        for row in db_rows:
            lst_left.append(row[1])
            lst_right.append(row[2])
        random.shuffle(lst_left)
        random.shuffle(lst_right)
        self.dic = dict(zip(lst_left, lst_right))
        # заполнение правой и левой колонок
        for k, v in self.dic.items():
            if len(k) > 1:
                self.left.insert(END, k)
            if len(v) > 1:
                self.right.insert(END, v)

    # обработка клика по словам в левой колонке
    def callback_left(self, event):
        self.message['text'] = ''
        if not event.widget.curselection():
            return
        # извлечение из базы значения выделенного слова
        w = event.widget
        idx = int(w.curselection()[0])
        self.eng = w.get(idx)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            sqlite_select_query = 'SELECT * from dictionary WHERE word = ?'
            cursor.execute(sqlite_select_query, (self.eng,))
            record = cursor.fetchone()
            self.trans = record[2]

    # обработка клика в правой колонке
    def callback_right(self, event1):
        self.message['text'] = ''
        if not event1.widget.curselection():
            return
        self.w_right = event1.widget
        idx = int(self.w_right.curselection()[0])
        click = self.w_right.get(idx)
        # если выбранное слово является правильным переводом, удаляем и оригинал, и значение
        if click == self.trans:
            self.right.delete(ANCHOR)
            self.left.delete(ANCHOR)
        # сообщаем о неверном значении
        else:
            self.message['text'] = 'Неправильно'
            self.right.selection_clear(0, END)

    # загружаем окно и скрипт редактирования словаря
    def run_edit(self):
        os.system('edit_dictionary.py')

    # перезапуск программы
    def restart_program(self):
        self.message['text'] = ''
        self.left.delete(0, END)
        self.right.delete(0, END)
        self.get_words()

    # Поиск слов в правой колонке,
    # выделение найденных слов красным красным цветом.
    def search_translate(self, event2):
        search_text = self.entry_search.get()

        if search_text == '':
            self.message['text'] = 'Введите слово'
        else:
            ls_tr = []
            for k, v in self.dic.items():
                if v.startswith(search_text):
                    ls_tr.append(v)
            self.tup_tr = tuple(ls_tr)
            print(self.tup_tr)
            print(self.right.size())
            ind = self.right.curselection()

            count = 0
            while count < len(self.tup_tr):
                #if self.tup_tr[count] ==
                item_search = self.tup_tr[count]
                for i in range(0, self.right.size()):
                    # print(self.right.get(i))
                    if self.right.get(i) == item_search:
                        self.right.itemconfig(i, fg='red')

                count += 1


if __name__ == '__main__':
    window = Tk()
    window.geometry('425x945+550+0')
    application = Match(window)
    window.mainloop()
