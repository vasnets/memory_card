import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QRadioButton, QDialog, QLineEdit


def init_db():
    conn = sqlite3.connect('question.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer1 TEXT,
    answer2 TEXT,
    answer3 TEXT,
    answer4 TEXT,
    correct_answer INTEGER)''')

    conn.commit()
    conn.close()


def add_question_to_db(question, answer1, answer2, answer3, answer4, correct_answer):
    conn = sqlite3.connect('question.db')
    cur = conn.cursor()

    cur.execute('''INSERT INTO questions (question, answer1, answer2, answer3, answer4, correct_answer)
    VALUES (?, ?, ?, ?, ?, ?)''', (question, answer1, answer2, answer3, answer4, correct_answer))

    conn.commit()
    conn.close()


def select_random_question():
    conn = sqlite3.connect('question.db')
    cur = conn.cursor()

    cur.execute("""SELECT * FROM questions ORDER BY RANDOM() LIMIT 1""")
    question = cur.fetchone()

    conn.commit()
    conn.close()

    return question

def check_answer():
    if btn_answer3.isChecked():
        QMessageBox.information(main_win, 'результат', 'Відповідь вірна')
    else:
        QMessageBox.information(main_win, 'результат', 'Обери іншу відповідь')


def change_questions():
    pass


def add_question():
    dialog = QDialog(main_win)
    dialog.setWindowTitle('Додати нове запитання')

    question_input = QLineEdit(dialog)
    question_input.setPlaceholderText('Введіть запитання')

    answer1 = QLineEdit(dialog)
    answer1.setPlaceholderText('введіть першу відповідь')

    answer2 = QLineEdit(dialog)
    answer2.setPlaceholderText('введіть другу відповідь')

    answer3 = QLineEdit(dialog)
    answer3.setPlaceholderText('введіть третю відповідь')

    answer4 = QLineEdit(dialog)
    answer4.setPlaceholderText('введіть четверту відповідь')

    correct_answer = QLineEdit(dialog)
    correct_answer.setPlaceholderText('Вірна відповідь (1-4)')

    add_button = QPushButton('Додати', dialog)

    dialog_layout = QVBoxLayout(dialog)
    dialog_layout.addWidget(question_input)
    dialog_layout.addWidget(answer1)
    dialog_layout.addWidget(answer2)
    dialog_layout.addWidget(answer3)
    dialog_layout.addWidget(answer4)
    dialog_layout.addWidget(correct_answer)
    dialog_layout.addWidget(add_button)

    def submit_question():
        new_question = question_input.text()
        new_answer1 = answer1.text()
        new_answer2 = answer2.text()
        new_answer3 = answer3.text()
        new_answer4 = answer4.text()
        new_correct_answer = correct_answer.text()

        if new_question and new_answer4 and new_answer3 and new_answer2 and new_answer1 and new_correct_answer.isdigit() and 1 <= int(new_correct_answer) <= 4:
            add_question_to_db(new_question, new_answer1, new_answer2, new_answer3, new_answer4, int(new_correct_answer))

            dialog.accept()
        else:
            QMessageBox.warning(dialog, 'помилка в заповненні полів')


    add_button.clicked.connect(submit_question)
    dialog.exec()





app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Memory card')

question = QLabel('В якому році канал отримав «золоту кнопку» від YouTube?')
btn_answer1 = QRadioButton('2005')
btn_answer2 = QRadioButton('2010')
btn_answer3 = QRadioButton('2015')
btn_answer4 = QRadioButton('2020')

check_button = QPushButton('Перевірити відповідь')
check_button.clicked.connect(check_answer)
change_question = QPushButton('Змінити питання')
change_question.clicked.connect(change_questions)
add_new_question = QPushButton('Додати нове запитання')
add_new_question.clicked.connect(add_question)

layout_main = QVBoxLayout()
layout_main.addWidget(question, alignment=Qt.AlignmentFlag.AlignCenter)
layout_main.addWidget(btn_answer1, alignment=Qt.AlignmentFlag.AlignCenter)
layout_main.addWidget(btn_answer2, alignment=Qt.AlignmentFlag.AlignCenter)
layout_main.addWidget(btn_answer3, alignment=Qt.AlignmentFlag.AlignCenter)
layout_main.addWidget(btn_answer4, alignment=Qt.AlignmentFlag.AlignCenter)

layoutH1 = QHBoxLayout()
layoutH2 = QHBoxLayout()
layoutH3 = QHBoxLayout()
layoutH4 = QHBoxLayout()
layoutH5 = QHBoxLayout()


layoutH1.addWidget(question, alignment=Qt.AlignmentFlag.AlignCenter)
layoutH2.addWidget(btn_answer1, alignment=Qt.AlignmentFlag.AlignCenter)
layoutH2.addWidget(btn_answer2, alignment=Qt.AlignmentFlag.AlignCenter)
layoutH3.addWidget(btn_answer3, alignment=Qt.AlignmentFlag.AlignCenter)
layoutH3.addWidget(btn_answer4, alignment=Qt.AlignmentFlag.AlignCenter)
layoutH4.addWidget(check_button, alignment=Qt.AlignmentFlag.AlignCenter)
layoutH4.addWidget(change_question, alignment=Qt.AlignmentFlag.AlignCenter)
layoutH5.addWidget(add_new_question, alignment=Qt.AlignmentFlag.AlignCenter)

layout_main = QVBoxLayout()
layout_main.addLayout(layoutH1)
layout_main.addLayout(layoutH2)
layout_main.addLayout(layoutH3)
layout_main.addLayout(layoutH4)
layout_main.addLayout(layoutH5)

main_win.setLayout(layout_main)
main_win.show()
app.exec()
