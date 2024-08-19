from tkinter import messagebox, simpledialog
import tkinter
import time

windows = tkinter.Tk()
windows.title('刷课脚本')

width = 400
height = 200
screenwidth = windows.winfo_screenwidth()
screenheight = windows.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
windows.geometry(alignstr)

clicked = False  # 添加一个全局变量，用于跟踪按钮是否已被点击

def gettime():
    timestr = time.strftime("%H:%M:%S")
    lb.configure(text=timestr)
    windows.after(1000, gettime)

def sy_str():
    global clicked  # 在函数内部声明全局变量
    if not clicked:  # 如果按钮还未被点击
        ask = simpledialog.askstring("请选择要刷的课程:", "请输入数字", initialvalue="1")
        tkinter.messagebox.showinfo("消息对话框", "成功! ！正在运行！")
        clicked = True  # 设置点击状态为True
        print(ask)
    else:
        tkinter.messagebox.showinfo("消息对话框", "已运行过，请等待！")


def show():
    global clicked  # 在函数内部声明全局变量
    if not clicked:  # 如果按钮还未被点击
        tkinter.messagebox.showinfo("消息对话框", "点击运行！")
        clicked = True  # 设置点击状态为True
        print(1)
    else:
        tkinter.messagebox.showinfo("消息对话框", "正在运行，请等待！")


button = tkinter.Button(windows, text="超星刷课", command=show)
button.pack(pady=10)

lb = tkinter.Label(windows, text='', fg='blue', font=("黑体", 45))
lb.pack(padx=10)

gettime()
windows.mainloop()