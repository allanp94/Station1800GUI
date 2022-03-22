from ast import Not
from email import message
import pyautogui
import os
from ProcessKiller import process_exists
import subprocess
import win32gui,win32con, time
from tkinter import messagebox


#global dictionary set for the button locations
buttonLocations = {}




#gets the img file location, locates the image on screen, returns center of location
def locateButton(name):
    if name in buttonLocations:
        print(buttonLocations)
        return buttonLocations[name]
    else:
        buttonLoc = os.path.join(os.path.dirname(__file__), '.', 'img', name)
        button =  pyautogui.locateOnScreen(buttonLoc) #locate picture on screen
        location = pyautogui.center(button) #center of the picture
        buttonLocations[name] = location
        print(buttonLocations)
        return location

#gets button file name, locates the center, and clicks on center
def clickButton(buttonName):
    try: 
        button = locateButton(buttonName)
        if (button.x & button.y):
            pyautogui.click(button.x, button.y)#click on returned x,y location 
            return 1 
    except:
        print(f'=== did not locate button from picture {buttonName} ===')
        return 0

#function that checks to see if the Standard platform executable is running
def openStandardTestInterface():
    try:
        standardPlatform = 'Standard Platform.exe'
        standardPlatformAbsPath = r'C:\Users\schuyler.wulff\Desktop\D1800\Standard Platform.exe'
        # check to see if the RFID standard platform program is running 
        if process_exists(standardPlatform):
            print("Standard Platform.exe is running")
        else:
            # call and open the standard Platform.exe
            print(f'trying to open {standardPlatform}')
            subprocess.Popen([standardPlatformAbsPath])
            time.sleep(20) #this will give the standard interface program time to fully load

        #once opened bring to foreground
        bringWindowToForeground("Standard Test Interface")
    except:
        print('=== Was not able to open the Standard Testing interface ===')

#inputs all the data in the pop-up window
def inputData(data = None):
    for num in data:
        pyautogui.write(num, interval=0.10)
        clickButton('GreenCheckButton.PNG')
        time.sleep(1) #this keeps the data from being cut during the write process
    clickButton('GreenCheckButton.PNG')

#if application passed is open then it brings it to the foreground
def bringWindowToForeground(name):
    try:
        hwnd = win32gui.FindWindow(None, name)
        if hwnd == 0:
            print('=== Requested window is not open at the moment ===')
        else:
            print(f'{name} is opening {hwnd}')
            win32gui.SetForegroundWindow(hwnd)
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(2)
    except Exception as e:
        print(e)


def LabViewIntergration(badgeNumber=None, unitSerialNumber=None, pumaBarcode=None): 
    data = [badgeNumber, unitSerialNumber, pumaBarcode]
    # data = ['5610447$18642369$M141000$DF48650G/S/P', '9217', '9041664$0006801C7BCC']
    print(data)
    openStandardTestInterface()
    # if clickRunButton():
    if clickButton('runButton.PNG'):
         #input data from the GUI
        print('input data from GUI')
        inputData(data)
    else:
        print('play button not visible')
        #if red X mark exists then start over the test
        if clickButton('redXMark.PNG'):
            LabViewIntergration(badgeNumber, unitSerialNumber, pumaBarcode)
        else:
            print('redXMark and runButton was not found')
    time.sleep(5)#wait for the program to complete
    if clickButton('testPassed.PNG'):
        print('test passed')
        return 1
    elif clickButton('testFailed.PNG'):
        print('test failed')
        return 0
    elif clickButton('setAction.PNG'):
        messagebox.showwarning("Warning", 
        "Make sure that there is a magnet/RFID tag present")
        response = messagebox.askyesno('Yes|No', 'Do you want to proceed?')
        print(response)

    

LabViewIntergration('5610447$18642369$M141000$DF48650G/S/P', '9217', '9041664$0006801C7BCC')
