from operator import indexOf
import os
import subprocess
from MESintegration import MESLogIn
from MESintegration import MESWork
from MESintegration import MESLogout
from ProcessKiller import killProcess
from selenium import webdriver




class Driver:
    def __init__(self, driver):
        self.driver = driver


###################################################################################################################
###                                                                                                             ###
###                                       GENERAL FUNCTIONS                                                      ###
###                                                                                                             ###
###################################################################################################################

# D1800
# RFIDWritePlugin ---> files to put it in

#LOGS/1800MESIntergrations

#1800Temp ---> .exe name


dataFromFile = ['','','','','']

def openFile(name):
    with open(name, "r") as file1800:
        data = file1800.readlines()
    for x, val in enumerate(data):
        dataFromFile[x] = val.strip()


#read values from file 
openFile("1800.txt")
print(dataFromFile)


killProcess("CHROME.EXE")
killProcess("CHROMEDRIVER.EXE")
MESLogIn(dataFromFile)



