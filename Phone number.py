import tkinter as tk
from tkinter import *
from tkinter import messagebox,filedialog
import phonenumbers
from phonenumbers import timezone, geocoder, carrier

def upload():
    num=number.get()
    num_lab.config(text=num)
    phone = phonenumbers.parse(num)
    time = timezone.time_zones_for_number(phone)
    car = carrier.name_for_number(phone, "en")
    reg = geocoder.description_for_number(phone, "en")
    phone_lab.config(text=phone)
    time_lab.config(text=time)
    car_lab.config(text=car)
    reg_lab.config(text=reg)


sp=tk.Tk()
sp.title("Phone number details")
sp.geometry("1000x500")
sp.config(bg="lightblue")

label=Label(sp,text="Phone Number Details",font=("Time New Roman",50),fg="yellow",bg="lightblue")
label.place(x="150",y="35")

number_label = Label(sp,text="ENTRE NUMBER WITH +__ :",font=("Time New Roman",15),fg="Yellow",bg="LIGHTBLUE" )
number_label.place(x="30",y="120")

number = tk.Entry(sp)
number.place(x="330",y="125",height="20")


tk.Button(sp,text="Entre", command= upload).place(x="500",y="120")

num_lab = Label(sp,text="",font=("Time New Roman",20),fg="Yellow",bg="LIGHTBLUE" )
num_lab.place(x="30",y="150")

phone_lab=Label(sp,text="",font=("Time New Roman",20),fg="Yellow",bg="LIGHTBLUE" )
phone_lab.place(x="30",y="190")

time_lab = Label(sp,text="",font=("Time New Roman",20),fg="Yellow",bg="LIGHTBLUE")
time_lab.place(x="30",y="230")

car_lab= Label(sp,text="",font=("Time New Roman",20),fg="Yellow",bg="LIGHTBLUE")
car_lab.place(x="30",y="270")

reg_lab = Label(sp,text="",font=("Time New Roman",20),fg="Yellow",bg="LIGHTBLUE")
reg_lab.place(x="30",y="310")

sp.mainloop()

