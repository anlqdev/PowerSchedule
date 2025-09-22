import tkinter as tk
import tkinter.messagebox
import subprocess

root = tk.Tk()
root.title("PowerSchedule v1.0")
root.resizable(False, False)
try:
    root.iconbitmap("PowerSchedule-icon.ico")
except:
    pass

time = tk.Label(root,text="Time: ")
time.grid(row=0,column=0)

hr_spin = tk.Spinbox(from_=0,to=87599,width=5)
hr_spin.grid(row=0,column=1)
hr_t = tk.Label(root,text="h")
hr_t.grid(row=0,column=2)

m_spin = tk.Spinbox(from_=0,to=60,width=5)
m_spin.grid(row=0,column=3)
m_t = tk.Label(root,text="m")
m_t.grid(row=0,column=4)

s_spin = tk.Spinbox(from_=0,to=60,width=5)
s_spin.grid(row=0,column=5)
s_t = tk.Label(root,text="s")
s_t.grid(row=0,column=6)

action = tk.StringVar()
action.set("-s")

act_t = tk.Label(root,text="Action:")
act_t.grid(row=1,column=0)

rb1 = tk.Radiobutton(root, text="Shut down", variable=action, value="-s")
rb1.grid(row=1,column=1)

rb2 = tk.Radiobutton(root, text="Restart", variable=action, value="-r")
rb2.grid(row=2,column=1)

def start():
    time = (int(hr_spin.get()) * 3600) + (int(m_spin.get()) * 60) + int(s_spin.get())
    if time >= 315360000:
        tkinter.messagebox.showinfo(title="Error (87): Time limit exceeded", message="Please re-enter the time to start. The required time is no more than 315360000 seconds (equivalent to 10 years)")
    else:
        result1 = subprocess.run("shutdown " + action.get() + " -t " + str(time), shell=True, capture_output=True, text=True)
        if "A system shutdown has already been scheduled.(1190)" in result1.stderr:
            tkinter.messagebox.showinfo(title="Error (1190): Number of scheduled times exceeded limit", message="Please cancel your previous schedule to start. You can only run 1 schedule at a time.")
        else:
            tkinter.messagebox.showinfo(title="Schedule started!", message="The schedule you're set on your computer started!")
            
def stop():
    result = subprocess.run("shutdown -a", shell=True, capture_output=True, text=True)
    if "Unable to abort the system shutdown because no shutdown was in progress.(1116)" in result.stderr:
        tkinter.messagebox.showinfo(title="Error (1116): No schedule set yet", message="There are currently no running schedule on your computer!")
    else:
        tkinter.messagebox.showinfo(title="Schedule cancelled!", message="The schedule you're set on your computer has been cancelled!")
    
start_bt = tk.Button(root, text="Start", command=start)
start_bt.grid(row=2, column=4)

can_bt = tk.Button(root, text="Cancel", command=stop)
can_bt.grid(row=2, column=3)


root.mainloop()
