import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,\
    QPushButton, QCalendarWidget, QTextEdit, QTextBrowser
from PyQt6.QtCore import QDate
import sqlite3
import traceback


class Calender(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 600, 400)

        self.cal = QCalendarWidget()
        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.date_connect)

        self.label = QLabel(self)
        self.label2 = QLabel(self)
        self.addText = QTextEdit(self)
        self.schedule = QTextBrowser(self)
        self.label3 = QLabel()
        self.send = QPushButton()
        self.send.setText("commit")
        vbox1 = QVBoxLayout()
        vbox2 = QVBoxLayout()
        hbox2 = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        vbox1.addWidget(self.label)
        vbox2.addWidget(self.label2)
        vbox1.addWidget(self.cal)
        vbox2.addWidget(self.addText)
        vbox2.addWidget(self.schedule)
        hbox2.addWidget(self.label3)
        hbox2.addWidget(self.send)
        vbox2.addLayout(hbox2)
        self.setLayout(hbox1)

        self.send.clicked.connect(self.commit)

    def database(self):
        db = sqlite3.connect('Calender.db', isolation_level = None)
        cursor = db.cursor()
        table = "create table if not exists schedule (time text unique, txt text unique)"
        cursor.execute(table)
        return db, cursor

    def date_connect(self):
        db, cursor = self.database()
        date = self.cal.selectedDate()
        time = date.toPyDate().strftime('%Y-%m-%d')
        self.label.setText(time)
        a = cursor.execute(f"SELECT txt FROM schedule WHERE time = '{time}'")
        b = a.fetchone()
        if b != None:
            if b[0]:
                self.label3.setText("데이터가 있어요!")
                self.schedule.setText(b[0])
        else:
            self.label3.setText("데이터가 없어요!")
            self.schedule.setText("")

        self.label.setText(time)
        self.label2.setText(f"{time} 스케줄")
        db.close()

    def commit(self):
        db, cursor = self.database()
        date = self.cal.selectedDate()
        time = date.toPyDate().strftime('%Y-%m-%d')
        txt = self.addText.toPlainText()
        self.schedule.setText(txt)
        cursor.execute(f"INSERT or replace into schedule values('{time}', '{txt}')")
        self.label3.setText("저장했어요!")
        self.addText.clear()
        db.close()


app = QApplication(sys.argv)
window = Calender()
window.show()
sys.exit(app.exec())