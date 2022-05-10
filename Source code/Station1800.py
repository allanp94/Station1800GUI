from lib2to3.pgen2 import driver
from MESintegration import MESLogIn
from MESintegration import MESWork
from ProcessKiller import killProcess

# D1800
# RFIDWritePlugin ---> files to put it in

#LOGS/1800MESIntergrations ---> location of .txt file to read from

#1800Script ---> .exe name

dataFromFile = ['','','','','']

#read data from .txt file 
def openFile(name):
    with open(name, "r") as file1800:
        data = file1800.readlines()
    for x, val in enumerate(data):
        dataFromFile[x] = val.strip()

#txt file location on deployment machine
openFile(r"C:\LOGS\1800MESIntegration.txt")
print(dataFromFile)

# close other chrome webpages
killProcess("CHROME.EXE")
killProcess("CHROMEDRIVER V80.EXE")

# pass in badge number to log in to MES
# function returns the chromedriver instance
driver = MESLogIn(dataFromFile[0])

# pass in data and the driver that was used to sign in
MESWork(dataFromFile, driver)
