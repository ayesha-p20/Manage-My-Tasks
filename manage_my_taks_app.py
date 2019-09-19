#MANAGE MY TASKS
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import tkinter.font as font
import sqlite3

#db
conn = sqlite3.connect('reminders.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS schedule (TASK text, CATEGORY text, DEADLINE text, TIME text, NOTES text)')
conn.commit()

def close():
    conn.close()
    win.destroy()
    
def insert_data():
    c.execute('INSERT INTO schedule VALUES(?,?,?,?,?)', (entry_task.get(),combo_category.get() ,entry_date.get(),entry_time.get(), text_box.get("1.0",END)))
    conn.commit()

def get_data():
    c.execute("SELECT * FROM schedule")
    return c.fetchall()

def update_data(taskval, category, deadline, times, notes,choice):
    c.execute("UPDATE schedule SET TASK = (?), CATEGORY = (?), DEADLINE = (?), TIME  = (?), NOTES  = (?) WHERE TASK  = (?)", (taskval, category, deadline, times, notes, choice))
    conn.commit()
    messagebox.showinfo("SUCCESS","CHANGES SAVED")
    
def delete_task(choice):
    c.execute("DELETE FROM schedule WHERE TASK = (?)", ([choice]))
    conn.commit()
    messagebox.showinfo("SUCCESS","TASK DELETED")

def edit(var_value):
    edit_win = Toplevel(bg = "beige")
    edit_win.title("EDIT")
    edit_win.resizable(0,0)
    pc_width = edit_win.winfo_screenwidth()
    pc_height = edit_win.winfo_screenheight()
    x_value = pc_width/2 - 340
    y_value = pc_height/2 - 175
    edit_win.geometry("681x350+%d+%d"%(x_value,y_value))
    data = var_value.get()
    c.execute("SELECT * FROM schedule WHERE TASK =(?)", ([data]))   
    #labels
    label_taskname = Label(edit_win, text = "TASK:", bg = "beige", font = ("Helvetica",10,"bold"))
    label_taskname.place(x = 10, y = 30)
    label_category = Label(edit_win, text = "CATEGORY:",bg = "beige", font = ("Helvetica",10,"bold"))
    label_category.place(x = 10, y = 75)
    label_deadline = Label(edit_win, text = "DEADLINE:",bg = "beige", font = ("Helvetica",10,"bold"))
    label_deadline.place(x = 10, y = 120)
    label_time = Label(edit_win, text = "TIME:",bg = "beige", font = ("Helvetica",10,"bold"))
    label_time.place(x = 10, y = 165)
    label_notes = Label(edit_win, text = "NOTES:",bg = "beige", font = ("Helvetica",10,"bold"))
    label_notes.place(x = 10, y = 210)
    #entry
    entry_taskname = Entry(edit_win,bd = 3, width = 20)
    entry_taskname.insert(0,"TASK")
    entry_taskname.place(x = 200, y = 30)
    entry_deadline = Entry(edit_win,bd = 3,width = 20)
    entry_deadline.insert(0,"DEADLINE(mm/dd/yy)")
    entry_deadline.place(x = 200, y = 120)
    entry_times = Entry(edit_win,bd = 3,width = 20)
    entry_times.insert(0,"TIME(hr:min)")
    entry_times.place(x = 200, y = 165)
    #combobox
    options = ['Work','Appointment', 'Leisure', 'Other']
    combo_cat = Combobox(edit_win,values = options ,width=17)
    combo_cat.set("CATEGORY")
    combo_cat.place(x = 200, y = 75)
    #text box
    text_notes = Text(edit_win,width=71,height=1,wrap=WORD,padx=10,pady=10,bd=4,selectbackground="blue",font=("Helvetica",10))
    text_notes.place(x = 10,y = 230)
    #buttons
    button_delete = Button(edit_win, text = "DELETE TASK", height = 2, width = 20,bg = "dark red",fg = "white",font = ("Helvetica",8,"bold"), command = lambda: [delete_task(data),edit_win.destroy()])
    button_delete.place(x = 502, y = 290)
    button_save = Button(edit_win, text = "SAVE", height = 2, width = 20, bg = "dark red", fg = "white", font = ("Helvetica",8,"bold"), command = lambda: [update_data(entry_taskname.get(),combo_cat.get() ,entry_deadline.get(),entry_times.get(), text_notes.get("1.0",END), data),edit_win.destroy()])
    button_save.place(x = 10, y = 290)
    
def view_data():                       
    view_win = Toplevel()
    view_win.title("SHOW MY TASK LIST")
    pc_width = view_win.winfo_screenwidth()
    pc_height = view_win.winfo_screenheight()
    view_win.geometry("1300x{0}+%d+%d".format(pc_height)%(pc_width/2-650, 0))
    label_edit = Label(view_win, text = "SELECT A TASK TO EDIT IT",font = ("Helvetica",10,"bold"))
    label_edit.grid(row = 0, column = 1, padx = 10, pady = 10)
    label_task = Label(view_win, text = "TASK", width = 12,font = ("Helvetica",10,"bold"))
    label_task.grid(row = 4, column = 1, padx = 30, columnspan = 2, sticky = N+S+E+W)
    label_category = Label(view_win, text = "CATEGORY",width = 12,font = ("Helvetica",10,"bold"))
    label_category.grid(row = 4, column = 3, padx = 30, columnspan = 2, sticky = N+S+E+W)
    label_deadline = Label(view_win, text = "DEADLINE",width = 12,font = ("Helvetica",10,"bold"))
    label_deadline.grid(row = 4, column = 5, padx = 30, columnspan = 2, sticky = N+S+E+W)
    label_time = Label(view_win, text = "TIME",width = 12,font = ("Helvetica",10,"bold"))
    label_time.grid(row = 4, column = 7, padx = 30, columnspan = 2, sticky = N+S+E+W)
    label_notes = Label(view_win, text = "NOTES",width = 12,font = ("Helvetica",10,"bold"))
    label_notes.grid(row = 4, column = 9, padx = 30, pady = 20, columnspan = 3, sticky = N+S+E+W)
    info = get_data()
    var = StringVar(value = "-1")
    for i, x in enumerate(info):
          Radiobutton(view_win, variable = var, value = info[i][0]).grid(row = i+6, column = 0, sticky = N+S+E+W)
          Label(view_win, text = info[i][0]).grid(row = i+6, column = 1, padx = 30, columnspan = 2, sticky = N+S+E+W)
          Label(view_win, text = info[i][1]).grid(row = i+6, column = 3, padx = 30, columnspan = 2, sticky = N+S+E+W)
          Label(view_win, text = info[i][2]).grid(row = i+6, column = 5, padx = 30, columnspan = 2, sticky = N+S+E+W)
          Label(view_win, text = info[i][3]).grid(row = i+6, column = 7, padx = 30, columnspan = 2, sticky = N+S+E+W)
          Label(view_win, text = "\n" + info[i][4]).grid(row = i+6, column = 9, padx = 30, pady = 20, columnspan = 3, sticky = N+S+E+W)
    
    button_edit = Button(view_win,text = "EDIT TASK",height = 2, width = 20,bg = "dark red",fg = "white",font = ("Helvetica",8,"bold"),command = lambda: [edit(var), view_win.destroy()])
    button_edit.grid(row = 0, column = 3, padx = 10, pady = 10)
    
#app interface
win = Tk()
win.title("MANAGE MY TASKS")
pc_width = win.winfo_screenwidth()
pc_height = win.winfo_screenheight()
x_val = pc_width/2 - 340
y_val = pc_height/2 - 175
win.geometry("681x350+%d+%d"%(x_val,y_val))
win.resizable(0,0)
win.configure(background = "beige")

def_font = font.Font(size = 8,weight = "bold")

#label
label = Label(win,text = "SCHEDULE A NEW EVENT:",bg = "beige",font = ("Helvetica",10,"bold"))
label.place(x = 235, y = 20)
label_notes = Label(win, text = "NOTES", bg = "beige", font = ("Helvetica",10))
label_notes.place(x = 8, y = 90)
label_or = Label(win, text = "OR", bg = "beige", font = ("Helvetica",10, "bold"))
label_or.place(x = 330, y = 250)

#entries
entry_task = Entry(win,bd = 3, width = 19)
entry_task.insert(0,"TASK")
entry_task.place(x = 8, y = 50)
entry_date = Entry(win,bd = 3,width = 19)
entry_date.insert(0,"DEADLINE(mm/dd/yy)")
entry_date.place(x = 344, y = 50)
entry_time = Entry(win,bd = 3,width = 19)
entry_time.insert(0,"TIME(hr:min)")
entry_time.place(x = 516, y = 50)

#combobox
options = ['Work','Appointment', 'Leisure', 'Other']
combo_category = Combobox(win,values = options ,width=16)
combo_category.set("CATEGORY")
combo_category.place(x = 177, y = 50)

#text box
text_box = Text(win,width=71,height=1,wrap=WORD,padx=10,pady=10,bd=4,selectbackground="blue",font=("Helvetica",10))
text_box.place(x = 8,y = 115)

#buttons
button_new = Button(win,text = "CREATE NEW REMINDER",height = 2, width = 20,bg = "dark red",fg = "white",command = insert_data)
button_view = Button(win, text = "SHOW MY TASK LIST",height = 2, width = 20,bg = "dark red",fg = "white",command = view_data)
button_cancel = Button(win,text = "CANCEL",height = 2, width = 20,bg = "dark red",fg = "white",command = close)
button_new["font"] = def_font
button_view["font"] = def_font
button_cancel["font"] = def_font
button_new.place(x = 261,y = 180)
button_view.place(x = 70,y = 290)
button_cancel.place(x = 450,y = 290)

win.mainloop()
