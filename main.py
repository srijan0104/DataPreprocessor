import PySimpleGUI as sg
import tkinter as tk
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
from tkinter import *
from PIL import Image, ImageTk
import csv
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.preprocessing import LabelEncoder

root = tk.Tk()
root.wm_geometry('1600x900')
root.title('DataAnalyser')

'''global count1
global sliderwords
#def labelslider():

    #global count1
    #global sliderwords
    #text = 'Enter the file path'

    #if count1 >= len(text):
        #count = 0
        #sliderwords = ''
    sliderwords += text[count1]
    count1 += 1
    fontlabel.configure(text=sliderwords)
    fontlabel.after(120, labelslider)'''


def import_csv_data():
    global v
    global csv_file_path
    global header_list
    global data
    global fn

    csv_file_path = askopenfilename()
    print(csv_file_path)
    v.set(csv_file_path)
    global df
    df = pd.read_csv(csv_file_path)
    df = df.fillna(0)
    # print(df.head())
    header_list = list(df.columns)
    data = df[1:].values.tolist()
    fn = csv_file_path.split('/')[-1]


# def show_table(data, header_list, fn):
# layout = [
# [sg.Table(values=data,
# headings=header_list,
# font='Helvetica',
# pad=(25,25),
# display_row_numbers=False,
# auto_size_columns=True,
# num_rows=min(25, len(data)))]
# ]

# window = sg.Window(fn, layout, grab_anywhere=False)
# event, values = window.read()
# window.close()

def DEnc(column):
    column.title("To Label Encode the column  :")
    #     for widgets in frame.winfo_children():
    #         widgets.destroy()
    a = df.select_dtypes(exclude=np.number).columns.tolist()
    pos = 4
    for x in a:
        sd = Button(column, text=x, bg="#6dc2f7", command=lambda x=x: encoding(x)).pack()
        pos += 4


def DEnc1(column):
    column.title("To Label Encode the column  :")
    #     for widgets in frame.winfo_children():
    #         widgets.destroy()
    a = df.select_dtypes(exclude=np.number).columns.tolist()
    pos = 4
    for x in a:
        sd = Button(column, text=x, bg="#6dc2f7", command=lambda x=x: encoding1(x)).pack()
        pos += 4


def OutL(column):
    column.title("To remove the outliers of the column :")
    #     for widgets in frame.winfo_children():
    #         widgets.destroy()
    a = df.select_dtypes(include=np.number).columns.tolist()
    pos = 4
    for x in a[3:]:
        sd = Button(column, text=x, bg="#6dc2f7", command=lambda x=x: outliers(x)).pack()
        pos += 4


def Impute(column):
    column.title("Impute the column :")
    #     for widgets in frame.winfo_children():
    #         widgets.destroy()
    a = df.select_dtypes(include=np.number).columns.tolist()
    pos = 4
    for x in a[3:]:
        sd = Button(column, text=x, bg="#6dc2f7", command=lambda x=x: Imputation(x)).pack()
        pos += 4


# def CMean(column):
# x = df[column]
#     print(x)
# mean = x.mean()
# resultLabel.config(text="The Mean of the " + column + " is: " + str(mean))


# def CMedian(column):
# x = df[column]
# median = x.median()
# resultLabel.config(text="The Median of the " + column + " is: " + str(median))

# def cEncoding(column):
# pd.concat([df, pd.get_dummies(df[column])], axis=1).head()


def Imputation(column):
    mean = df[column].mean()
    df[column] = df.column.fillna(mean, inplace=True)

    # Add new data in Treeview widget
    tree["column"] = list(df.columns)
    tree["show"] = "headings"

    tree.column("#0", width=120)

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)

    # Put Data in Rows
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)
    sb = Scrollbar(frame, orient=HORIZONTAL)
    sb.pack(side=BOTTOM, fill=X)

    tree.config(xscrollcommand=sb.set)
    sb.config(command=tree.xview)
    tree.pack()


def encoding(column):
    df_desc1 = pd.concat([df, pd.get_dummies(df[column])], axis=1).head()

    # Add new data in Treeview widget
    tree["column"] = list(df_desc1.columns)
    tree["show"] = "headings"

    tree.column("#0", width=120)

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)

    # Put Data in Rows
    df_rows = df_desc1.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)
    sb = Scrollbar(frame, orient=HORIZONTAL)
    sb.pack(side=BOTTOM, fill=X)

    tree.config(xscrollcommand=sb.set)
    sb.config(command=tree.xview)
    tree.pack()


def encoding1(column):
    clear_treeview()
    le = LabelEncoder()
    le.fit(df[column])
    df['le_class'] = le.transform(df[column])

    df_desc2 = df

    # Add new data in Treeview widget
    tree["column"] = list(df_desc2.columns)
    tree["show"] = "headings"

    tree.column("#0", width=120)

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)

    # Put Data in Rows
    df_rows = df_desc2.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)
    sb = Scrollbar(frame, orient=HORIZONTAL)
    sb.pack(side=BOTTOM, fill=X)

    tree.config(xscrollcommand=sb.set)
    sb.config(command=tree.xview)
    tree.pack()


def outliers(column):
    clear_treeview()
    IQR = df[column].quantile(0.75) - df[column].quantile(0.25)
    lower_limit = df[column].quantile(0.25) - (IQR * 1.5)
    upper_limit = df[column].quantile(0.75) - (IQR * 1.5)
    out = np.where(df[column] > upper_limit, True, np.where(df[column] < lower_limit, True, False))
    df_out = df.loc[~(out),]

    df_desc2 = df_out

    # Add new data in Treeview widget
    tree["column"] = list(df_desc2.columns)
    tree["show"] = "headings"

    tree.column("#0", width=120)

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)

    # Put Data in Rows
    df_rows = df_desc2.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)
    sb = Scrollbar(frame, orient=HORIZONTAL)
    sb.pack(side=BOTTOM, fill=X)

    tree.config(xscrollcommand=sb.set)
    sb.config(command=tree.xview)
    tree.pack()


'''def mv1(column):
    clear_treeview()

    df_desc3 = df.isnull().mean()

    # Add new data in Treeview widget
    tree["column"] = list(df_desc3.columns)
    tree["show"] = "headings"

    tree.column("#0", width=120)

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)

    # Put Data in Rows
    df_rows = df_desc2.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)
    sb = Scrollbar(frame, orient=HORIZONTAL)
    sb.pack(side=BOTTOM, fill=X)

    tree.config(xscrollcommand=sb.set)
    sb.config(command=tree.xview)
    tree.pack()'''


def plot(parent):
    parent.title("Plotting the histogram of :")
    a = df.select_dtypes(include=np.number).columns.tolist()
    pos = 4
    for x in a[:10]:
        sd = Button(parent, text=x, bg="orange", command=lambda x=x: showPlot(x, parent)).pack()
        pos += 2


def plot2(parent):
    parent.title("Plotting the Box plot of :")
    a = df.select_dtypes(include=np.number).columns.tolist()
    pos = 4
    for x in a[:10]:
        sd = Button(parent, text=x, bg="orange", command=lambda x=x: showBoxPlot(x, parent)).pack()
        pos += 2


def plot3(parent):
    parent.title("Plotting the Bar plot of :")
    a = df.select_dtypes(include=np.number).columns.tolist()
    pos = 4
    for x in a[:10]:
        sd = Button(parent, text=x, bg="orange", command=lambda x=x: showBarPlot(x, parent)).pack()
        pos += 2


def showPlot(column, parent):
    resultLabel = Label(parent, text="Result: -", font=(None, 15))
    resultLabel.place(x=120, y=250)
    resultLabel.config(text="The Plot of " + column + " is shown below: ")
    x = df[column]
    fig = Figure(figsize=(5, 5), dpi=100)

    plot1 = fig.add_subplot(111)
    plot1.hist(x)

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, parent)
    canvas.draw()

    # placing the canvas on the Tkinter window
    #     canvas.get_tk_widget().place(x = 100, y = 0)

    canvas.get_tk_widget().place(x=100, y=280)


def showBoxPlot(column, parent):
    resultLabel = Label(parent, text="Result: -", font=(None, 15))
    resultLabel.place(x=120, y=250)
    resultLabel.config(text="The Plot of " + column + " is shown below: ")
    x = df[column]
    fig = Figure(figsize=(5, 5), dpi=100)

    plot1 = fig.add_subplot(111)
    plot1.boxplot(x)

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, parent)
    canvas.draw()

    # placing the canvas on the Tkinter window
    #     canvas.get_tk_widget().place(x = 100, y = 0)

    canvas.get_tk_widget().place(x=100, y=280)


def showBarPlot(column, parent):
    resultLabel = Label(parent, text="Result: -", font=(None, 15))
    resultLabel.place(x=120, y=250)
    resultLabel.config(text="The Plot of " + column + " is shown below: ")
    x = df[column]
    fig = Figure(figsize=(5, 5), dpi=100)

    plot1 = fig.add_subplot(111)
    plot1.plot(x)

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, parent)
    canvas.draw()

    # placing the canvas on the Tkinter window
    #     canvas.get_tk_widget().place(x = 100, y = 0)

    canvas.get_tk_widget().place(x=100, y=280)


def create_window():
    newwindow = tk.Toplevel(root)
    newwindow.geometry("700x750")
    return newwindow


def clear():
    pass


def show():
    #     filename = filedialog.askopenfilename(title = "Open a File", filetype=(("csv files", ".*csv"),("All Files", "*.")))
    #     if csv_file_path:
    #         try:
    #             csv_file_path = r"{}".format(csv_file_path)
    #             df = pd.read_csv(csv_file_path)
    #         except ValueError:
    #             label.config(text = "File could not be opened")
    #         except FileNotFoundError:
    #             label.config(text = "File Not Found")

    # Clear all the previous data in tree

    clear_treeview()
    df_desc = df.describe()
    vsb = ttk.Scrollbar(orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=vsb.set)

    # Add new data in Treeview widget
    tree["column"] = list(df_desc.columns)
    tree["show"] = "headings"

    tree.column("#0", width=120)

    # For Headings iterate over the columns
    for col in tree["column"]:
        tree.heading(col, text=col)

    # Put Data in Rows
    df_rows = df_desc.to_numpy().tolist()
    for row in df_rows:
        tree.insert("", "end", values=row)
    sb = Scrollbar(frame, orient=HORIZONTAL)
    sb.pack(side=BOTTOM, fill=X)

    tree.config(xscrollcommand=sb.set)
    sb.config(command=tree.xview)
    tree.pack()


# Clear the Treeview Widget
def clear_treeview():
    tree.delete(*tree.get_children())


# root.configure(bg='#00ffff')
load = Image.open(
    r'C:\Users\DELL\PycharmProjects\pythonProject3\big-data-analysis.jpg')  # Opens and identifies the given image file.
render = ImageTk.PhotoImage(load)  # It will bring the image given in load .
img = Label(root, image=render)
img.place(x=0, y=0)

# Create an object of Style widget
style = ttk.Style()
style.theme_use('clam')

# Create a Frame
frame = Frame(root)
frame.pack(pady=20, side=BOTTOM)

# Create a Treeview widget
tree = ttk.Treeview(frame)

# fontlabel = Label(root, text='', font=('Arial Black', 25, 'bold'), bg='SkyBlue1', fg='black', width=31,justify='center')
# fontlabel.place(x=31, y=110)
# labelslider()
tk.Label(root, text='Enter the file path', font=('Arial', 25), bg="yellow").pack()
# tk.Label(root, text='Enter the file path', font=('Arial', 25)).pack()
v = tk.StringVar()
entry = tk.Entry(root, textvariable=v).place(x=710, y=120)

tk.Button(root, text='Load the Data Set', command=import_csv_data, bg="yellow").place(x=720, y=145)

# show_prompt = sg.popup_yes_no('Show the dataset?')
# if show_prompt=='Yes':
# show_table(data, header_list, fn)


encBtn = Button(root, text="OneHotEncoding", command=lambda: DEnc(create_window()), bg="gold", width="20",
                height="2").place(x=50, y=300)
encBtn2 = Button(root, text="LabelEncoding", command=lambda: DEnc1(create_window()), bg="yellow", width="20",
                 height="2").place(x=300, y=300)
Oh = Button(root, text="HandleOutliers", command=lambda: OutL(create_window()), bg="yellow", width="20",
            height="2").place(x=1050, y=300)

# medianBtn = Button(root, text="Calc.Median", command=lambda: DMedian(create_window()), bg="#F5F5F5", width="20", height="2").place(x=450, y=300)

# resultLabel = Label(root, text="--Result--", font=(None, 15))
# resultLabel.place(x=725, y=200)

plotBtn = Button(root, text="Histogram", command=lambda: plot(create_window()), bg="orange", width="10", height="2")
plotBtn.place(x=730, y=350)

plotBtn2 = Button(root, text="Box plot", command=lambda: plot2(create_window()), bg="orange", width="10", height="2")
plotBtn2.place(x=730, y=400)

plotBtn3 = Button(root, text="Line plot", command=lambda: plot3(create_window()), bg="orange", width="10", height="2")
plotBtn3.place(x=730, y=450)

Impute1 = Button(root, text="IMPUTE", command=lambda: Impute(create_window()), bg="gold", width="10", height="2")
Impute1.place(x=1350, y=300)

showBtn = Button(root, text="DESCRIBE", command=show, width="10", height="2", bg="medium violet red", fg="white").place(
    x=730, y=250)
#Mv = Button(root, text="Check MissingValues", command=show, width="15", height="2", bg="medium violet red",
            #fg="white").place(x=730, y=250)
# encBtn = Button(root, text="Encode", command=encoding, width="10", height="2", bg="brown", fg="white").place(x=800, y=400)
# encBtn = Button(root, text="Encoding", command=encoding, bg="blue", fg="white", width="10", height="2")
# encBtn.place(x=1200, y=100)

# tk.Button(root, text='Quit', command=root.destroy, bg="red", width="10", height="2").place(x=1460, y=0)

# Add a Label widget to display the file content
# label = Label(root, text = '')
# label.pack(pady = 20)

root.mainloop()
#-*- coding: utf-8 -*-
