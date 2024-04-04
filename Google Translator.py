from tkinter import *
from tkinter import ttk
from googletrans import Translator,LANGUAGES

def change(text="type",src="English",dest="Hindi"):
    text1 = text
    src1= src
    dest1= dest
    trans =Translator
    trans1 = trans._translate(self="",text=text1,src=src1,dest=dest1,override="")

    return trans1.text
    

def data():
    sr = comb_sor.get()
    de= comb_dest.get()
    masga = sor_text.get(1.0, END)
    text1 = change(text=masga, src=sr, dest=de)
    dest_text.delete(1.0, END)
    dest_text.insert(END, text1)


sp=Tk()
sp.title("Google Translator")
sp.geometry("1000x800")
sp.config(bg="lightblue")
p1=PhotoImage(file='Google_Translate_logo.svg.png')
sp.iconphoto(False, p1)

Lab_1 = Label(sp,text="Google Translator",font=("Time New Roman",50,"bold"),bg="lightblue",fg="darkblue")
Lab_1.place(x="230",y="10")

frame = Frame(sp).pack(side= BOTTOM)

Lab_2 = Label(sp,text="Source Text",font=("Time New Roman",20,"bold"),bg="lightblue",fg="darkblue")
Lab_2.place(x="420",y="90")

sor_text = Text(frame,font=("Time New Roman",20,"bold"),wrap=WORD)
sor_text.place(x="30",y="140",height="200",width="940")

list_text = list(LANGUAGES.values())

comb_sor = ttk.Combobox(frame,values=list_text)
comb_sor.place(x="630",y="350",height="30",width="100")
comb_sor.set("english")

button_change = Button(frame,text = "Translate",relief= RAISED,command=data)
button_change.place(x="750",y="350",height="30",width="100")

comb_dest = ttk.Combobox(frame,values=list_text)
comb_dest.place(x="870",y="350",height="30",width="100")
comb_dest.set("hindi")

dest_text = Text(frame,font=("Time New Roman",20,"bold"),wrap=WORD)
dest_text.place(x="30",y="450",height="200",width="940")

Lab_3 = Label(sp,text="Destination Text",font=("Time New Roman",20,"bold"),bg="lightblue",fg="darkblue")
Lab_3.place(x="420",y="410")

sp.mainloop()

