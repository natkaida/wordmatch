
import sqlite3 as sq


class Main:
    def __init__(self):
        self.db = db
        self.translation()

    def translation(self):
        self.dict_translation = {}
        self.db.cur.execute('''SELECT word, meaning FROM dictionary''')
        self.base_traslation = self.db.cur.fetchall()

        for item in self.base_traslation:
            self.dict_translation[item[0]] = item[1]

        self.list_keys = list(self.dict_translation)
        self.list_keys.sort()


        self.input_file = open('translation.txt', 'w')
        for k in self.list_keys:
            self.input_file.write(f'{k} - {self.dict_translation[k]}\n')

        self.input_file.close()


class DB:
    def __init__(self):
        with sq.connect('dictionary.db') as conn:
            self.cur = conn.cursor()


if __name__ == '__main__':
    db = DB()
    app = Main()