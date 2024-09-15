import tkinter as tk
import csv
import random

#ข้อแรก

def check_cowid():
    cowid = enter_id.get()
    global cowdata
    idmatch = False

    if len(cowid) != 8:
        message.config(text="ขาดหรือเกิน 8 อักษร", fg="red")
    elif not cowid.isdigit():
        message.config(text="ตัวเลขเท่านั้น", fg="red")
    elif cowid[0] == "0":
        message.config(text="ตัวแรกห้ามเป็น 0", fg="red")
    else:
        with open('cowdata.csv', newline='')as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['id'] == cowid:
                    idmatch = True
                    milkvalue = row['milk']
                    yearvalue = int(row['year'])
                    monthsvalue = int(row['months'])

                    cowdata = {
                        'id': cowid,
                        'year' : yearvalue,
                        'months' : monthsvalue,
                        'milk': milkvalue
                    }

                    if idmatch and milkvalue == '4':
                        milkscreen(yearvalue, monthsvalue)
                    elif idmatch and milkvalue == '3':
                        nomilkscreen()
                    elif idmatch and milkvalue == '':
                        goatscreen()
                    break
        
        if not idmatch:
            message.configure(text="ไม่พบวัว", fg="red")

def clearscreen():
    for widget in root.winfo_children():
        widget.pack_forget()

def mainscreen():
    clearscreen()

    label = tk.Label(root, text="ใส่ ID ของวัว ")
    label.pack(pady=20)

    global enter_id
    enter_id = tk.Entry(root)
    enter_id.pack(pady=10)

    button = tk.Button(root, text="ยืนยัน", command=check_cowid)
    button.pack(pady=20)

    global message
    message = tk.Label(root, text="")
    message.pack(pady=10)

def milkscreen(yearvalue, monthsvalue):
    clearscreen()
    nomilkmessage = tk.Label(root, text="วัวตัวนี้พร้อมแล้ว")
    nomilkmessage.pack(pady=20)

    milkbuttom = tk.Button(root, text="รีดนมวัว", command=lambda:sumofmilkscreen(yearvalue, monthsvalue))
    milkbuttom.pack(pady=20)

def sumofmilkscreen(yearvalue, monthsvalue):
    clearscreen()

    if cowdata['milk'] == 4 and random.random()<0.05:
        cowdata['milk'] = 3

    sumofmilk = yearvalue + monthsvalue
    milkvaluemessage = tk.Label(root, text=f"ได้นมมาทั้งหมด {sumofmilk} ลิตร")
    milkvaluemessage.pack(pady=20)

    with open('cowdata.csv', newline='')as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['id'] != cowdata['id'] and row['milk'] == 3:
                    if random.random()<0.20:
                        milkupdate(row['id'],4)

    backbuttom = tk.Button(root, text="เปลี่ยนวัว", command=mainscreen)
    backbuttom.pack(pady=20)

def nomilkscreen():
    clearscreen()

    nomilkmessage = tk.Label(root, text="มี 3 เต้าไม่สามารถรีดนมได้")
    nomilkmessage.pack(pady=20)

    backbuttom = tk.Button(root, text="เปลี่ยนวัว", command=mainscreen)
    backbuttom.pack(pady=20)

def goatscreen():
    clearscreen()

    goatmessage = tk.Label(root, text="มันคือแพะ!!")
    goatmessage.pack(pady=20)

    chasebuttom = tk.Button(root, text="ไล่แพะออก", command=mainscreen)
    chasebuttom.pack(pady=20)

def milkupdate(cowid, new_milkvalue):
    rows = []
    with open('cowdata.csv', newline='')as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['id'] == cowid:
                    row['milk'] == str(new_milkvalue)
                rows.append(row)

    with open('cowdata.csv', newline='')as csvfile:
        fieldnames = ['id', 'year', 'months', 'milk']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

root = tk.Tk()
root.title("cow")
root.geometry("400x300")

mainscreen()

root.mainloop()