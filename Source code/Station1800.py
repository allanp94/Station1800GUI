import os
import subprocess
from MESintegration import MESLogIn
from MESintegration import MESWork
from MESintegration import MESLogout
import configparser
from shutil import copyfile
import win32gui, win32con

class data:
    def __init__(self, badge, serialNumber, puma, MDL1, MDL2):
        self.badge = badge
        self.serialNumber = serialNumber
        self.puma = puma
        self.MDL1 = MDL1
        self.MDL2 = MDL2

    def print(self):
        print(f"badge {self.badge} serial {self.serialNumber} puma {self.puma} mdl {self.MDL1} mdl2 {self.MDL2}" )

class driver:
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

def openFile(name):
    lines = None
    with open(name, "r") as file1:
        lines = file1.readlines()
        print(lines[0])
    data = data(lines[0], lines[1], lines[2], lines[3], lines[4])
    print(data)



openFile("1800.txt")

    


if __name__ == "__main__":
    # Initialize variables
    driver = driver(None)


