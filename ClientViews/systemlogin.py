from ClientViews.GuiWidgets.Widget import *
import tkinter as tk
import requests as rq
import ClientViews.StaticVars as svlogin
class SystemLogin(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # set title of window
        self.master.title("VeraJohnBot")

        # set dimension of window
        self.master.geometry("900x550")


        self.create_empty_first()

        self.create_label_systemUserId()

        self.create_entry_userid()

        self.create_label_systemUserPass()

        self.create_entry_userpass()

        self.create_empty_second()

        self.create_button()

    # empty widget create method
    def create_empty_first(self):
        self.firstEmpty = tk.Label()
        self.firstEmpty["text"] = ""
        self.firstEmpty["pady"] = 10
        self.firstEmpty.pack()



    # Entry field label
    def create_label_systemUserId(self):
        self.systemUserId = tk.Label()
        self.systemUserId["text"] = "User ID"
        self.systemUserId["font"] = ("bold", 10)
        self.systemUserId["pady"] = 10
        self.systemUserId.pack()



    # Input fields
    def create_entry_userid(self):
        self.entryFieldValue = tk.StringVar()
        self.systemUserIdInput = tk.Entry()
        self.systemUserIdInput["textvariable"] = self.entryFieldValue
        self.systemUserIdInput["width"] = 30
        self.systemUserIdInput.pack()



    # Entry field label
    def create_label_systemUserPass(self):
        self.systemUserPass = tk.Label()
        self.systemUserPass["text"] = "Password"
        self.systemUserPass["font"] = ("bold", 10)
        self.systemUserPass["pady"] = 10
        self.systemUserPass.pack()



    # Input fields
    def create_entry_userpass(self):
        self.systemUserPassVal = tk.StringVar()
        self.systemUserPassInput = tk.Entry()
        self.systemUserPassInput["textvariable"] = self.systemUserPassVal
        self.systemUserPassInput["width"] = 30
        self.systemUserPassInput.pack()
        # self.systemUserPassInput.insert(0, "here goes default text")



    # empty widget create method
    def create_empty_second(self):
        self.secondEmpty = tk.Label()
        self.secondEmpty["text"] = ""
        self.secondEmpty["pady"] = 10
        self.secondEmpty.pack()



    # button widget create method
    def create_button(self):
        self.sysLogin = tk.Button()
        self.sysLogin["text"] = "Sign In"
        self.sysLogin["padx"] = 25
        self.sysLogin["command"] = self.localAuthentication
        self.sysLogin["fg"] = "white"
        self.sysLogin["bg"] = "#3399ff"
        self.sysLogin.pack()



    def localAuthentication(self):
        userid = self.systemUserIdInput.get()
        userpassword = self.systemUserPassInput.get()
        svlogin.StaticVars.userId = userid
        svlogin.StaticVars.userPass = userpassword

        # data packet for authentication api call
        data = {
                'name': svlogin.StaticVars.userId,
                'password': svlogin.StaticVars.userPass,
                'token': 'LDiDPgxFCxXOesKGm4gxc0iIseM24P'
            }

        # api call
        clientAuthentication = rq.get(svlogin.StaticVars.clientAuthenticationApi, data)
        result = clientAuthentication.json()

        # User authenticated
        if result['status'] == 200:
            print("user confirmed")
            svlogin.StaticVars.isAuthenticated = True
            self.master.destroy()
        # User unauthorized
        else:
            print("user denied")
            svlogin.StaticVars.isAuthenticated = False

        # self.master.destroy()



def create():
    root = tk.Tk()
    app = SystemLogin(master=root)
    app.mainloop()