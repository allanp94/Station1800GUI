from operator import indexOf
import os
import subprocess
from MESintegration import MESLogIn
from MESintegration import MESWork
from MESintegration import MESLogout
from shutil import copyfile


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


MESLogIn(dataFromFile)


    


# if __name__ == "__main__":
#     # Initialize variables
#     driver = Driver(None)
    


