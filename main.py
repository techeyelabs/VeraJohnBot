# from ClientViews.systemlogin import *
import ClientViews.systemlogin as cs
import ClientViews.botwindow as bw
import ClientViews.StaticVars as sv
import time

# login screen for user to log into the client application from systemlogin module
sysLoginWindow = cs.create()
print(sv.StaticVars.userId)

userid = sv.StaticVars.userId
userpass = sv.StaticVars.userPass


# User is authenticated
if sv.StaticVars.isAuthenticated == True:
    sysLoginWindow = bw.create()


