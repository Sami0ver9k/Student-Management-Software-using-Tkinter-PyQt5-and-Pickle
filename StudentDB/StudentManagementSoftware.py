from tkinter import *
from tkinter import ttk
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout,QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.Qt import *
from PyQt5 import QtCore
from collections import OrderedDict
import tkinter
import pickle

database = dict()
database={}

gRow=0
gCol=0
headerText=''

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Student Information Table'
        self.left = 190
        self.top = 450
        self.width = 900
        self.height = 200
        self.top2=550
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        delbutton = QPushButton('Delete', self)
        delbutton.setToolTip('This is an example button')
        #button.move(100, 470)
        delbutton.clicked.connect(self.del_click1)
        upbutton = QPushButton('Update', self)
        upbutton.setToolTip('This is an example button')
        # button.move(100, 470)
        upbutton.clicked.connect(self.up_click2)
        sortbutton = QPushButton('Sort By ID', self)
        sortbutton.setToolTip('This is an example button')
        # button.move(100, 470)
        sortbutton.clicked.connect(self.sort_table)
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QGridLayout()
        self.layout.addWidget(delbutton,0,0)
        self.layout.addWidget(upbutton,0,1)
        self.layout.addWidget(sortbutton, 0, 2)
        self.layout.addWidget(self.tableWidget,1,0,1,5)
        self.setLayout(self.layout)


        # Show widget
        self.show()

    @pyqtSlot()
    def del_click1(self):

        try:

            pickle_in = open("student2.pickle", "rb")
            student = pickle.load(pickle_in)
            Window.i = len(student)
            top=gRow+1
            for k in range(top, Window.i):
                student[k]=student[k+1]
                print(student[k])
                print(student[k+1])
            del student[Window.i]
            pickle_out = open("student2.pickle", "wb")
            global database
            database=student
            pickle.dump(student, pickle_out)

            print("Insert after deletion ...")

        except EOFError as error:
            print("File Empty")
        self.close()
        #self.createTable()
        #self.show()
        if Window.i>1 :
            self.__init__()



    @pyqtSlot()
    def up_click2(self):
        try:
            pickle_in = open("student2.pickle", "rb")
            student = pickle.load(pickle_in)
            print("Opening file ...")
            if gCol is 0:
                QMessageBox.about(self, "Error Message!!", "Id can not be changed")
                return

            student[gRow + 1][headerText]= self.tableWidget.item(gRow,gCol).text()
            #Update_database
            pickle_out = open("student2.pickle", "wb")
            pickle.dump(student, pickle_out)

        except EOFError as error:
            QMessageBox.about(self, "Error Message!!", "Empty File!!")

    @pyqtSlot()
    def sort_table(self):
        temp={}
        pickle_in = open("student2.pickle", "rb")
        student = pickle.load(pickle_in)
        database1={}
        database1=student
        for n, key in enumerate(sorted(database1.keys())):
            print('loop....')
            print(key)
            for m,key1 in enumerate(sorted(database1.keys())):
                if key1>key:
                    print('loop2....')
                    print(key1)
                    print(database1[key]['Id'] > database1[key1]['Id'])
                    print(database1[key])
                    print(database1[key1])
                    if database1[key]['Id'] > database1[key1]['Id']:
                        temp = database1[key]
                        database1[key] = database1[key1]
                        database1[key1] = temp

        # Update_database
        student=database1
        global database
        database=database1
        pickle_out = open("student2.pickle", "wb")
        pickle.dump(student, pickle_out)
        self.close()
        self.__init__()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        print(database)
        row = len(database)
        col = len(database[1])
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(col)

        #Enter data into table
        forHeader =[]
        self.tableWidget.setHorizontalHeaderLabels(['Id', 'Title', 'First Name', 'Middle Name', 'Last Name',
                                                    'Gender', 'DEPT', 'Year', 'Sem', 'Marks'])
        header = self.tableWidget.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignHCenter)

        for n, key in enumerate(sorted(database.keys())):
            forHeader.append(key)
            print('Key........')
            print(key)
            for m, item in enumerate(database[key]):
                str1=''

                for t, item1 in enumerate(database[key][item]):
                    newitem1 = QTableWidgetItem(item1)
                    str = self.tableWidget.setItem(n, m, newitem1)
                    str1+=item1
                newitem = QTableWidgetItem(str1)
                str=self.tableWidget.setItem(n, m, newitem)
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
        QMessageBox.about(self, "Notice!!", "Double Click the ,Required Row before pressing Delete button,"
                                            "desired cell before editing value in a cell before pressing Update button,"
                                             "Press ok!!")

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            global gRow,gCol,headerText
            gRow=currentQTableWidgetItem.row()
            gCol=currentQTableWidgetItem.column()
            headerText = self.tableWidget.horizontalHeaderItem(gCol).text()

class Window(Frame):
    i = 1

    def init_window(self):
        global comboName
        global ID
        global FirstName
        global MiddleName
        global LastName
        global MaleValue
        global FemaleValue
        global comboYear
        global comboSem
        global TotalMarks
        global btn2
        global student

        #Creating tkinter window.......
        self.master.title("Student Registration Form")
        self.pack(fill=BOTH, expand=1)
        instruction = Label(self, text="Student Information\n")
        instruction.place(x=0, y=0)

        Title = Label(self, text="Title : ")
        comboName = ttk.Combobox(self)
        comboName['values'] = ('Mr.', 'Miss.', 'Mrs.')
        Title.place(x=0, y=45)
        comboName.place(x=100, y=45)
        comboName.current(0)
        IDL = Label(self, text="ID : ")
        IDLexm = Label(self, text="*XX.01.04.XXX : ")
        FirstNameL = Label(self, text="First Name : ")
        MiddleNameL = Label(self, text="Middle Name : ")
        LastNameL = Label(self, text="Last Name : ")
        IDL.place(x=0, y=20)
        IDLexm.place(x=250, y=20)
        FirstNameL.place(x=0, y=80)
        MiddleNameL.place(x=0, y=120)
        LastNameL.place(x=0, y=160)

        ID = Entry(self)
        FirstName = Entry(self)
        MiddleName = Entry(self)
        LastName = Entry(self)
        ID.place(x=100, y=20)
        FirstName.place(x=100, y=80)
        MiddleName.place(x=100, y=120)
        LastName.place(x=100, y=160)

        MaleValue = tkinter.IntVar()
        FemaleValue = tkinter.IntVar()
        GenderT = Label(self, text="Gender : ")
        Gender_1 = Checkbutton(self, text="Male", variable=MaleValue, onvalue=1, offvalue=0)
        Gender_2 = Checkbutton(self, text="female", variable=FemaleValue, onvalue=1, offvalue=0)
        GenderT.place(x=0, y=190)
        Gender_1.place(x=100, y=190)
        Gender_2.place(x=160, y=190)

        btn2 = StringVar()
        DeptT = Label(self, text="Department : ")
        Dept_1 = Radiobutton(self, text="CSE", value="CSE", variable=btn2)
        Dept_2 = Radiobutton(self, text="CE", value="CE", variable=btn2)
        Dept_3 = Radiobutton(self, text="Textile", value="Textile", variable=btn2)
        Dept_4 = Radiobutton(self, text="Arch", value="Arch", variable=btn2)
        Dept_5 = Radiobutton(self, text="BBA", value="BBA", variable=btn2)
        Dept_6 = Radiobutton(self, text="ME", value="ME", variable=btn2)
        Dept_7 = Radiobutton(self, text="IPE", value="IPE", variable=btn2)
        DeptT.place(x=0, y=230)
        Dept_1.place(x=80, y=230)
        Dept_2.place(x=130, y=230)
        Dept_3.place(x=180, y=230)
        Dept_4.place(x=230, y=230)
        Dept_5.place(x=280, y=230)
        Dept_6.place(x=330, y=230)
        Dept_7.place(x=380, y=230)

        Year = Label(self, text="Year : ")
        comboYear = ttk.Combobox(self)
        comboYear['values'] = ('1st', '2nd', '3rd', '4th')
        Year.place(x=0, y=270)
        comboYear.place(x=100, y=270)
        comboYear.current(0)

        Sem = Label(self, text="Semester : ")
        comboSem = ttk.Combobox(self)
        comboSem['values'] = ('1st', '2nd')
        Sem.place(x=250, y=270)
        comboSem.place(x=350, y=270)
        comboSem.current(0)

        instruction2 = Label(self, text="Student Grade\n")
        instruction2.place(x=590, y=50)

        TotalMarksL = Label(self, text="Total Marks : ")
        TotalMarksL.place(x=590, y=100)

        TotalMarks = Entry(self)
        TotalMarks.place(x=700, y=100)

        button1 = Button(self, text='Show', command=self.ShowInfo)
        button1.place(x=30, y=400)

        button2 = Button(self, text='Insert', command=self.InsertAllInfo)
        button2.place(x=30, y=440)


    def ShowInfo(self):
        pickle_in = open("student2.pickle", "rb")
        student = pickle.load(pickle_in)
        global database
        database=student
        app1 = QApplication(sys.argv)
        ex = App()#used
        app1.exec_()

    def InsertAllInfo(self):
        G = StringVar()
        student = {}
        title = comboName.get()
        fName = FirstName.get()
        mName = MiddleName.get()
        lName = LastName.get()
        dept = btn2.get()
        num = TotalMarks.get()
        year = comboYear.get()
        sem = comboSem.get()

        #For checking purpose....
        print("Title : " + comboName.get())
        print("First Name : " + FirstName.get())
        print("Middle Name : " + MiddleName.get())
        print("Last Name : " + LastName.get())
        if MaleValue.get() == 1 and FemaleValue.get() == 1:
            G = "Nuetral Gender"

        elif MaleValue.get() == 1 and FemaleValue.get() == 1:
            G = "Gender Not choosen"

        elif MaleValue.get() == 1:
            G = "Male"
        elif FemaleValue.get() == 1:
            G = "Female"
        print("Dept : " + btn2.get())
        print("Year : " + comboYear.get())
        print("Semester : " + comboSem.get())
        print("Marks : " + TotalMarks.get())

        try:
            pickle_in = open("student2.pickle", "rb")
            try:
                student = pickle.load(pickle_in)
                Window.i = len(student) + 1
                print(Window.i)
                for k in range(1,Window.i):
                    print(ID.get())
                    if ID.get() in student[k]['Id']:
                        print("ID is already in use ")
                        return
                orig = {
                    Window.i: {"Id": ID.get(), "Title": comboName.get(), "First Name": FirstName.get(),

                               "Middle Name": MiddleName.get(),

                               "Last Name": LastName.get(), 'Gender': G, 'DEPT': btn2.get(),

                               'Year': comboYear.get(),

                               'Sem': comboSem.get(), 'Marks': TotalMarks.get()}}

                student.update(orig)

                print("Insert Done ...")

                pickle_out = open("student2.pickle", "wb")

                pickle.dump(student, pickle_out)

                print("Insert Done2 ...")


            except TypeError as e:
                print("insert Gender")
            pickle_out.close()

        except FileNotFoundError as error:

            try:
                student = {
                    Window.i: {"Id": ID.get(),'Title': title, 'First Name': fName, 'Middle Name': mName,
                               'Last Name': lName, 'Gender': G, 'DEPT': dept, 'Year': year,
                               'Sem': sem, 'Marks': num}}
                print("Insert Done In an Empty file...")
                print(student)
                pickle_out = open("student2.pickle", "wb")
                pickle.dump(student, pickle_out)
                pickle_out.close()


            except TypeError as e:
                print("insert Gender")

        except EOFError as error:
            try:
                student = {
                    Window.i: {"Id": ID.get(),'Title': title, 'First Name': fName, 'Middle Name': mName,
                               'Last Name': lName, 'Gender': G, 'DEPT': dept, 'Year': year,
                               'Sem': sem, 'Marks': num}}
                print("Insert Done In an Empty file...")
                print(student)
                pickle_out = open("student2.pickle", "wb")
                pickle.dump(student, pickle_out)
                pickle_out.close()


            except TypeError as e:
                print("insert Gender")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

if __name__ == '__main__':
    root = Tk()
    root.geometry("1000x500")
    app = Window(root)
    root.mainloop()

