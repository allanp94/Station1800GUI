from lib2to3.pgen2 import driver
from MESintegration import MESLogIn, testing
from MESintegration import MESWork
from ProcessKiller import killProcess, process_exists
from selenium import webdriver


# D1800
# RFIDWritePlugin ---> files to put it in

#LOGS/1800MESIntergrations ---> location of .txt file to read from

#1800Script ---> .exe name


dataFromFile = ['','','','','']

def openFile(name):
    with open(name, "r") as file1800:
        data = file1800.readlines()
    for x, val in enumerate(data):
        dataFromFile[x] = val.strip()


#read values from file for testing purpose
# openFile("1800.txt")

#txt file location on deployment machine
openFile(r"C:\LOGS\1800MESIntegration.txt")
print(dataFromFile)

# close other chrome webpages if open
# killProcess("CHROME.EXE")
# killProcess("CHROMEDRIVER.EXE")

if process_exists("Chromedriver.exe"):
    print('chromedriver running')
else:
    print('not chromedriver available')

# pass in badge number to log in to MES
# function returns the chromedriver instance that was used to do so
driver = MESLogIn(dataFromFile[0])



# pass in data and the driver that was used to sign in
MESWork(dataFromFile, driver)
# testing(driver, dataFromFile)
