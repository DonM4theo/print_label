from simple_zpl2 import ZPLDocument
import io
from simple_zpl2 import NetworkPrinter
from tkinter import *
from PIL import Image, ImageTk
import tkinter.filedialog as tkf
import os
import shutil
from tkinter import messagebox
import time

user_name = os.getenv('username')  # dla odczytu aktualnie zalogowanego użytkownika - wykorzystanie przy ścieżkach do plików


##############################################################################################################################

# Czyszczenie tymek

def clear():
    try:
        os.remove("C:/toprint/tmp/label.zpl")
        print("Usunięto label.zpl")
        os.remove("C:/toprint/tmp/view.png")
        print("Usunięto view.png")

    except:
        print("Nic nie było do usunięcia")


clear()

# Deklaracja elementów:
printer_tab = []
prt_file = open("C:/toprint/default/printer_list.txt", "r", encoding='utf8')
lin = prt_file.readlines()
prt_file.close()

prt_file = open("C:/toprint/default/printer_list.txt", "r", encoding='utf8')
for iteration in lin:
    printer_tab.append(iteration)
prt_file.close()


def copy():
    filename = tkf.askopenfilenames(initialdir="C:/Users/" + user_name + "/Desktop/", title="Wybierz pliki", filetypes=(
        ("Printer code file", ("*.zpl")),

    ))
    lst = list(filename)
    print(lst)
    if len(lst) <= 1:
        for path in lst:
            path = str(path).replace("/", "\\")
            print(path)
            shutil.copy(path, 'C:\\toprint\\tmp\\label.zpl')
        print("Done")
    else:
        messagebox.showerror("Limit error", "Wskaż jedną etykietę")

    raw = ''
    file = open("C:/toprint/tmp/label.zpl", "r", encoding='utf8')
    lines = file.readlines()
    file.close()

    file = open("C:/toprint/tmp/label.zpl", "r", encoding='utf8')
    #
    for line in lines:
        raw = raw + line

    file.close()
    zdoc = ZPLDocument()
    zdoc.add_zpl_raw(raw)
    # Get PNG byte array
    convert_to_png = zdoc.render_png(label_width=4.13, label_height=4.13)
    # render fake file from bytes
    fake_file = io.BytesIO(convert_to_png)
    img = Image.open(fake_file)
    img.save('C:/toprint/tmp/' + "view" + '.png')


def print_view():
    exists = os.path.isfile("C:/toprint/tmp/view.png")
    if exists:
        view = Image.open("C:/toprint/tmp/view.png")
    else:
        view = Image.open("C:/toprint/default/default.png")

    view.show()


def just_print():
    raw = ''
    exists = os.path.isfile("C:/toprint/tmp/label.zpl")
    if exists:
        print("To zajebiście")
    else:
        messagebox.showinfo("Brak etykiety", "Wskaż etykietę poprzez \"Wybierz z pliku...\"")

    try:
        file = open("C:/toprint/tmp/label.zpl", "r", encoding='utf8')
        lines = file.readlines()
        file.close()
        file = open("C:/toprint/tmp/label.zpl", "r", encoding='utf8')

        for line in lines:
            raw = raw + line
        zdoc = ZPLDocument()
        zdoc.add_zpl_raw(raw)
    except:
        print("Brak wskazanego pliku .zpl")
    selection = printer_list.curselection()
    if len(selection) < 1:
        messagebox.showerror("Brak drukarki", "Wskaż drukarkę w polu \"Wybierz drukarkę:\".")
    else:
        print("curselection", selection)
        pos = 0
        for i in selection:
            idx = int(i) - pos
            printer = printer_list.get(idx)
            print("wybrana drukarka-", printer)
            ip_printer = str(printer).split('-')[0]

    amount = amount_entry.get()

    try:
        val = int(amount)
        if 0 < int(amount) <= 10:
            for i in range(int(amount)):
                print(i)
                prn = NetworkPrinter(ip_printer)
                prn.print_zpl(zdoc)
        else:
            messagebox.showerror("Błędna wartość", "Wprowadź wartość w polu \"Ilość:\" z przedziału: [1-10].")

    except ValueError:
        messagebox.showerror("Błędna wartość", "Wprowadź wartość w polu \"Ilość:\" z przedziału: [1-10].")
        return


window = Tk()
window.title('Drukuj etykietę')
window.configure(background="#474747")
window.resizable(0, 0)
window.geometry("400x400")
window.attributes("-topmost", True)
windowW = window.winfo_reqwidth()
windowH = window.winfo_reqheight()
windowR = int(window.winfo_screenwidth() / 2 - windowW)
windowD = int(window.winfo_screenheight() / 2 - windowH - 50)
window.geometry("+{}+{}".format(windowR, windowD))

lb1 = Label(window, text='Wybierz drukarkę:', font="Tahoma 10 bold", bg="#474747", fg="RED")
printer_list = Listbox(window, width=35, height=3, bg="#f2e5dc", font="Tahoma 10 ", fg="BLACK")
lb2 = Label(window, text='Wybierz etykiete:', font="Tahoma 10 bold", bg="#474747", fg="RED")
button_choice = Button(window, text='Wybierz z pliku...', font="Tahoma 10 bold", bg="#474747", fg="RED", command=copy)
button_show = Button(window, text='Podgląd wydruku', font="Tahoma 10 bold", bg="#474747", fg="RED", command=print_view)
amount_entry = Entry(window, width=3, bg="#f2e5dc", font="Tahoma 10 ", fg="BLACK", )
amount_label = Label(window, text='Ilość:', font="Tahoma 10 bold", bg="#474747", fg="RED")
button_print = Button(window, text='Drukuj', font="Tahoma 10 bold", bg="#474747", fg="RED", command=just_print)

##############################################################################################################################
for element in printer_tab:
    printer_list.insert(printer_tab.index(element), element)
print("ptab", printer_tab)
print("plist", printer_list.get(0))
##############################################################################################################################
# Pozycjonowanie elementów:
lb1.place(relx=0.05, rely=0.02, anchor=NW)
printer_list.place(relx=0.05, rely=0.08, anchor=NW)
lb2.place(relx=0.05, rely=0.25, anchor=NW)
button_choice.place(relx=0.05, rely=0.3, anchor=NW)
button_show.place(relx=0.05, rely=0.4, anchor=NW)
amount_label.place(relx=0.05, rely=0.9)
amount_entry.place(relx=0.15, rely=0.9)
button_print.place(relx=0.8, rely=0.9)


window.mainloop()
