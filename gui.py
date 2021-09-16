import glob
import json
import tarfile
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.font import Font
import requests
import audit
import re

main = Tk()
myFont = Font(family="Mincho", size=13)
s = ttk.Style()
s.configure('TFrame', background='#FFC7FF')
main.title("Security Benchmarking Tool Lab 1 Malîi Antonela")
main.geometry("1100x700")
frame = ttk.Frame(main, width=1100, height=700, style='TFrame', padding=(4, 4, 450, 450))
frame.grid(column=0, row=0)

index = 0
arr = []
matching = []

vars = StringVar()
tofile = []
structure = []

def download_url(url, save_path, chunk_size=1024):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def extract_download():
    url = "https://www.tenable.com/downloads/api/v1/public/pages/download-all-compliance-audit-files/downloads/7472/download?i_agree_to_tenable_license_agreement=true"
    path = "audits.tar.gz"
    download_url(url, path)
    tf = tarfile.open("audits.tar.gz")
    tf.extractall()
    print(glob.glob("portal_audits/*"))



def import_audit():
    global arr
    file_name = fd.askopenfilename(initialdir="../portal_audits")
    if file_name:
        arr = []
    global structure
    structure = audit.main(file_name)
    for element in structure:
        for key in element:
            str = ''
            for char in element[key]:
                if char != '"' and char != "'":
                    str += char
            isspacefirst = True
            str2 = ''
            for char in str:
                if char == ' ' and isspacefirst:
                    continue
                else:
                    str2 += char
                    isspacefirst = False
            element[key] = str2

    global matching
    matching = structure
    if len(structure) == 0:
        f = open(file_name, 'r')
        structure = json.loads(f.read())
        f.close()
    for struct in structure:
        if 'description' in struct:
            arr.append(struct['description'])
        else:
            arr.append('Error in selecting')
    vars.set(arr)


lstbox = Listbox(frame, bg="#000000", font=myFont, fg="white", listvariable=vars, selectmode=MULTIPLE, width=95,
                 height=25, highlightthickness=3)
lstbox.config(highlightbackground="white")
lstbox.grid(row=0, column=0, columnspan=3, padx=100, pady=105)



def save_config():
    lstbox.select_set(0, END)
    for struct in structure:
        lstbox.insert(END, struct)

    file_name = fd.asksaveasfilename(filetypes=(("Audit FILES", ".audit"),
                                                ("All files", ".")))
    file_name += '.audit'
    file = open(file_name, 'w')
    selection = lstbox.curselection()
    for i in selection:
        tofile.append(matching[i])
    json.dump(tofile, file)
    file.close()



saveButton = Button(frame, bg="#0023FF", fg="white", font=myFont, text="Save", width=7, height=1,
                    command=save_config).place(relx=0.01, rely=0.099)
import_button = Button(frame, bg="#0023FF", fg="white", font=myFont, text="Import", width=7, height=1,
                       command=import_audit).place(relx=0.09, rely=0.099)
downloadButton = Button(frame, bg="#0023FF", fg="white", font=myFont, text="Download audits", width=15, height=1,
                        command=extract_download).place(relx=0.17, rely=0.099)

main.mainloop()