import re
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from sqlite3 import *
import matplotlib.pyplot as plt
import requests

root=Tk()
root.title("Employee Management System By Rahul")
root.geometry("800x700+350+50")
f=("Times New Roman",25,"bold")
root.configure(bg="lightblue")

# ====Functions===========================================================================================
def f1():
    add_window.deiconify()
    root.withdraw()


def f2():
    root.deiconify()
    add_window.withdraw()


def f3():
    view_window.deiconify()
    root.withdraw()
    vw_st_data.delete(1.0, END)
    info = ""
    con = None
    try:
        con = connect("emp.db")
        cursor = con.cursor()
        sql = "select * from employee"
        cursor.execute(sql)
        data = cursor.fetchall()
        for d in data:
            info = info + "id: " + str(d[0]) + "   name: " + str(d[1]) + "   salary: " + str(d[2]) + "\n"
        vw_st_data.insert(INSERT, info)
    except Exception as e:
        showerror("Issue", e)
    finally:
        if con is None:
            con.close()


def f4():
    root.deiconify()
    view_window.withdraw()


def f5():
    update_window.deiconify()
    root.withdraw()


def f6():
    root.deiconify()
    update_window.withdraw()


def f7():
    delete_window.deiconify()
    root.withdraw()


def f8():
    root.deiconify()
    delete_window.withdraw()


def validate_name(name):
    if name == "" :
        showerror("ERROR", "Name can't be empty.")
        return False
    elif not name.isalpha():
        showerror("ERROR", "Invalid Name. Please enter alphabetic characters only.")
        return False
    elif name.strip() == "":
        showerror("ERROR", "Name cannot be spaces.")
        return False
    elif len(name)<2:
        showerror("ERROR", "Name length should be more than 2 characters.")
        return False
    return True


def validate_id(id):
    if id == "":
        showerror("ERROR", "ID can't be empty.")
        return False
    elif not id.strip():
        showerror("ERROR", "ID cannot be spaces.")
        return False
    elif not id.isdigit():
        showerror("ERROR", "ID should only cantain digits.")
        return False
    elif int(id) < 0:
        showerror("ERROR", "ID cannot be negative.")
        return False
    return True


def validate_salary(salary):
    if salary == "":
        showerror("ERROR", "Salary can't be empty.")
        return False
    elif not salary.strip():
        showerror("ERROR", "Salary cannot be spaces.")
        return False
    elif not salary.isdigit():
        showerror("ERROR", "Salary should only cantain digits.")
        return False
    elif int(salary) < 0:
        showerror("ERROR", "Salary cannot be negative.")
        return False
    return True


def f9():
    con = None
    try:
        con = connect("emp.db")
        cursor = con.cursor()
        sql = "insert into employee values('%d','%s','%s')"
        id = aw_ent_id.get()
        name = aw_ent_name.get()
        salary = aw_ent_salary.get()

        if not validate_id(id):
            aw_ent_id.delete(0,END)
            aw_ent_id.focus() 
            return
        elif not validate_name(name):
            aw_ent_name.delete(0,END)
            aw_ent_name.focus()
            return
        elif not validate_salary(salary):
            aw_ent_salary.delete(0,END)
            aw_ent_salary.focus()
            return
        cursor.execute(sql % (int(id), name, salary))
        con.commit()
        showinfo("Success", "Record added.")
    except Exception as e:
        showerror("Issue", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
    aw_ent_id.delete(0,END)
    aw_ent_name.delete(0,END)
    aw_ent_salary.delete(0,END)
    aw_ent_id.focus() 

def f10():
    con = None
    try:
        con = connect("emp.db")
        cursor = con.cursor()
        sql = "update employee set name = '%s', salary = '%s' where id = '%d'"
        id = uw_ent_id.get()
        name = uw_ent_name.get()
        salary = uw_ent_salary.get()

        if not validate_id(id):
            uw_ent_id.delete(0, END)
            uw_ent_id.focus()
            return
        elif not validate_name(name):
            uw_ent_name.delete(0, END)
            uw_ent_name.focus()
            return
        elif not validate_salary(salary):
            uw_ent_salary.delete(0,END)
            uw_ent_salary.focus()
            return
        cursor.execute(sql % (name, salary, int(id)))
        if cursor.rowcount == 1:
            con.commit()
            showinfo("Success", "Record updated.")
        else:
            showerror("Invalid", f"Employee with id {id} does not exist.")
    except Exception as e:
        showerror("Issue", e)
    finally:
        if con is not None:
            con.close()
    uw_ent_id.delete(0, END)
    uw_ent_name.delete(0, END)
    uw_ent_salary.delete(0,END)
    uw_ent_id.focus()


def f11():
    con = None
    try:
        con = connect("emp.db")
        cursor = con.cursor()
        sql = "delete from employee where id = '%d'"
        id = dw_ent_id.get()

        if not validate_id(id):
            dw_ent_id.delete(0,END)
            dw_ent_id.focus()
            return

        cursor.execute(sql % int(id))
        if cursor.rowcount == 1:
            showinfo('Success', 'Record deleted.')
            con.commit()
        else:
            showerror("Invalid", f"Employee with id {id} does not exist.")
    except Exception as e:
        showerror("Issue", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
    dw_ent_id.delete(0,END)
    dw_ent_id.focus()


def f12():
    con = None
    try:
        con = connect("emp.db")
        cursor = con.cursor()
        sql = "SELECT * FROM employee ORDER BY salary DESC LIMIT 5"
        cursor.execute(sql)
        data = cursor.fetchall()
        
        if len(data) == 0:
            showinfo('No Data', 'No employee data found.')
            return

        name = []
        salary = []
        for d in data:
            name.append(d[1])
            salary.append(d[2])
        
        plt.bar(name, salary, linewidth=4, color=['blue', 'green', 'yellow','orange','red'])
        plt.title("Top 5 Highest Salary Employees")
        plt.xlabel("Names")
        plt.ylabel("Salaries")
        plt.show()
    except Exception as e:
        showerror('Issue', e)
    finally:
        if con is not None:
            con.close()


def close():
    if askyesnocancel("Quit", "Do you want to exit?"):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", close)

# ======Main Window=======================================================================================
btn_add = Button(root, text="Add", font=f, width=10, fg="black", bg="yellow", command=f1)
btn_view = Button(root, text="View", font=f, width=10, fg="black", bg="yellow", command=f3)
btn_update = Button(root, text="Update", font=f, width=10, fg="black", bg="yellow", command=f5)
btn_delete = Button(root, text="Delete", font=f, width=10, fg="black", bg="yellow", command=f7)
btn_charts = Button(root, text="Charts", font=f, fg="black", width=10, bg="yellow", command=f12)

btn_add.pack(pady=10)
btn_view.pack(pady=10)
btn_update.pack(pady=10)
btn_delete.pack(pady=10)
btn_charts.pack(pady=10)

response = requests.get("https://ipapi.co/json/")
if response.status_code == 200:
    location_data = response.json()
    city = location_data['city']
    region = location_data['region']
    country = location_data['country_name']
    location_text = f"Location: {city}, {region}, {country}"
    lbl_loc = Label(root, text=location_text, font=f, fg="black", bg="yellow")
    lbl_loc.place(x=120, y=500)
    api_key = "c41d1ea9fa38bad27e306fd27af250ee"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric"
    weather_response = requests.get(weather_url)
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        temperature = weather_data['main']['temp']
        temp_text = f"Temperature: {temperature}°C"
        lbl_temp = Label(root, text=temp_text, font=f, fg="black", bg="yellow")
        lbl_temp.place(x=230, y=550)

# ============Add Window==================================================================================
add_window = Toplevel(root)
add_window.title("Add Employee")
add_window.geometry("800x700+400+50")

add_window.configure(bg='lightblue')
aw_lbl_id = Label(add_window, text="Enter Id", bg="yellow",font=f)
aw_ent_id = Entry(add_window, bd=4, width=20, font=f)
aw_lbl_name = Label(add_window, text="Enter Name", bg="yellow",font=f)
aw_ent_name = Entry(add_window, bd=4, width=20, font=f)
aw_lbl_salary = Label(add_window, text="Enter Salary", bg="yellow",font=f)
aw_ent_salary = Entry(add_window, bd=4, width=20, font=f)
aw_btn_save = Button(add_window, text="Save", font=f, bg="light green", command=f9)
aw_btn_back = Button(add_window, text="Back", font=f, bg="yellow", command=f2)

aw_lbl_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lbl_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lbl_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)

add_window.withdraw()
add_window.protocol("WM_DELETE_WINDOW", close)
# ============View Window=================================================================================
view_window = Toplevel(root)
view_window.title("View Employee")
view_window.geometry("800x700+400+50")

view_window.configure(bg='lightblue')
vw_st_data = ScrolledText(view_window, width=40, height=15, font=f, bg="white")
btn_back = Button(view_window, text="Back", font=f, bg="yellow", command=f4)

vw_st_data.pack()
btn_back.pack(pady=50)

view_window.withdraw()
view_window.protocol("WM_DELETE_WINDOW", close)

# ============Update Window===============================================================================
update_window = Toplevel(root)
update_window.title("Update Employee")
update_window.geometry("800x700+400+50")

update_window.configure(bg='lightblue')
lbl_id = Label(update_window, text="Enter Id",bg="yellow", font=f)
uw_ent_id = Entry(update_window, bd=4, width=20, font=f)
lbl_name = Label(update_window, text="Enter Name", bg="yellow",font=f)
uw_ent_name = Entry(update_window, bd=4, width=20, font=f)
lbl_salary = Label(update_window, text="Enter Salary",bg="yellow", font=f)
uw_ent_salary = Entry(update_window, bd=4, width=20, font=f)
btn_save = Button(update_window, text="Save", font=f, bg="light green", command=f10)
btn_back = Button(update_window, text="Back", font=f, bg="yellow", command=f6)

lbl_id.pack(pady=10)
uw_ent_id.pack(pady=10)
lbl_name.pack(pady=10)
uw_ent_name.pack(pady=10)
lbl_salary.pack(pady=10)
uw_ent_salary.pack(pady=10)
btn_save.pack(pady=10)
btn_back.pack(pady=10)

update_window.withdraw()
update_window.protocol("WM_DELETE_WINDOW", close)

# =============Delete Window=============================================================================
delete_window = Toplevel(root)
delete_window.title("Delete Employee")
delete_window.geometry("800x700+400+50")

delete_window.configure(bg='lightblue')
lbl_id = Label(delete_window, text="Enter Id", bg="yellow",font=f)
dw_ent_id = Entry(delete_window, bd=6, width=20, font=f)
btn_save = Button(delete_window, text="Delete", font=f, bg="red", command=f11)
btn_back = Button(delete_window, text="Back", font=f, bg="yellow", command=f8)

lbl_id.pack(pady=20)
dw_ent_id.pack(pady=20)
btn_save.pack(pady=20)
btn_back.pack(pady=20)
delete_window.withdraw()
delete_window.protocol("WM_DELETE_WINDOW", close)

root.mainloop()
