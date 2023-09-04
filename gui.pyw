import customtkinter
from CTkListbox import *
import main as kargotakip
import os
import subprocess
from CTkMessagebox import CTkMessagebox
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


def askquestion(titlee,question):
    msg = CTkMessagebox(title=titlee, message=question, option_1="Yes", option_2="No")
    response = msg.get()
    if response=="Yes":
        return True       
    else:
        return False
def update_db():
    new_content = ""
    for item in listboxitems:
        new_content = new_content + item.cget("text") + "\n"
    with open("database.db","w",encoding="utf-8") as file:
        file.write(new_content)

def add_on_click():
    if urunadiTxt.get().strip() == "" or takip_kodu.get().strip() == "": return
    data = f"{urunadiTxt.get().strip().upper()}\t{firmaCombo.get()}\t{takip_kodu.get().strip()}"
    urunadiTxt.delete(0,customtkinter.END)
    takip_kodu.delete(0,customtkinter.END)
    add(data)
    update_db()

def add(data):
    newlistboxitem = customtkinter.CTkCheckBox(master=listbox,text=data,width=500)
    newlistboxitem.pack(pady=10,padx=10)
    listboxitems.append(newlistboxitem)

def delete():
    if (not askquestion("Proje","Seçili kargoları listeden silmek istediğinize emin misiniz?")): return 
    toRemove = []
    for item in listboxitems:
        if item.get() == 1:
            item.destroy()
            toRemove.append(item)
    for item in toRemove:
        listboxitems.remove(item) 
    update_db()

root = customtkinter.CTk()
root.title("Proje")

frame = customtkinter.CTkFrame(master=root)
frame.pack(side="left", pady=10,padx=10,fill="y",expand=False)

frame2 = customtkinter.CTkFrame(master=root)
frame2.pack(side="right", pady=10,padx=10,fill="y",expand=False)

urunadiTxt = customtkinter.CTkEntry(master=frame,width=500,placeholder_text="Ürün Adı")
urunadiTxt.pack(padx=10,pady=10)

subframe = customtkinter.CTkFrame(master=frame,fg_color="transparent")
subframe.pack(pady=10,padx=0,fill="x",expand=False)


takip_kodu = customtkinter.CTkEntry(master=subframe,width=350,placeholder_text="Takip Kodu")
takip_kodu.pack(pady=10,padx=10,side="left")

firmaCombo = customtkinter.CTkComboBox(master=subframe,values=["ARAS KARGO","YURTİÇİ KARGO","TRENDYOL EXPRESS","MNG KARGO","PTT KARGO"])
firmaCombo.pack(pady=10,padx=0,side="left")

addbutton = customtkinter.CTkButton(master=frame,text="EKLE",command=add_on_click,width=500)
addbutton.pack(pady=10,padx=10)

listbox = customtkinter.CTkScrollableFrame(master=frame)
listbox.pack(fill="both",expand=True, padx=10, pady=10)

listboxitems = []

subframe2 = customtkinter.CTkFrame(master=frame,fg_color="transparent")
subframe2.pack(pady=0,padx=0,fill="x",expand=False)

deletebtn = customtkinter.CTkButton(master=subframe2,text="SİL",command=delete,width=350,fg_color="purple")
deletebtn.pack(pady=10,padx=10, side="left")

showCB = customtkinter.CTkCheckBox(master=subframe2,text="Show Browser")
showCB.pack(pady=10,padx=10)

def learn():
    for item in listboxitems:
        if item.get() == 1:
            data = item.cget("text")
            text_to_send = data + '\n'
            takip_kodu = data.split('\t')[2]
            firma_adi = data.split('\t')[1]
            if showCB.get() == 0: flag = True 
            else: flag = False
            kargotakip.headless = flag
            text_to_send = text_to_send + kargotakip.get_info(takip_kodu,firma_adi) + '\n'
            text_to_send = text_to_send + '-'*50 + '\n'
            resultTxt.insert(customtkinter.END,text_to_send)
            root.update()
            kargotakip.driver.close()
            subprocess.call(f"taskkill /F /IM chromedriver.exe /T", shell=True)


secili = customtkinter.CTkButton(master=frame,text="SEÇİLİ KARGOLARIN DURUMUNU ÖĞREN",command=learn,width=500)
secili.pack(pady=10,padx=10)

def selectall():
    for item in listboxitems:
        if item.get() == 0:
            item.toggle()

tumkargo = customtkinter.CTkButton(master=frame,text="TÜMÜNÜ SEÇ",command=selectall,width=500)
tumkargo.pack(pady=10,padx=10)

resultTxt = customtkinter.CTkTextbox(master=frame2,width=500,height=600)
resultTxt.pack(padx=10,pady=10)

with open("database.db","r",encoding="utf-8") as file:
    content = file.read()
for line in content.split('\n'):
    if line.strip() != "": 
        add(line)


root.mainloop()
