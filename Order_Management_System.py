import re
from tkinter import *
from tkinter.scrolledtext import *
from tkinter.messagebox import *
from sqlite3 import *

from matplotlib import pyplot as plt

root = Tk()
root.title("Order Management System By Rahul")
root.geometry("500x450+500+150")
f = ("Times New Roman", 18, "bold")
root.configure(bg="lightblue")

# Admin credentials
admin_username = "admin"
admin_password = "123456"
admin_authenticated = False 

# Functions
def admin_login():
    global admin_authenticated
    username = admin_username_entry.get()
    password = admin_password_entry.get()

    if username == admin_username and password == admin_password:
        admin_authenticated = True
        admin_login_window.withdraw()
    else:
        showerror("Invalid Login", "Invalid username or password.")
        admin_password_entry.delete(0, END)
        admin_username_entry.focus()


def open_view_window():
    if admin_authenticated:
        view_window.deiconify()
    else:
        showerror("Access Denied", "Please log in as admin first.")

def open_delete_window():
    if admin_authenticated:
        delete_window.deiconify()
    else:
        showerror("Access Denied", "Please log in as admin first.")


def close():
    if askyesnocancel("Quit", "Do you want to exit?"):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", close)

# Admin Login Window
admin_login_window = Toplevel(root)
admin_login_window.title("Admin Login")
admin_login_window.geometry("500x450+500+150")
admin_login_window.configure(bg="lightblue")

admin_lbl_username = Label(admin_login_window, text="Username:", font=f)
admin_username_entry = Entry(admin_login_window, bd=3, width=20, font=f)
admin_lbl_password = Label(admin_login_window, text="Password:", font=f)
admin_password_entry = Entry(admin_login_window, bd=3, width=20, font=f, show="*")
admin_btn_login = Button(admin_login_window, text="Login", font=f, bg="lightgreen", command=admin_login)

admin_lbl_username.pack(pady=10)
admin_username_entry.pack(pady=5)
admin_lbl_password.pack(pady=10)
admin_password_entry.pack(pady=5)
admin_btn_login.pack(pady=15)
admin_login_window.protocol("WM_DELETE_WINDOW", close)

# Main Window Functions
def f1():
    add_window.deiconify()
    root.withdraw()

def f2():
    root.deiconify()
    add_window.withdraw()

def f3():
    if admin_authenticated:
        view_window.deiconify()
        root.withdraw()
        vw_st_data.delete(1.0, END)
        
        con = None
        try:
            con = connect("order.db")
            cursor = con.cursor()
            sql = "SELECT * FROM orders"
            cursor.execute(sql)
            data = cursor.fetchall()
            
            for d in data:
                info = ("Name: "+ str(d[0])+ "\n"
                    + "Phone: "+ str(d[1])+ "\n"
                    + "Email: "+ str(d[2])+ "\n"
                    + "Delivery Address: "+ str(d[3])+ "\n"
                    + "Drinks: Tea: {}, Coffee: {}, Juice: {}, Milkshake: {}, Soda: {}".format(d[4], d[5], d[6], d[7], d[8])+ "\n\n"
                )
                vw_st_data.insert(INSERT, info)

                drink_preferences = {
                "Tea": 0,
                "Coffee": 0,
                "Juice": 0,
                "Milkshake": 0,
                "Soda": 0
            }
            
            for d in data:
                for drink, preference in zip(drink_preferences.keys(), d[4:]):
                    drink_preferences[drink] += preference
            
            # Generate the bar graph
            drinks = list(drink_preferences.keys())
            preferences = list(drink_preferences.values())
            
            plt.bar(drinks, preferences)
            plt.xlabel("Drink Preferences")
            plt.ylabel("Number of Orders")
            plt.title("Drink Preferences of Orders")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            showerror("Issue", e)
        finally:
            if con is not None:
                con.close()
    else:
        showerror("Access Denied", "Please log in as admin first.")

def f4():
    root.deiconify()
    view_window.withdraw()

def f7():
    if admin_authenticated:
        delete_window.deiconify()
        root.withdraw()
    else:
        showerror("Access Denied", "Please log in as admin first.")

def f8():
    root.deiconify()
    delete_window.withdraw()

def validate_name(name):
    if not name:
        showerror("ERROR", "Name can't be empty.")
        return False
    elif not name.isalpha():
        showerror("ERROR", "Invalid Name. Please enter alphabetic characters only.")
        return False
    elif not name.strip():
        showerror("ERROR","Name cannot be Spaces.")
        return False
    elif len(name) < 2 :
        showerror("ERROR", "Name length should be more than 2  characters.")
        return False
    return True


def validate_phone(phone):
    if not phone :
        showerror("ERROR", "Phone number can't be empty.")
        return False
    elif not phone.isdigit():
        showerror("ERROR", "Phone number should only contain digits.")
        return False
    elif not phone.strip():
        showerror("ERROR", "Phone number cannot be spaces.")
        return False
    elif len(phone) != 10:
        showerror("ERROR", "Invalid Phone number. Please enter a 10-digit numeric phone number.")
        return False
    return True

def validate_email(email):
    if not email:
        showerror("ERROR", "Email address can't be empty.")
        return False
    elif isinstance(email, int) or email.strip().isdigit():
        showerror("ERROR", "Invalid Email address. Email cannot be all numeric.")
        return False
    elif email.strip() == "":
        showerror("ERROR", "Email address can't consist of spaces only.")
        return False
    elif "@" not in email or "." not in email:
        showerror("ERROR", "Invalid Email address. Please enter a valid email format.")
        return False
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        showerror("ERROR", "Invalid Email address. Please enter a valid email format.")
        return False
    elif len(email) < 5:
        showerror("ERROR", "Email address should be at least 5 characters.")
        return False
    return True
    

def validate_delivery_address(address):
    MIN_ADDRESS_LENGTH = 5  # Adjust as needed
    MAX_ADDRESS_LENGTH = 30  # Adjust as needed
    
    if address == "":
        showerror("ERROR", "Delivery address can't be empty.")
        return False
    elif address.isdigit():
        showerror("ERROR", "Delivery address can't consist of only numbers.")
        return False
    elif address.isalpha():
        showerror("ERROR", "Delivery address can't consist of only text.")
        return False
    elif address.isspace():
        showerror("ERROR", "Delivery address can't consist of only spaces.")
        return False
    elif address.isalnum() and not any(char.isalpha() for char in address):
        showerror("ERROR", "Delivery address can't consist of only special characters.")
        return False
    elif len(address) < MIN_ADDRESS_LENGTH:
        showerror("ERROR", f"Delivery address should have at least {MIN_ADDRESS_LENGTH} characters.")
        return False
    elif len(address) > MAX_ADDRESS_LENGTH:
        showerror("ERROR", f"Delivery address should not exceed {MAX_ADDRESS_LENGTH} characters.")
        return False
    return True


def f9():
    con = None
    try:
        con = connect("order.db")
        cursor = con.cursor()
        sql = "insert into orders values('%s','%s','%s','%s','%d','%d','%d','%d','%d')"
        #sql_check_email = "SELECT * FROM orders WHERE email = '%s'"
        name = aw_ent_name.get()
        phone = (aw_ent_phone.get())
        email = aw_ent_email.get()
        delivery_address = aw_ent_delivery.get()
        tea = int(aw_var_tea.get()) if aw_var_tea.get() else 0
        coffee = int(aw_var_coffee.get()) if aw_var_coffee.get() else 0
        juice = int(aw_var_juice.get()) if aw_var_juice.get() else 0
        milkshake = int(aw_var_milkshake.get()) if aw_var_milkshake.get() else 0
        soda = int(aw_var_soda.get()) if aw_var_soda.get() else 0

        if not validate_name(name):
            aw_ent_name.delete(0, END)
            aw_ent_name.focus()
            return
        
        elif not validate_phone(str(phone)):
            aw_ent_phone.delete(0, END)
            aw_ent_phone.focus()
            return
        
        elif not validate_email(email):
            aw_ent_email.delete(0, END)
            aw_ent_email.focus()
            return
        
        elif not validate_delivery_address(delivery_address):
            aw_ent_delivery.delete(0, END)
            aw_ent_delivery.focus()
            return
        
        
        # Check if email already exists
#        cursor.execute(sql_check_email, (email,))
#        if cursor.fetchone():
#            showerror("Error", "Email already exists. Please use a different email.")
#            return
        
        cursor.execute(sql % (name, phone, email, delivery_address, tea, coffee, juice, milkshake, soda))
        con.commit()
        showinfo("Success", "Order added.")
    except Exception as e:
        showerror("Issue", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()

    # Clear input fields and checkboxes
    aw_ent_name.delete(0, END)
    aw_ent_phone.delete(0, END)
    aw_ent_email.delete(0, END)
    aw_ent_delivery.delete(0, END)
    aw_chk_tea.deselect()
    aw_chk_coffee.deselect()
    aw_chk_juice.deselect()
    aw_chk_milkshake.deselect()
    aw_chk_soda.deselect()


def f11():
    con = None
    try:
        con = connect("order.db")
        cursor = con.cursor()
        sql = "delete from orders where name = ?"  # Delete by name
        name = dw_ent_name.get()  # Get the name from the entry widget

        if not validate_name(name):
            dw_ent_name.delete(0, END)
            dw_ent_name.focus()
            return

        cursor.execute(sql, (name,))  # Pass the name as a parameter
        if cursor.rowcount >= 1:  # Check if any rows were affected
            showinfo('Success', 'Order deleted.')
            con.commit()
        else:
            showerror("Invalid", f"Order with name '{name}' does not exist.")
    except Exception as e:
        showerror("Issue", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
    dw_ent_name.delete(0, END)
    dw_ent_name.focus()

# Main Window
btn_add = Button(root, text="Add Order", font=f, width=20, fg="black", bg="yellow", command=f1)
btn_adm = Button(root, text="Admin", font=f, width=20, fg="black", bg="yellow", command=admin_login)
btn_view = Button(root, text="View Orders", font=f, width=20, fg="black", bg="yellow", command=f3)
btn_delete = Button(root, text="Delete Order", font=f, width=20, fg="black", bg="yellow", command=f7)

btn_add.pack(pady=10)
btn_adm.pack(pady=10)
btn_view.pack(pady=10)
btn_delete.pack(pady=10)

# Add Window
add_window = Toplevel(root)
add_window.title("Add Order")
add_window.geometry("800x720+400+50")
add_window.configure(bg="lightblue")

aw_lbl_name = Label(add_window, text="Enter name", font=f)
aw_ent_name = Entry(add_window, bd=3, width=20, font=f)
aw_lbl_phone = Label(add_window, text="Enter phone", font=f)
aw_ent_phone = Entry(add_window, bd=3, width=20, font=f)
aw_lbl_email = Label(add_window, text="Enter email", font=f)
aw_ent_email = Entry(add_window, bd=3, width=25, font=f)
aw_lbl_delivery = Label(add_window, text="Enter delivery address", font=f)
aw_ent_delivery = Entry(add_window, bd=3, width=30, font=f)
aw_lbl_drinks = Label(add_window, text="Select drinks:", font=f)
aw_var_tea = IntVar(value=1)  # Set the default value for Tea checkbox
aw_var_coffee = IntVar()
aw_var_juice = IntVar()
aw_var_milkshake = IntVar()
aw_var_soda = IntVar()
aw_chk_tea = Checkbutton(add_window, text="Tea", variable=aw_var_tea, font=10)
aw_chk_coffee = Checkbutton(add_window, text="Coffee", variable=aw_var_coffee, font=10)
aw_chk_juice = Checkbutton(add_window, text="Juice", variable=aw_var_juice, font=10)
aw_chk_milkshake = Checkbutton(add_window, text="Milkshake", variable=aw_var_milkshake, font=10)
aw_chk_soda = Checkbutton(add_window, text="Soda", variable=aw_var_soda, font=10)
aw_btn_save = Button(add_window, text="Save", font=f, bg="lightgreen", command=f9)
aw_btn_back = Button(add_window, text="Back", font=f, bg="yellow", command=f2)


aw_lbl_name.pack(pady=5)
aw_ent_name.pack(pady=5)
aw_lbl_phone.pack(pady=5)
aw_ent_phone.pack(pady=5)
aw_lbl_email.pack(pady=5)
aw_ent_email.pack(pady=5)
aw_lbl_delivery.pack(pady=5)
aw_ent_delivery.pack(pady=5)
aw_lbl_drinks.pack(pady=5)
aw_chk_tea.pack(pady=5)
aw_chk_coffee.pack(pady=5)
aw_chk_juice.pack(pady=5)
aw_chk_milkshake.pack(pady=5)
aw_chk_soda.pack(pady=5)
aw_btn_save.pack(pady=5)
aw_btn_back.pack(pady=5)


add_window.withdraw()
add_window.protocol("WM_DELETE_WINDOW", close)


# View Window
view_window = Toplevel(root)
view_window.title("View Orders")
view_window.geometry("840x650+400+50")
view_window.configure(bg="lightblue")

view_window.configure(bg='lightblue')
vw_st_data = ScrolledText(view_window, width=60, height=20, font=f, bg="white")
btn_back = Button(view_window, text="Back", font=f, bg="yellow", command=f4)

vw_st_data.pack()
btn_back.pack(pady=40)

view_window.withdraw()
view_window.protocol("WM_DELETE_WINDOW", close)

# Delete Window
delete_window = Toplevel(root)
delete_window.title("Delete Order")
delete_window.geometry("600x500+450+150")
delete_window.configure(bg="lightblue")

lbl_name = Label(delete_window, text="Enter name", font=f)
dw_ent_name = Entry(delete_window, bd=6, width=20, font=f)
btn_save = Button(delete_window, text="Delete Order", font=f, bg="lightgreen", command=f11)
btn_back = Button(delete_window, text="Back", font=f, bg="yellow", command=f8)

lbl_name.pack(pady=20)
dw_ent_name.pack(pady=20)
btn_save.pack(pady=20)
btn_back.pack(pady=20)
delete_window.withdraw()
delete_window.protocol("WM_DELETE_WINDOW", close)


root.mainloop()
