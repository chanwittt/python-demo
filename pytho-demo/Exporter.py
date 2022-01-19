import tkinter as tk
import numpy as np
import pandas as pd
from tkinter import PhotoImage, filedialog, messagebox, ttk
from ttkthemes import ThemedTk


# initalise the tkinter GUI
root = ThemedTk(theme="radiance")
root.iconphoto(False, tk.PhotoImage(file='images/logo2.png'))
# tells the root to not let the widgets inside it determine its size.
root.pack_propagate(False)
root.resizable(0, 0)  # makes the root window fixed in size.
root.title("Exporter")

#set geometry
window_width = 1024
window_height = 768

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Frame for TreeView
frame1 = tk.LabelFrame(root, text="Excel Data")
frame1.place(height=600, width=1024)

# Frame for open file dialog
file_frame = tk.LabelFrame(root, text="Open File",)
file_frame.place(height=100, width=600, rely=0.8, relx=0.01)

# Buttons
browse_btn_img = PhotoImage(file='images/button_browse.png')
browse_btn = tk.Button(file_frame, image=browse_btn_img, borderwidth=0, width=80, height=30, text="Browse",
                    command=lambda: File_dialog())
browse_btn.place(rely=0.4, relx=0.05)

save_btn_img = PhotoImage(file='images/button_save.png')
save_btn = tk.Button(file_frame, image=save_btn_img, borderwidth=0,
                    width=80, height=30, text="Export", command=lambda: save_file())
save_btn.place(rely=0.4, relx=0.40)

# The file/file path text
label_file = ttk.Label(file_frame, text="No File Selected")
label_file.place(rely=0, relx=0)


dst_file = ttk.Label(file_frame, text="Destination")
dst_file.place(rely=0, relx=0.4)
dst_file = ttk.Label(file_frame, text=" ")
dst_file.place(rely=0, relx=0.55)


# Treeview Widget
tv1 = ttk.Treeview(frame1)
# set the height and width of the widget to 100% of its container (frame1).
tv1.place(relheight=1, relwidth=1)

# command means update the yaxis view of the widget
treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)
# command means update the xaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)
# assign the scrollbars to the Treeview Widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
# make the scrollbar fill the x axis of the Treeview widget
treescrollx.pack(side="bottom", fill="x")
# make the scrollbar fill the y axis of the Treeview widget
treescrolly.pack(side="right", fill="y")


def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xls files", "*.xls"), ("All Files", "*.*")))
    label_file["text"] = filename
    Load_excel_data()
    return None


def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""
    global df
    file_path = label_file["text"]
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv((excel_filename), skiprows=1, converters={
                             'empNo': str, 'eventTime': pd.to_datetime})
        else:
            df = pd.read_excel((excel_filename), skiprows=1, converters={
                               'empNo': str, 'eventTime': pd.to_datetime})

        #drop row which empNo is null
        df = df[df['empNo'].notna()]                         

    except ValueError:
        tk.messagebox.showerror(
            "Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        # let the column heading = column name
        tv1.heading(column, text=column)

    df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        tv1.insert("", "end", values=row)
        # print(df)

    return None


def clear_data():
    tv1.delete(*tv1.get_children())
    return None

def fixed_width(dst):
    f = open(dst, "r")
    data = f.read()
    # max-width per column, column == key, width == value
    w = {}
    lines = data.splitlines()
    for line in lines:
        for col_nr, col in enumerate(line.strip().split(",")):
            w[col_nr] = max( w.get(col_nr,0), len(col))

    # write file
    with open(dst,"w") as ff:
        for line in lines:
            for col_nr, col in enumerate(line.strip().split(",")):
                # the :<{w[col_nr]+5}} - part is left-adjusting to certain width 
                #f.write(f"{col:<{w[col_nr]+5}}") # 5 additional spaces
                if col_nr == 0:
                    ff.write(f"{col:<{'16'}}")
                else:
                    ff.write(f"{col:<{'14'}}")
            ff.write("\n")

    return None


def save_file():
    src = label_file["text"]
    if src == "No File Selected" or src == "":
        return tk.messagebox.showwarning(title="Exporter", message='Please browse file first!')
    else:
        dst = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if dst is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        # set dst_file label to dst path
        dst_file["text"] = dst.name
        # concat datafram from first and last of day
        result = df_concat()
        try:
            #save dataframe to txt
            np.savetxt(dst.name, result, delimiter=',', fmt="%s")
            #fixed length charecter
            fixed_width(dst.name)
            tk.messagebox.showinfo(title="Exporter", message='Successfully')


        except Exception as e:
            tk.messagebox.showwarning(title="Exporter", message=e)


def df_concat():

    # find first log of day
    first_scan = first_of_day()
    # find last log of day
    last_scan = last_of_day()

    res_concat = pd.concat([first_scan, last_scan])
    res_concat = res_concat.sort_values(by=['new_date'])

    remove_newdatetime = ['empNo', 'eventTime']
    res = res_concat[remove_newdatetime]

    return res


def first_of_day():
    df1 = df
    df1['new_date'] = [d.date() for d in df1['eventTime']]
    df1['new_time'] = [d.time() for d in df1['eventTime']]

    first_scan = df1.drop_duplicates(
        subset=['empNo', 'new_date'], keep="first")
    new_column = ['empNo', 'eventTime', 'new_date', 'new_time']
    first_scan = first_scan[new_column]
    first_scan['eventTime'] = first_scan['eventTime'].dt.strftime(
        '% Y % m % d % r')
    first_scan['eventTime'] = first_scan['eventTime'].str.replace(r'\D', '')
    return first_scan


def last_of_day():
    df2 = df
    df2['new_date'] = [d.date() for d in df2['eventTime']]
    df2['new_time'] = [d.time() for d in df2['eventTime']]

    last_scan = df2.drop_duplicates(subset=['empNo', 'new_date'], keep="last")
    new_column = ['empNo', 'eventTime', 'new_date', 'new_time']
    last_scan = last_scan[new_column]
    last_scan['eventTime'] = last_scan['eventTime'].dt.strftime(
        '% Y % m % d % r')
    last_scan['eventTime'] = last_scan['eventTime'].str.replace(r'\D', '')
    return last_scan


root.mainloop()
