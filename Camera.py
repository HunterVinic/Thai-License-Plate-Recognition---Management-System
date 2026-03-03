import datetime
import tkinter as tk
from tkinter import messagebox


class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("License Management System")
        self.root.geometry("1540x800+0+0")

        lbltitle = tk.Label(self.root, bd=20, relief=tk.RIDGE, text="License Management System", fg="red", bg="white",
                            font=("times new roman", 50, "bold"))
        lbltitle.pack(side=tk.TOP, fill=tk.X)

        Dataframe = tk.Frame(self.root, bd=20, relief=tk.RIDGE)
        Dataframe.place(x=0, y=130, width=1530, height=400)

        DataframeLeft = tk.LabelFrame(Dataframe, bd=10, padx=20, relief=tk.RIDGE,
                                      font=("arial", 12, "bold"), text="Driver Information")
        DataframeLeft.place(x=0, y=5, width=980, height=350)

        DataframeRight = tk.LabelFrame(Dataframe, bd=10, padx=20, relief=tk.RIDGE,
                                       font=("arial", 12, "bold"), text="")
        DataframeRight.place(x=990, y=5, width=980, height=350)

        Buttonframe = tk.Frame(self.root, bd=20, relief=tk.RIDGE)
        Buttonframe.place(x=0, y=530, width=1530, height=70)

        Detailsframe = tk.Frame(self.root, bd=20, relief=tk.RIDGE)
        Detailsframe.place(x=0, y=600, width=1530, height=190)

        lblNameTablet=tk.Label(DataframeLeft,text="Names of Tablet",font=("times New Roman",12,"bold"),padx=2, pady=6)
        lblNameTablet.grid(row=0,column=0)

        comNametablet=tk.Combobox(DataframeLeft,font=("times new roman"))
        comNametablet["value"]=("SUV", "Minivan", "Hatchback", "Station Wagon", "Sedan", "Crossover", "Van", "Sports Car", "Coupe", "Convertable", "Pickup truck", "Compact", "Motorcycle", "Bus", "Ambulance", "Truck", "Taxi")
        comNametablet.grid(row=0,column=0)

root = tk.Tk()
ob = Hospital(root)
root.mainloop()
