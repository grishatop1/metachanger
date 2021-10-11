import os
import datetime
import time

from tkinter import *
from tkinter.ttk import *
from tkcalendar import Calendar
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

import pywintypes, win32file, win32con

class MainApplication(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("Metadata Changer v1.0")
        self.resizable(0,0)

        self.file_frame = FileSelector(self)
        self.separator1 = Separator(self, orient="horizontal")
        self.change_frame = ChangeFrame(self)

        self.file_frame.grid(row=0, column=0)
        self.separator1.grid(row=1, column=0, sticky="ew")
        self.change_frame.grid(row=2, column=0)

class FileSelector(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.path_entry = Entry(self, width=40, state="disabled")
        self.select_btn = Button(self, text="Select file...", command=self.openFile)

        self.path_entry.grid(row=0, column=0)
        self.select_btn.grid(row=0, column=1)

    def openFile(self):
        self.filepath = askopenfilename()
        if not self.filepath: return

        self.path_entry["state"] = "normal"
        self.path_entry.insert(0, self.filepath)
        self.path_entry["state"] = "disabled"

        self.parent.change_frame.setFile(self.filepath)

class ChangeFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.currentfile_label = Label(self, text="Current file: Not selected!")
        self.open_btn = Button(self, text="Pick a date...", state="disabled", command=self.openPick)

        self.currentfile_label.grid(row=0, column=0)
        self.open_btn.grid(row=2, column=0)

    def setFile(self, filepath):
        filename = os.path.basename(filepath)
        self.currentfile_label["text"] = f"Current file: {filename}"
        self.open_btn["state"] = "normal"

    def openPick(self):
        chs_date = ChooseDate(self.parent)
        chs_date.mainloop()

class ChooseDate(Toplevel):
    def __init__(self, parent, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.title("Pick a date...")
        self.resizable(0,0)
        self.grab_set()

        self.cal = Calendar(self, selectmode = 'day',
               year = 2021, month = 1,
               day = 7)
        self.apply_btn = Button(self, text="Select!", command=self.select)

        self.cal.pack()
        self.apply_btn.pack()

    def select(self):
        month, day, year = self.cal.get_date().split("/")
        year = "20" + year
        epoch = datetime.datetime(int(year), int(month), int(day), 15, 27, 1).timestamp()
        changeFileCreationTime(self.parent.file_frame.filepath, epoch)
        os.utime(self.parent.file_frame.filepath, (epoch, epoch))
        showinfo("Success", "The date successfully has been changed!")
        self.destroy()

def changeFileCreationTime(fname, newtime):
    wintime = pywintypes.Time(newtime)
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    win32file.SetFileTime(winfile, wintime, None, None)

    winfile.close()


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()