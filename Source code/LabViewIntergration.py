import pyautogui
import os
from ProcessKiller import process_exists
import subprocess

# # a small demonstration program on how to interact with the labview testing 
# # interface

# #find the picture trying to locate
# runButton = os.path.join(os.path.dirname(__file__), '..', 'Macro image files', 'RunButton.jpg')
# #locate picture on screen
# eight = pyautogui.locateOnScreen(eightLoc)
# # eightScreenLoc = pyautogui.center(eightLoc)
# print(eight)
# print(eight.left)
# pyautogui.click(eight.left, eight.top)





def LabViewIntergration(badgeNumber=None, unitSerialNumber=None, pumaBarcode=None): 

    standardPlatform = 'Standard Platform.exe'
    standardPlatformAbsPath = r'C:\Users\schuyler.wulff\Desktop\D1800\Standard Platform.exe'
    # check to see if the RFID standard platform program is running 
    if process_exists(standardPlatform):
        # call function that finds the play button
        # and inputs the data from the GUI to the standard platform
        print("Standard Platform.exe is running")
    else:
        # call and open the standard Platform.exe
        print('trying to open .exe')
        openStandardPlatform =  subprocess.run([standardPlatformAbsPath])



LabViewIntergration()