# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# from tkinter import messagebox
# import time
# import os
# from selenium.webdriver.chrome.options import Options
# # from selenium
# import selenium.common.exceptions as sex
#
# webdriver.ChromeOptions().add_argument("--ignore-certificate-errors")
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
#
# def LaunchBrowser():
#
#     MESWebSite = "https://www.google.com"
#     # import Chrome web driver
#
#     driver = webdriver.Chrome(os.path.join(".\\Drivers\\chromedriver V92.exe"))
#     driver.get(MESWebSite)
#     return driver
#
# # import httplib
# import socket
#
# from selenium.webdriver.remote.command import Command
#
# def get_status(driver):
#     try:
#         driver.execute(Command.STATUS)
#         print("Alive")
#     except:
#         print("Dead")
#
# if __name__ == "__main__":
#     driver = LaunchBrowser()
#     """    while True:
#         get_status(driver)
#         time.sleep(1)"""
#
#     """    DISCONNECTED_MSG = 'Unable to evaluate script: disconnected: not connected to DevTools\n'
#
#     while True:
#         driverMSG = driver.get_log('driver')[0]['message']
#         if driverMSG == DISCONNECTED_MSG:
#             print('Browser window closed by user')
#         else:
#             print("all gucci")
#         time.sleep(1)"""
#
#
#
#     """while True:
#         try:
#             x = driver.find_element_by_class_name("ddlsv-cta_")
#             print("Found")
#         except:
#             print("not found")
#         time.sleep(1)"""
#
#     while True:
#         try:
#             driver.switch_to.default_content()
#             print("All gucci")
#         except Exception as e:
#             print(str(e))
#             # print(sex.WebDriverException.msg)
#             # print(WebDriver.webDriverException)
#
#             if str(e).startswith("Message: chrome not reachable") == True:
#                 # if e.startswith("Message: chrome not reachable") == True:
#                 print("Can't reach")
#         else:
#             time.sleep(1)
#


import win32gui, win32con
import time
# try:
#     # hwnd = win32gui.FindWindow("Notepad", None)
#     hwnd = win32gui.FindWindow(None, "Calculator")
#     print(hwnd)
#     win32gui.SetForegroundWindow(hwnd)
#     # hwnd = win32gui.GetForegroundWindow()
#     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
#     time.sleep(2)
#     win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE) 
#     #brings the program back to original size
# except Exception as e:
#     print(e)


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
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE) #brings the program back to original size
        
    except Exception as e:
        print(e)

bringToForeground("Calculator")

    # input("press enter")
# import ctypes
#
# user32 = ctypes.WinDLL('user32')
# hwnd = user32.FindWindow("Standard Test Interface", None)
# SW_MAXIMISE = 3
#
# hWnd = user32.GetForegroundWindow()
#
# user32.ShowWindow(hWnd, SW_MAXIMISE)



# import ctypes
# import win32gui
# EnumWindows = ctypes.windll.user32.EnumWindows
# EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
# GetWindowText = ctypes.windll.user32.GetWindowTextW
# GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
# IsWindowVisible = ctypes.windll.user32.IsWindowVisible

# titles = []
# def foreach_window(hwnd, lParam):
#     if IsWindowVisible(hwnd):
#         length = GetWindowTextLength(hwnd)
#         buff = ctypes.create_unicode_buffer(length + 1)
#         GetWindowText(hwnd, buff, length + 1)
#         titles.append((hwnd, buff.value))
#     return True
# EnumWindows(EnumWindowsProc(foreach_window), 0)

# for i in range(len(titles)):
#     print(titles[i])
#     if titles[i][1] == "Macro for Station 1800, by Jeyc":
#         print("found")
#         try:
#             hwnd = win32gui.FindWindow(titles[i][1], None)
#             hwnd = win32gui.FindWindow(None, titles[i][1])

#             # hwnd = win32gui.FindWindow("Notepad", None)
#             # hwnd = win32gui.FindWindow("Standard Test Interface", None)
#             win32gui.SetForegroundWindow(hwnd)
#             # hwnd = win32gui.GetForegroundWindow()
#             # win32gui.ShowWindow(titles[i][0], win32con.SW_MAXIMIZE)
#         except Exception as e:
#             print(e)

# input("press enter")
# win32gui.MoveWindow((titles)[5][0], 0, 0, 760, 500, True)


# HLD = win32gui. FindWindow (None, "Notepad")
# print(HLD)