from tkinter import *
from datetime import *
import time
import threading
from time import strftime
from tkinter.messagebox import *

def f1():
	cw.deiconify()
	mw.withdraw()
def f2():
	mw.deiconify()
	cw.withdraw()
def f3():
	ct.deiconify()
	mw.withdraw()
def f4():
	mw.deiconify()
	ct.withdraw()
def f5():
    alarm_frame.deiconify()
    mw.withdraw()
def f6():
    mw.deiconify()
    alarm_frame.withdraw()  
def f7():
    world_clock_frame.deiconify()
    mw.withdraw()
def f8():
    mw.deiconify()
    world_clock_frame.withdraw()
def f9():
    stopwatch_frame.deiconify()
    mw.withdraw()
def f10():
    mw.deiconify()
    stopwatch_frame.withdraw()

#window    
mw = Tk()
mw.title("Digital Clock By Rahul")
mw.geometry("1000x720+250+40")
mw.configure(bg="yellow")
#font
f = ("Times New Roman",40,"bold")
ft = ("Times New Roman",25,"bold","italic")
#label for heading
lbl_Welcome = Label(mw,text = "Welcome To Digital Clock ",font = f, anchor="center",bg="orange" )
lbl_Welcome.pack(pady=20)
#buttons for current time and date,timer,alarm
btn_current = Button(mw,text = "Current time and date",font=ft,bg="orange",command=f1,width=20)
btn_current.place(x=300,y=120)

btn_Count = Button(mw,text = "Countdown Timer",font=ft,bg="orange",command=f3,width=20)
btn_Count.place(x=300,y=240)

btn_Alarm = Button(mw,text = "Alarm",font=ft,bg="orange",command=f5,width=20)
btn_Alarm.place(x=300,y=360)

cw = Toplevel(mw)
cw.title("Current Time and Date By Rahul")

cw.geometry("600x350+500+200")
cw.configure(bg="yellow")

lbl_Time = Label(cw,text="Current Time:-",font = ft,bg="orange")
lbl_Time.place(x=80,y=20)
lbl_time = Label(cw, font=ft,anchor='center',bg="orange")
lbl_time.place(x=320,y=20)

def t():
    string = strftime('%H:%M:%S %p')
    lbl_time.configure(text=string)
    lbl_time.after(1000, t)

lbl_Date = Label(cw,text="Current Date:-",font=ft,bg="orange")
lbl_Date.place(x=80,y=120)

lbl_date = Label(cw, font=ft,anchor='center',bg="orange")
lbl_date.place(x=320,y=120)
today = date.today()
lbl_date.configure(text=today)

btn_back = Button(cw,text="Back",font=ft,command=f2,bg="light green")
btn_back.place(x=240,y=220)

cw.withdraw()

def on_closing():
	if askokcancel("Quit","Are You Sure?"):
		mw.destroy()

cw.protocol("WM_DELETE_WINDOW", on_closing)
mw.protocol("WM_DELETE_WINDOW", on_closing)

t()


#Countdown

def Start_Timer():
    try:
        hours_val = int(hours.get())
        minutes_val = int(minutes.get())
        seconds_val = int(seconds.get())

        if hours_val >= 24 or minutes_val >= 60 or seconds_val >= 60:
            showerror("Invalid Input", "Hours, minutes, and seconds must be less than 24, 60, and 60, respectively.")
            return

        times = hours_val * 3600 + minutes_val * 60 + seconds_val

        while times > -1:
            minute, second = divmod(times, 60)
            hour, minute = divmod(minute, 60)

            seconds.set(second)
            minutes.set(minute)
            hours.set(hour)

            ct.update()
            time.sleep(1)
            times -= 1
        showinfo("Countdown Timer", "Time is up!")
    except ValueError:
        showerror("Invalid Input", "Please enter valid numeric values for hours, minutes, and seconds.")
    except Exception as e:
        showerror("Error", str(e))

        

hours=StringVar()
minutes=StringVar()
seconds=StringVar()

ct = Toplevel(mw)
ct.title("Countdown Timer By Rahul")
ct.geometry("560x350+500+200")
ct.configure(bg="yellow")

lbl_hr = Label(ct,text="HRS",font=ft,bg="orange")
lbl_hr.place(x=110,y=100)
ent_hr= Entry(ct, width=3, font=ft,textvariable=hours)
ent_hr.place(x=50,y=100)
hours.set("00")

lbl_mt = Label(ct,text="MINS",font=ft,bg="orange")
lbl_mt.place(x=260,y=100)
ent_mt= Entry(ct, width=3, font=ft,textvariable=minutes)
ent_mt.place(x=200,y=100)
minutes.set("00")

lbl_sc = Label(ct,text="SECS",font=ft,bg="orange")
lbl_sc.place(x=430,y=100)
ent_sc= Entry(ct, width=3, font=ft,textvariable=seconds)
ent_sc.place(x=370,y=100)
seconds.set("00")

btn_st = Button(ct,text="start",font=ft,command=Start_Timer,bg="skyblue")
btn_st.place(x=150,y=200)
btn_b = Button(ct,text="back",font=ft,command=f4,bg="light green")
btn_b.place(x=280,y=200)
ct.withdraw()

ct.protocol("WM_DELETE_WINDOW", on_closing)

#Stopwatch

class Stopwatch:
    def __init__(self, parent):
        self.parent = parent
        self.is_running = False
        self.elapsed_time = 0

        self.time_label = Label(parent, font=("Times New Roman", 50), bg="orange", fg="black", text="00:00:00")
        self.time_label.pack(pady=30)

        self.start_button = Button(parent, text="Start", command=self.start_stopwatch,width=30,height=4,bg="Skyblue")
        self.start_button.pack(pady=10)

        self.reset_button = Button(parent, text="Reset", command=self.reset_stopwatch,width=30,height=4,bg="white")
        self.reset_button.pack(pady=10)

        self.stop_button = Button(parent, text="Stop", command=self.stop_stopwatch, width=30, height=4, bg="tomato")
        self.stop_button.pack(pady=10)

    def start_stopwatch(self):
        if not self.is_running:
            self.is_running = True
            self.stop_button.config(state="normal")
            self.update_stopwatch()

    def stop_stopwatch(self):
        self.is_running = False
        self.start_button.config(text="Start")

    def update_stopwatch(self):
        if self.is_running:
            self.elapsed_time += 1
            minutes, seconds = divmod(self.elapsed_time, 60)
            hours, minutes = divmod(minutes, 60)
            time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
            self.time_label.config(text=time_string)
            self.parent.after(1000, self.update_stopwatch)

    def reset_stopwatch(self):
        self.is_running = False
        self.elapsed_time = 0
        self.time_label.config(text="00:00:00")
        self.start_button.config(text="Start")
stopwatch_frame = Toplevel(mw)
stopwatch_frame.geometry("500x500+500+150")
stopwatch_frame.title("Stopwatch By Rahul")
stopwatch = Stopwatch(stopwatch_frame)
stopwatch_frame.configure(bg="yellow")
#button for stopwatch
Bk = Button(stopwatch_frame,text="Back",command=f10,width=30,height=4,bg="light green")
Bk.pack(pady=10)

stopwatch_frame.withdraw()
stopwatch_frame.protocol("WM_DELETE_WINDOW", on_closing)
btn_stopwatch = Button(mw,text = "Stopwatch",font=ft,bg="orange", command=f9,width=20)
btn_stopwatch.place(x=300,y=480)


#Alarm
#Importing all the necessary libraries to form the alarm clock

class Alarm:
    def __init__(self, parent):
        self.parent = parent

        self.alarm_label = Label(parent, font=("Times New Roman", 24,"bold"), bg="orange", fg="black", text="Set the Alarm Time:")
        self.alarm_label.pack(pady=20)

        self.alarm_entry = Entry(parent, font=("Times New Roman", 24))
        self.alarm_entry.pack(pady=20)

        self.set_alarm_button = Button(parent, text="Set Alarm", command=self.set_alarm,width=20,height=2,bg="skyblue")
        self.set_alarm_button.pack(pady=20)

    def set_alarm(self):
        alarm_time = self.alarm_entry.get()
        if self.validate_alarm_time(alarm_time):
            self.alarm_label.config(text=f"Alarm set for: {alarm_time}")
            threading.Thread(target=self.check_alarm, args=(alarm_time,)).start()

    def validate_alarm_time(self, alarm_time):
        try:
            time.strptime(alarm_time, "%H:%M:%S")
            return True
        except ValueError:
            showerror("Invalid Time", "Please enter a valid time in HH:MM:SS format.")
            return False

    def check_alarm(self, alarm_time):
        while True:
            current_time = time.strftime("%H:%M:%S")
            if current_time == alarm_time:
                showinfo("Alarm", "Wake up!")
                break
alarm_frame = Toplevel(mw)
alarm_frame.geometry("500x400+500+200")
alarm_frame.title("Alarm By Rahul")
alarm = Alarm(alarm_frame)
alarm_frame.configure(bg="yellow")
R = Button(alarm_frame,text="Back",command=f6,width=20,height=2,bg="light green")
R.place(x=170,y=240)

alarm_frame.withdraw()
alarm_frame.protocol("WM_DELETE_WINDOW", on_closing)

class WorldClock:
    
    def __init__(self, parent):
        self.parent = parent

        self.city_label = Label(parent, text="Select A City:",bg="orange",font=("Arial",20))
        self.city_label.pack(pady=20)
#radiobuttons 
        self.selected_city = StringVar()
        self.selected_city.set("India")

        self.city_radio1 = Radiobutton(parent, text="India", variable=self.selected_city, value="India",font=20,width=10)
        self.city_radio1.pack(pady=5)

        self.city_radio2 = Radiobutton(parent, text="New York", variable=self.selected_city, value="New York",font=20,width=10)
        self.city_radio2.pack(pady=5)

        self.city_radio3 = Radiobutton(parent, text="Tokyo", variable=self.selected_city, value="Tokyo",font=20,width=10)
        self.city_radio3.pack(pady=5)

        self.city_radio4 = Radiobutton(parent, text="London", variable=self.selected_city, value="London",font=20,width=10)
        self.city_radio4.pack(pady=5)

        self.city_label = Label(parent, text="Current Time In Selected City:",bg="orange",font=("Arial",20))
        self.city_label.pack(pady=20)

        self.time_label = Label(parent, font=("Times New Roman", 50), bg="lightyellow", fg="orange")
        self.time_label.pack(pady=20)

        self.update_time()

    def update_time(self):
        selected_city = self.selected_city.get()
        if selected_city == "India":
            current_time = time.strftime("%H:%M:%S")
        elif selected_city == "New York":
            current_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - 4 * 3600))
        elif selected_city == "Tokyo":
            current_time = time.strftime("%H:%M:%S", time.gmtime(time.time() + 9 * 3600))
        elif selected_city == "London":
            current_time = time.strftime("%H:%M:%S", time.gmtime(time.time() + 1 * 3600))
        else:
            current_time = ""
        self.time_label.config(text=current_time)
        self.time_label.after(1000, self.update_time)
world_clock_frame = Toplevel(mw)
world_clock_frame.geometry("500x560+500+150")
world_clock_frame.configure(bg="yellow")
world_clock_frame.title("World Clock By Rahul")
world_clock = WorldClock(world_clock_frame)
Bak = Button(world_clock_frame,text="Back",font="Arial",command=f8,width=20,height=2,bg="light green")
Bak.pack(pady=20)

world_clock_frame.withdraw()
world_clock_frame.protocol("WM_DELETE_WINDOW", on_closing)

btn_WC = Button(mw,text = "World Clock",font=ft,bg="orange",command=f7,width=20)
btn_WC.place(x=300,y=600)
#label at the bottom
lbl_r = Label(text = "By Rahul ",font=("Times New Roman",20,"bold","italic"),bg="yellow")
lbl_r.place(x=850,y=680)


mw.mainloop()
