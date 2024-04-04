from tkinter import *
import tkinter as tk

def upload():
    q1 = q1_e.get()
    q2_e = tk.Entry(sp)
    q2 = q2_e.get()
    a="Do you have driving licence"
    b="No you can not drive"
    if q1 == "18" or q1 >= "18":
        q1_label.config(text=a)
        q2_e.place(x="500", y="175", height="30")
        b2.place(x="700",y="175",height="30")
    else:
        fini.config(text=b)

def upload1():
    q2_e = tk.Entry(sp)
    q2 = q2_e.get()
    y = "Yes you can drive"
    n= "No you need licence to drive a car."
    if q2 == "Yes" :
        fini.config(text=y)
    else:
        fini.config(text=n)



sp= Tk()
sp.geometry("1000x500")
sp.title("Driving age")
sp.config(bg="lightblue")

lab_1 = Label(sp,text="Allowing Age for driving",font=("Time New Roman",50,"bold"),bg="lightblue",fg="yellow")
lab_1.place(x="100",y="20")

q_1 = Label(sp,text="Entre your age",font=("Time New Roman",25,),bg="lightblue",fg="black")
q_1.place(x="20",y="110")

q1_e = tk.Entry(sp)
q1_e.place(x="350",y="125",height="30")


b1=tk.Button(sp,text="Entre",command=upload).place(x="500",y="125",height="30")

b2= tk.Button(sp,text="Entre",command=upload1)

q1_label=Label(sp,text="",font=("Time New Roman",25,),bg="lightblue",fg="black")
q1_label.place(x="20",y="175",)

fini = Label(sp,text="",font=("Time New Roman",30,"bold"),bg="lightblue",fg="black")
fini.place(x="100",y="250",)

sp.mainloop()