from ClientViews.GuiWidgets.Widget import *


import tkinter as tk
import ClientViews.StaticVars as svlogin
import ClientViews.BotClasses.botinitiation as bt
class BotBegin(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # set title of window
        self.master.title("VeraJohnBot")

        # set dimension of window
        self.master.geometry("900x500")

        frame_first = tk.LabelFrame(self.master, text="", padx=282, pady=20, font=("bold", 20))
        frame_first.grid(row=0, columnspan=2)
        topLabel = tk.Label(frame_first, text="Vera&John BOTへようこそ！", font=("bold", 17))
        topLabel.grid()

        # left frame
        frame_left = tk.LabelFrame(self.master, text="", padx=0, pady=0, font=("bold", 20))
        frame_left.grid(row=1, column=0)
        # frame for "monitor" text on top of left frame
        frame_left_header = tk.LabelFrame(frame_left, text="", font=("bold", 14), height=200, width=400)
        frame_left_header.grid()
        # monitor text inside subframe of left frame
        monitoringLabel = tk.Label(frame_left_header, text="モニタリング", font=("bold", 16), padx=150)
        monitoringLabel.grid()
        # dummy activity frame
        verajohnlogin = tk.LabelFrame(frame_left_header, text="", font=("bold", 20), height=385, width=430).grid()



        # right frame
        frame_right = tk.LabelFrame(self.master, text="", padx=0, pady=0, font=("bold", 20))
        frame_right.grid(row=1, column=1)
        # frame for "monitor" text on top of right frame
        frame_right_header = tk.LabelFrame(frame_right, text="", font=("bold", 14), height=200, width=400)
        frame_right_header.grid(row=2, column=1)
        # username text inside subframe of left frame
        nameLabel = tk.Label(frame_right_header, text="名前表示", font=("bold", 14), padx=120).grid()

        # email text inside subframe of left frame
        mailLabel = tk.Label(frame_right_header, text="メールアドレス表示", font=("bold", 14), padx=120).grid()

        # bet activation frame
        betOnOff = tk.LabelFrame(frame_right_header, text="", font=("bold", 20), height=60, width=430).grid()

        # Bet lable Label
        betLable = tk.Label(betOnOff, text="uysdgfuyse", font=("bold", 20), padx=20, pady=20)
        betLable.grid(row=1, column=2)



    # Entry field label
    def create_label_appname(self):
        self.systemUserId = tk.Label()
        self.systemUserId["text"] = "Vera&JohnBot"
        self.systemUserId["font"] = ("bold", 13)
        self.systemUserId["pady"] = 10
        self.systemUserId["border"] = 2
        self.systemUserId.pack()


    def localAuthentication(self):
        userid = self.systemUserIdInput.get()
        userpassword = self.systemUserPassInput.get()
        svlogin.StaticVars.userId = userid
        svlogin.StaticVars.userPass = userpassword
        self.master.destroy()



def create():
    root = tk.Tk()
    app = BotBegin(master=root)
    app.after(2000, goToVeraJohn)
    app.mainloop()

def goToVeraJohn():
    bot = bt.BotInitiation()
    bot.start()
