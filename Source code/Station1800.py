import os
import subprocess
from MESintegration import MESLogIn
from MESintegration import MESWork
from MESintegration import MESLogout
import configparser
from shutil import copyfile
from ProcessKiller import killProcess
import win32gui, win32con

class data:
    def __init__(self, badge, serialNumber, puma, MDL1, MDL2):
        self.badge = badge
        self.serialNumber = serialNumber
        self.puma = puma
        self.MDL1 = MDL1
        self.MDL2 = MDL2

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

if __name__ == "__main__":
    # Initialize variables
    data = data("","","","","","","")
    driver = driver(None)

