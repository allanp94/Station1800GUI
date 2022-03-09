import opcode
from traceback import print_tb
from webbrowser import open_new_tab
import pyautogui
import os
from ProcessKiller import process_exists
import subprocess
import win32gui,win32con, time

# # a small demonstration program on how to interact with the labview testing 
# # interface

# #find the picture trying to locate
# eightLoc = os.path.join(os.path.dirname(__file__), '..', 'Macro image files', 'RunButton.jpg')
# #locate picture on screen
# eight = pyautogui.locateOnScreen(eightLoc)
# # eightScreenLoc = pyautogui.center(eightLoc)
# print(eight)
# print(eight.left)
# pyautogui.click(eight.left, eight.top)

def locateButton(name):
    buttonLoc = os.path.join(os.path.dirname(__file__), name)
    print(f"picture at location {buttonLoc}")
    #locate picture on screen
    button = pyautogui.locateOnScreen(buttonLoc)
    location = pyautogui.center(button) #center of the picture
    return location

def clickRunButton():
    try:
        runButtonLoc = locateButton('runButton.PNG')
        time.sleep(3)
        if runButtonLoc.x & runButtonLoc.y:
            pyautogui.click(runButtonLoc.x, runButtonLoc.y)        
        else: #if play button is not available it means that an input box is awaiting input
            redXMark = locateButton('redXMark.PNG')
            print(redXMark)
            if redXMark.x & redXMark.y:
                pyautogui.click(redXMark.x, redXMark.y)


        #if finding and clicking the runButton was successful return 1 else 0
        return 1 
    except:
        return 0


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

        #once opened bring to foreground
        bringToForeground("Standard Test Interface")
        
        return 1
    except:
        print('=== Was not able to open the Standard Testing interface ===')
        return 0

def LabViewIntergration(badgeNumber=None, unitSerialNumber=None, pumaBarcode=None): 

    openStandardTestInterface()
    if clickRunButton():
         #input data from the GUI
        print('input data from GUI')
        pyautogui.write("serial NUmber", interval=0.25)


def bringToForeground(name = None):
    try:
        # hwnd = win32gui.FindWindow("Notepad", None)
        hwnd = win32gui.FindWindow(None, name)
        if hwnd == 0:
            print('=== Requested window is not open at the moment ===')
        else:
            print(f'{name} is opening{ hwnd}')
            win32gui.SetForegroundWindow(hwnd)
            # hwnd = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(2)
            # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL) #brings the program back to original size
        
    except Exception as e:
        print(e)



LabViewIntergration()