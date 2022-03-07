import pyautogui
import os

# a small demonstration program on how to interact with the labview testing 
# interface

eightLoc = os.path.join(os.path.dirname(__file__), 'eightsAreGreat.PNG')


eight = pyautogui.locateOnScreen(eightLoc)
# eightScreenLoc = pyautogui.center(eightLoc)
print(eight)
print(eight.left)
pyautogui.click(eight.left, eight.top)