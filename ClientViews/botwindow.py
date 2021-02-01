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

        self.frame_first = tk.LabelFrame(self.master, text="", padx=282, pady=20, font=("bold", 20))
        self.frame_first.grid(row=0, columnspan=2)
        self.topLabel = tk.Label(self.frame_first, text="Vera&John BOTへようこそ！", font=("bold", 17))
        self.topLabel.grid()

        # left frame
        self.frame_left = tk.LabelFrame(self.master, text="", padx=0, pady=0, font=("bold", 20))
        self.frame_left.grid(row=1, column=0)
        # frame for "monitor" text on top of left frame
        self.frame_left_header = tk.LabelFrame(self.frame_left, text="", font=("bold", 14), height=200, width=400)
        self.frame_left_header.grid()
        # monitor text inside subframe of left frame
        self.monitoringLabel = tk.Label(self.frame_left_header, text="モニタリング", font=("bold", 16), padx=150)
        self.monitoringLabel.grid()
        # dummy activity frame
        self.verajohnlogin = tk.LabelFrame(self.frame_left_header, text="", font=("bold", 20), height=385, width=430)
        self.verajohnlogin.grid()

        # veraJohn user id label and field
        self.veraJohnID = tk.Label(self.verajohnlogin, text="UserId", font=("bold", 12), padx=150, pady = 10)
        self.veraJohnID.grid()
        self.VeraJohnIDField = tk.Entry(self.verajohnlogin)
        self.VeraJohnIDField.grid()

        # veraJohn pass label and field
        self.veraJohnpass = tk.Label(self.verajohnlogin, text="Password", font=("bold", 12), padx=150, pady = 10)
        self.veraJohnpass.grid()
        self.VeraJohnpassField = tk.Entry(self.verajohnlogin)
        self.VeraJohnpassField.grid()

        # empty lable
        self.empty1 = tk.Label(self.verajohnlogin, text="", font=("bold", 16), padx=150, pady=5)
        self.empty1.grid()


        # VeraJohn Authentication button
        self.authButton = tk.Button(self.verajohnlogin, text ="Submit", padx = 25, command = self.VeraJohnAuth())
        self.authButton.grid()

        # empty lable
        self.empty2 = tk.Label(self.verajohnlogin, text="", font=("bold", 16), padx=150, pady=5)
        self.empty2.grid()

        verajohnlogin = tk.LabelFrame(self.verajohnlogin, text="", font=("bold", 20), height=85, width=430).grid()

        # e2 = tk.Entry(master)
        #
        #
        # e2.grid(row=1, column=1)

        # right frame
        self.frame_right = tk.LabelFrame(self.master, text="", padx=0, pady=0, font=("bold", 20))
        self.frame_right.grid(row=1, column=1)
        # frame for "monitor" text on top of right frame
        self.frame_right_header = tk.LabelFrame(self.frame_right, text="", font=("bold", 14), height=200, width=400)
        self.frame_right_header.grid(row=2, column=1)
        # username text inside subframe of left frame
        nameLabel = tk.Label(self.frame_right_header, text="名前表示", font=("bold", 14), padx=120).grid()

        # email text inside subframe of left frame
        mailLabel = tk.Label(self.frame_right_header, text="メールアドレス表示", font=("bold", 14), padx=120).grid()

        # bet activation frame
        betOnOff = tk.LabelFrame(self.frame_right_header, text="", font=("bold", 20), height=60, width=430).grid()

        # Bet lable Label
        betLable = tk.Label(betOnOff, text="uysdgfuyse", font=("bold", 20), padx=20, pady=20)
        betLable.grid(row=1, column=2)

    def VeraJohnAuth(self):
        print("done")
        userid = self.VeraJohnIDField.get()
        userpassword = self.VeraJohnpassField.get()
        svlogin.StaticVars.verajohnUserId = userid
        svlogin.StaticVars.verajohnUserPass = userpassword
        self.goToVeraJohn()

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

    def goToVeraJohn(self):
        print(svlogin.StaticVars.verajohnUserId + "this")
        while True:
            # break
            print("not yet")
            if svlogin.StaticVars.verajohnUserId != 'unique user id' and svlogin.StaticVars.verajohnUserPass != 'Secure':
                bot = bt.BotInitiation()
                result = bot.start()
                while result is False or True:
                    print("master returned")
                    result = bot.start()



def create():
    root = tk.Tk()
    app = BotBegin(master=root)
    app.mainloop()


