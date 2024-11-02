# Python, Tkinter и SQL: разрабатываем приложение для создания словарей и запоминания иностранных слов
### WordMatch project for Proglib.io

Программа WordMatch состоит из 3 независимых модулей:
- скрипт для создания баз данных;
- GUI + CRUD для работы с базой SQLite;
- GUI для скрипта, выводящего слова и значения, и проверяющего правильность сопоставления.

[Пошаговый урок по разработке](https://proglib.io/p/python-tkinter-i-sql-razrabatyvaem-prilozhenie-dlya-sozdaniya-slovarey-i-zapominaniya-inostrannyh-slov-2022-08-08)

![1d135ceefb316e8280eb96257f2ba212](https://user-images.githubusercontent.com/85797091/183397294-e70d3fc8-0275-4f73-80a8-12e6a3363b74.jpg)

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

	create_new_db.py:
		Скрипт для создания баз данных.
		
	dictionary.db:
		Небольшой словарь (две сотни строк) иностранных слов, выражений и их
		переводов. Для наглядной демонстрации, как можно составлять свой словарь,
		разделять слова и выражения по алфавиту, а также посмотреть, как 
		работают тесты.
	
	edit_dictionary.py:
		GUI для заполнения базы SQLite иностранными словами и их переводами.
		
![edit_dict_py.png](https://github.com/donKarabas/wordmatch/blob/main/pictures/edit_dict_py.png)
		
	write_in_file.py:
			Скрипт создаст текстовый файл translation.txt и перепишет в него 
			построчно вашу БД иностранных слов и переводов. Текстовый файл можно
			скопировать на смартфон и в любое удобное время тренироваться, 
			запоминать перевод иностранных слов из вашей БД.
		
![translation.txt](https://github.com/donKarabas/wordmatch/blob/main/pictures/translation_txt.png)
