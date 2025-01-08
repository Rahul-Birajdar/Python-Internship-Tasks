from tkinter import *
from tkinter import messagebox
import re
from matplotlib import pyplot as plt

def validate_loan_amount(loan_amount_str):
    try:
        loan_amount = float(loan_amount_str)

        # Check if the loan amount is positive
        if loan_amount <= 0:
            raise ValueError("Loan amount must be a positive number.")

        # Check if the loan amount is within a certain range (you can modify the limits as needed)
        min_loan_amount = 0
        max_loan_amount = 1000000
        if loan_amount < min_loan_amount or loan_amount > max_loan_amount:
            raise ValueError(f"Loan amount must be between {min_loan_amount} and {max_loan_amount}.")

    except ValueError:
        raise ValueError("Max Loan Amount should be 1000000 rupees.")

    return loan_amount
    

def validate_loan_tenure(loan_tenure_str):
    try:
        loan_tenure = int(loan_tenure_str)

        # Check if the loan tenure is positive
        if loan_tenure <= 0:
            raise ValueError("Loan tenure must be a positive integer.")

        # Check if the loan tenure is within a certain range (you can modify the limits as needed)
        min_loan_tenure = 0
        max_loan_tenure = 30
        if loan_tenure < min_loan_tenure or loan_tenure > max_loan_tenure:
            raise ValueError(f"Loan tenure must be between {min_loan_tenure} and {max_loan_tenure} years.")

    except ValueError:
        raise ValueError("Max Loan Tenure should be 30 years.")

    return loan_tenure
    

def validate_interest_rate(interest_rate_str):
    try:
        interest_rate = float(interest_rate_str)

        # Check if the interest rate is positive
        if interest_rate <= 0:
            raise ValueError("Interest rate must be a positive number.")

        # Check if the interest rate is within a certain range (you can modify the limits as needed)
        min_interest_rate = 0
        max_interest_rate = 20
        if interest_rate < min_interest_rate or interest_rate > max_interest_rate:
            raise ValueError(f"Interest rate must be between {min_interest_rate}% and {max_interest_rate}%.")

    except ValueError:
        raise ValueError("Max Interest Rate should be 20%.")

    return interest_rate

def display_pie_chart(total_interest, loan_amount):
    # Calculate the principal amount (loan amount - total interest)
    principal_amount = loan_amount - total_interest

    # Create data for the pie chart
    data = [principal_amount, total_interest]
    labels = ['Principal Amount', 'Total Interest Payable']
    colors = ['skyblue', 'orange']

    # Create the pie chart
    plt.figure(figsize=(5, 5))
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=120)
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle.

    # Display the pie chart
    plt.show()

def calculate_loan():
    try:
        loan_amount_str = loan_amount_entry.get().strip()
        loan_tenure_str = loan_tenure_entry.get().strip()
        interest_rate_str = interest_rate_entry.get().strip()

        # Check if the loan amount is empty
        if not loan_amount_str:
            raise ValueError("Loan amount cannot be empty.")
        # Check if the loan amount contains only digits
        if not re.match(r'^\d+(\.\d+)?$', loan_amount_str):
            raise ValueError("Loan amount must contain only digits.")
        
        # Check if the loan tenure is empty
        if not loan_tenure_str:
            raise ValueError("Loan tenure cannot be empty.")
        # Check if the loan tenure contains only digits
        if not re.match(r'^\d+$', loan_tenure_str):
            raise ValueError("Loan tenure must contain only digits.")
        
        # Check if the interest rate is empty
        if not interest_rate_str:
            raise ValueError("Interest rate cannot be empty.")
        # Check if the interest rate contains only digits and an optional decimal point
        if not re.match(r'^\d+(\.\d+)?$', interest_rate_str):
            raise ValueError("Interest rate must contain only digits.")
        
        # Validate the loan amount
        loan_amount = validate_loan_amount(loan_amount_str)
        # Validate the loan tenure
        loan_tenure = validate_loan_tenure(loan_tenure_str)
        # Validate the interest rate
        interest_rate = validate_interest_rate(interest_rate_str)

        loan_tenure=int(loan_tenure_entry.get())
        interest_rate=float(interest_rate_entry.get())
        interest_rate = float(interest_rate_entry.get())
        
        #Claculation for EMI
        r=interest_rate/(12*100)
        n=loan_tenure*12
        emi=(loan_amount*r*pow(1+r,n))/(pow(1+r,n)-1)

        total_payment=emi*n
        total_interest=total_payment-loan_amount

        emi_label.config(text=f"EMI Amount : {emi:10.2f}")
        total_interest_label.config(text=f"Total Interest Payable : {total_interest:10.2f}")
        total_payment_label.config(text=f"Total Payment : {total_payment:10.2f}")

        # Display the pie chart
        display_pie_chart(total_interest, loan_amount)

    except ValueError as e:
        messagebox.showerror("Input Error",str(e))
        clear_fields()

def clear_fields():
    loan_amount_entry.delete(0,END)
    loan_tenure_entry.delete(0,END)
    interest_rate_entry.delete(0,END)

    emi_label.config(text="EMI Amount : ")
    total_interest_label.config(text="Total Interest Payable : ")
    total_payment_label.config(text="Total Payment : ")
    pass

#GUI
root=Tk()
root.title("Loan Calculator By Rahul")
root.geometry("800x600+400+100")
root.configure(bg="lightblue")
#font
f = ("Times New Roman",15,"bold","italic")
ft = ("Times New Roman",25,"bold")

LC_label=Label(root,text="Welcome to Loan Calculator",font=ft,anchor="center",bg="yellow")
LC_label.pack(pady=20)

loan_amount_label=Label(root,text="Loan Amount(in rupees) : ",font=f,bg="yellow",width=25)
loan_amount_label.place(x=120,y=100)
loan_amount_entry=Entry(root,font=f,width=25)
loan_amount_entry.place(x=420,y=100)
la_label = Label(text = "Range : 0 to 1000000 ",font=("Times New Roman",10,"bold","italic"),bg="orange")
la_label.place(x=420,y=130)

loan_tenure_label=Label(root,text="Loan Tenure(in years) : ",font=f,bg="yellow",width=25)
loan_tenure_label.place(x=120,y=150)
loan_tenure_entry=Entry(root,font=f,width=25)
loan_tenure_entry.place(x=420,y=150)
lt_label = Label(text = "Range : 0 to 30 ",font=("Times New Roman",10,"bold","italic"),bg="orange")
lt_label.place(x=420,y=180)

interest_rate_label=Label(root,text="Interest Rate(%per annum) : ",font=f,bg="yellow",width=25)
interest_rate_label.place(x=120,y=200)
interest_rate_entry=Entry(root,font=f,width=25)
interest_rate_entry.place(x=420,y=200)
ir_label = Label(text = "Range : 0 to 20 ",font=("Times New Roman",10,"bold","italic"),bg="orange")
ir_label.place(x=420,y=230)

calculate_button=Button(root,text="Calculate",command=calculate_loan,font=f,bg="lightgreen",width=25)
calculate_button.place(x=250,y=280)

emi_label=Label(root,text="EMI Amount : ",font=f,bg="yellow",width=35)
emi_label.place(x=200,y=350)

total_interest_label=Label(root,text="Total Interest Payable : ",font=f,bg="yellow",width=35)
total_interest_label.place(x=200,y=400)

total_payment_label=Label(root,text="Total Payment : ",font=f,bg="yellow",width=35)
total_payment_label.place(x=200,y=450)

clear_button=Button(root,text="Clear",command=clear_fields,font=f,bg="red",width=25)
clear_button.place(x=250,y=520)

r_label = Label(text = "By Rahul ",font=("Times New Roman",20,"bold","italic"),bg="yellow")
r_label.place(x=650,y=550)

root.mainloop()
