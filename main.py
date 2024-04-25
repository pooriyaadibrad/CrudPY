
from sqlalchemy import create_engine, Column, Integer, String

from sqlalchemy.orm import sessionmaker,declarative_base

import messagebox
engine = create_engine('sqlite:///Crud.db',echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
class product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    quantity = Column(Integer)

    def __init__(self, name='', price=0,quantity=0):
        self.name = name
        self.price = price
        self.quantity = quantity

Base.metadata.create_all(engine)

from tkinter import *
from tkinter import ttk
class App(Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master
        self.createWidgets()
        self.Load()


    def createWidgets(self):
        self.VariableCreate()
        self.textbox()
        self.button()
        self.lable()
        self.table()
    def textbox(self):
        self.textName=Entry(self.master,textvariable=self.TxtName)
        self.textName.place(x=100,y=10)

        self.textPrice=Entry(self.master,textvariable=self.TxtPrice)
        self.textPrice.place(x=100,y=40)

        self.textQuantity=Spinbox(self.master,from_=0,to=10000,textvariable=self.TxtQuantity)

        self.textQuantity.place(x=100,y=80)

        self.textSearch=Entry(self.master)
        self.textSearch.place(x=150,y=400)
    def button(self):
        self.buttonRegister=Button(self.master,text="Register")
        self.buttonRegister.bind("<Button-1>",self.onClickRegister)
        self.buttonRegister.place(x=80,y=120)

        self.buttonSearch=Button(self.master,text="Search")
        self.buttonSearch.bind("<Button-1>",self.onClickSearch)
        self.buttonSearch.place(x=70,y=400)

        self.buttondelete=Button(self.master,text="Delete")
        self.buttondelete.bind("<Button-1>",self.onClickDelete)
        self.buttondelete.place(x=200,y=120)
    def lable(self):
        self.lableName=Label(self.master,text="Name")
        self.lableName.place(x=30,y=10)

        self.lablePrice=Label(self.master,text="Price")
        self.lablePrice.place(x=30,y=40)

        self.lableQuantity=Label(self.master,text="Quantity")
        self.lableQuantity.place(x=30,y=80)

    def table(self):
        coulmns=('id','Product Name','Price','Quantity')
        self.table=ttk.Treeview(self.master,columns=coulmns,show='headings')
        for i in range(4):
            self.table.column(coulmns[i],anchor=CENTER,width=160)
            self.table.heading(coulmns[i],text=coulmns[i])
        self.table.bind('<Button-1>',self.selection)
        self.table.pack(side=RIGHT,fill=BOTH)
    def onClickRegister(self,event=None):
        product1=product(name=self.textName.get(),price=int(self.textPrice.get()),quantity=int(self.textQuantity.get()))
        self.Register(product1)
        self.insertTable(product1)
        test=product1.__class__.__name__
        messagebox.showinfo("Register",str(test))
    def Register(self,value):
        session.add(value)
        session.commit()
    def insertTable(self,value):
        self.table.insert('','end',values=[value.id,value.name,value.price,value.quantity])
    def readAll(self):
        return session.query(product).all()
    def Load(self):
        alldata=self.readAll()
        self.clearTable()
        for data in alldata:
            self.insertTable(data)
    def clearTable(self):
        for item in self.table.get_children():
            self.table.delete(item)

    def onClickSearch(self,e):
        if self.textSearch.get()=='':
            self.Load()
        else:
            resultList=self.search(self.textSearch.get())
            self.clearTable()
            for data in resultList:
                self.insertTable(data)
    def search(self,value):
        alldata=self.readAll()
        result=[]
        for data in alldata:
            if data.name==value or str(data.quantity)==value or str(data.price)==value:
                result.append(data)
        return result
    def onClickDelete(self,e):
        select = self.table.selection()
        if select != ():
            id = self.table.item(select)['values'][0]
            alldata=self.readAll()
            for data in alldata:
                if data.id==id:
                    session.delete(data)
            self.table.delete(select)
    def selection(self,e):
        select = self.table.selection()
        if select != ():
            data = self.table.item(select)['values']
            self.TxtName.set(data[1])
            self.TxtPrice.set(data[2])
            self.TxtQuantity.set(data[3])
    def VariableCreate(self):
        self.TxtName=StringVar()
        self.TxtPrice=StringVar()
        self.TxtQuantity=StringVar()

if __name__ == '__main__':
    root = Tk()

    root.geometry('1000x500')
    app = App(root)

    root.mainloop()