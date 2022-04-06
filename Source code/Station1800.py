import os
import subprocess
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
from MESintegration import MESLogIn
from MESintegration import MESWork
from MESintegration import MESLogout
from shutil import copyfile
from ProcessKiller import killProcess
import win32gui
from LabViewIntergration import LabViewIntergration


class data:
    def __init__(self, badge, serialNumber, puma, MDL1, MDL2, unitSize, unitType):
        self.badge = badge
        self.serialNumber = serialNumber
        self.puma = puma
        self.MDL1 = MDL1
        self.MDL2 = MDL2
        self.unitSize = unitSize
        self.unitType = unitType

class inputField:
    def __init__(self, Badge, Serial, Puma, MDL1, MDL2, runbttn_image, runbttn_tlrnc, checkbttn_image, checkbttn_tlrnc, waitMul, keyWord):
        self.Badge = Badge
        self.Serial = Serial
        self.Puma = Puma
        self.MDL1 = MDL1
        self.MDL2 = MDL2
        self.runbttn_image = runbttn_image
        self.runbttn_tlrnc = runbttn_tlrnc
        self.checkbttn_image = checkbttn_image
        self.checkbttn_tlrnc = checkbttn_tlrnc
        self.waitMul = waitMul
        self.keyWord = keyWord

class driver:
    def __init__(self, driver):
        self.driver = driver


###################################################################################################################
###                                                                                                             ###
###                                       GENERAL FUNCTIONS                                                      ###
###                                                                                                             ###
###################################################################################################################

def RiseGUI(): #raising GUI to the front of the screen using Macro Scheduler
    subprocess.call([".\\Macro\\bringGUI2Front.exe"])


"""def BringGUI2Front(frame, nextInputField):
    frame.focus_force()
    nextInputField.focus_set()"""


def raise_frame(frame, inputField=None): #raising a certain frame
    """
    Moves frame to the top of the GUI, sets focus on the indicated input field
    """
    frame.tkraise()
    frame.focus_force()
    if inputField != None:
        inputField.focus_set()


def selectImageFile(imageType):

    sourceFile = filedialog.askopenfilename(
        initialdir=".\\Macro\\Macro image files", title='Select image file',
        filetypes=(("JPG files", "*.jpg"), ("BMP files", "*.bmp"), ("All files", "*.*")))

    # Copy image file to the Macro images folder
    # if not os.path.isfile(os.path.join(".\\Macro\\Macro image files", os.path.split(filename)[1])):
    #     copyfile(filename, os.path.join(".\\Macro\\Macro image files", os.path.split(filename)[1]))

    destinationFile = os.path.join(".\\Macro\\Macro image files", os.path.split(sourceFile)[1])
    try:
        copyfile(sourceFile, destinationFile)
    except:
        pass
    if imageType == "RunButton":
        inputField.runbttn_image = "Macro image files\\" + os.path.split(sourceFile)[1]
    elif imageType == "CheckButton":
        inputField.checkbttn_image = "Macro image files\\" + os.path.split(sourceFile)[1]


def displayError(Error_number, message): #displaying an error message
    """
    Displays an Error box with the desired message in it
    """
    messagebox.showerror("Error " + str(Error_number), message)


def login(selfFrame, nextFrame, selfInputField, nextInputField): #logging in function
    """
    Saves the badge number to data.badge and displays the next frame of the GUI, setting the focus on the next input
    field (serial number input field).

    If a wrong badge number is input it displays an error message and clears the badge input field
    """
    data.badge = selfInputField.get()
    if data.badge.isdigit() and len(data.badge) <= 6 and len(data.badge) >= 4:
        driver.driver = MESLogIn(data)                                                                                # MES Integration
        # workingTime.clockIn = time.perf_counter() will not use a time clockin 
        ClearField(inputField.Serial)
        ClearField(inputField.Puma)
        ClearField(inputField.MDL1)
        ClearField(inputField.MDL2)

        raise_frame(nextFrame, nextInputField)
    else:
        displayError(7, "Invalid ID")
        # Clear entry field
        ClearField(selfInputField)
        raise_frame(selfFrame, selfInputField)


def Logout(nextFrame): #logout function
    MESLogout(driver.driver)
    ClearField(inputField.Badge)
    raise_frame(nextFrame, inputField.Badge)


def ClearField(inputField): #clearing the text box
    """
    Clears the input field provided
    """
    inputField.delete(0,END)


def clearUnitEntryFieldsAndWipeOutData(): #clears data for entry boxes and empty class variables
    """
    Clears every input field in the second frame (serial number, puma, MDL1, MDL2)
    Wipes out data
    """
    for entry in (inputField.Serial, inputField.Puma, inputField.MDL1, inputField.MDL2):
        ClearField(entry)
    data.serialNumber = ""
    data.puma = ""
    data.MDL1 = ""
    data.MDL2 = ""
    data.unitSize = ""
    data.unitType = ""


def GoToNextEntry(selfEntry, attribute, nextEntry=None, MDL2_entry=None):
    """
    This function switches the focus from one entry box to the next

    ex. once the serial number is typed in by the user with the help of a scanner and the enter key is pressed (scanner
    does this automatically) we want to switch the focus to the next entry field automatically (in this case the puma entry field)
    This helps save time so the operator doesn't have to click anything on the screen.

    We'll get the length of the unit from the serial number. This parameter will tell us if the input field MDL2 is needed or not.
    If it's not needed the MDL2 input field will remain disabled. Otherwise it will be enabled (set to 'normal').
    Note: only 48" and 60" units require a second MDL.

    Once everything is scanned in the macro will execute automatically.

    EXECUTION

    The serial number is scanned in. This value is stored in data.serialNumber. The unit size is obtained based on this
    value and stored in data.unitSize. If a 48" or 60" unit is scanned the MDL2 entry field becomes enabled. Go to next
    entry field (Puma).

    Scan the Puma. This value is stored in data.puma. Go to next entry field (MDL1)

    Scan MDL1. This value is stored in data.MDL1.
        If a 30" or 36" unit is scanned the macro will execute once the MDL1 entry field is filled and enter is pressed
        If a 48" or 60" unit is scanned, go to next entry field (MDL2)

            Scan MDL2. This value is stored in data.MDL2. Macro will execute once the MDL2 entry field is filled and enter is pressed

    PARAMETERS

    :param selfEntry: the input field that you're currently typing in
    :param attribute: the attribute of the data class where you want to store what you just typed in the input field
    :param nextEntry: the input field you want to switch focus to. If this parameter is not specified it will take the value None
    :param MDL2_entry: the last input field (MDL2). If this parameter is not specified it will take the value None
    :return: No returns
    """
    # data.attribute = selfEntry.get()                            # Save serial number
    if attribute == "serialNumber":
        data.serialNumber = selfEntry.get()
        serialNum = data.serialNumber
        unitSize = ""

        try:
            # 5610447$18642369$M141000$DF48650G/S/P
            #slicing through serial number to just the model code "DF48...."
            unitSize = serialNum.split("$")[3]  
            if unitSize.startswith("ICBDF") or unitSize.startswith("ICBIR"):
                try:
                    data.unitType = unitSize[0:5]
                    unitSize = int(unitSize[5:7])
                except:
                    displayError(1, "Problems finding the unit size in ICB unit")
                    ClearField(selfEntry)  # Clear entry field
            elif unitSize.startswith("DF") or unitSize.startswith("IR"):
                try:
                    data.unitType = unitSize[0:2]
                    unitSize = int(unitSize[2:4])
                except:
                    displayError(2, "Problems finding the unit size in regular")
                    ClearField(selfEntry)                       # Clear entry field
            else:
                displayError(3, "Problems finding the unit type in serial")
                ClearField(selfEntry)                           # Clear entry field
        except:
            displayError(4, "Serial string could not be parsed")
            ClearField(selfEntry)                               # Clear entry field
            selfEntry.focus_set()
            

        data.unitSize = unitSize # Save unit size

        if data.unitSize == 48 or data.unitSize == 60:      # Change the state of MDL2 entry field to normal if unit is 48" or 60"
            MDL2_entry['state'] = "normal"

        if data.unitType == "DF" or data.unitType == "IR":
            inputField.Puma["state"] = "normal"

    elif attribute == "puma":
        data.puma = selfEntry.get()
        if not data.puma.startswith("9041664"):
            displayError(5, "Wrong puma serial number")
            ClearField(selfEntry)  # Clear entry field
            selfEntry.focus_set()
            

    elif attribute == "MDL1":
        data.MDL1 = selfEntry.get()
        if not data.MDL1.startswith("215033"):
            displayError(6, "Wrong MDL serial number")
            ClearField(selfEntry)  # Clear entry field
            selfEntry.focus_set()
            

    elif attribute == "MDL2":
        data.MDL2 = selfEntry.get()
        if not data.MDL2.startswith("215033"):
            displayError(6, "Wrong MDL serial number")
            ClearField(selfEntry)  # Clear entry field
            selfEntry.focus_set()
            

    else:
        print("Error\nBad entry field")

    if nextEntry == None:
        # doMacro()
        if LabViewIntergration(data.serialNumber, data.badge,  data.puma):
            driver.driver = MESWork(data, driver.driver)            # Call driver and input data                              # MES Integration
        else:
            print('standard test interface test failed -- line 282')
            messagebox.showwarning("Warning", 
            "TEST FAILED -- clear input fields and scan items again")
    else:
        nextEntry.focus_set()

    # ICB's do not get a PUMA 
    if (data.unitType == "ICBDF" or data.unitType == "ICBIR") and nextEntry == inputField.Puma:
        inputField.MDL1.focus_set()

    if attribute == "MDL1":                                     # If we're scanning MDL1, go to next entry field (MDL2) if unit requires it.
        if (data.unitSize == 48 or data.unitSize == 60):
            nextEntry.focus_set()
        else:                                                   # Otherwise execute macro
            # doMacro()
            if LabViewIntergration(data.serialNumber, data.badge,  data.puma):
                driver.driver = MESWork(data, driver.driver)            # Call driver and input data                              # MES Integration
            else:
                print('standard test interface test failed -- line 300')
                messagebox.showwarning("Warning", 
                "TEST FAILED -- clear input fields and scan items again")


def submit(): #saving entered values into class variable
    data.serialNumber = inputField.Serial.get()
    try:
        data.puma = inputField.Puma.get()
    except:
        pass
    data.MDL1 = inputField.MDL1.get()
    try:
        data.MDL2 = inputField.MDL2.get()
    except:
        pass
    # doMacro()
    if LabViewIntergration(data.serialNumber, data.badge,  data.puma):
        # MES Integration
        driver.driver = MESWork(data, driver.driver)            # Call driver and input data  
    else:
        print('standard test interface test failed -- line 322')
        messagebox.showwarning("Warning", 
        "TEST FAILED -- clear input fields and scan items again")


def startOver():
    clearUnitEntryFieldsAndWipeOutData()                    # Clear entry fields and data stored
    inputField.Puma["state"] = "disabled"                   # Disable Puma input field
    inputField.MDL2["state"] = "disabled"                   # Disable MDL2 input field
    inputField.Serial.focus_set()                           # Set focus on serial input field

def nextUnitPrep():
    clearUnitEntryFieldsAndWipeOutData()                    # Clear entry fields and data stored
    inputField.Puma["state"] = "disabled"                   # Disable Puma input field
    inputField.MDL2["state"] = "disabled"                   # Disable MDL2 input field

    print("Bring GUI to front")
    GUI_hwnd = findApplication("Macro for Station 1800, by Jeyc")
    try:
        win32gui.SetForegroundWindow(GUI_hwnd)
    except Exception as e:
        print(e)

    RiseGUI()                                               # Bring GUI to front again

    print("GUI up. Clearing entry fields")
    inputField.Serial.focus_set()   

def findApplication (applicationName):
        """
        This function returns the application handle of a program running in your computer

        For example, assume that you have Notepad open and you would like to get the handle of this program so you can
        interact with it (bring to front, maximize, etc). you would use this application in the following way

        appHndl = findApplication("Untitled - Notepad")
        try:
            win32gui.SetForegroundWindow(appHndl)
        except:
            print("Couldn't bring Notepad to the front of your screen")
        """

        try:
            return win32gui.FindWindow(None, applicationName)
        except Exception as e:
            print(e)



###################################################################################################################
###                                                                                                             ###
###                                    GRAPHICAL USER INTERFACE                                                 ###
###                                             GUI                                                             ###
###################################################################################################################


def GUI(): #GUI
    global loginFrame, scanFrame
    """
    This is the user interface. It contains only the buttons and entry boxes that the user can interact with
    """

    # Define window parameters
    window = Tk()
    window.title("Macro for Station 1800, by Jeyc")
    window.resizable(width=False, height=False)


    icon_Path = ".\\Media\\SmartGuy_Ico.ico"
    window.iconbitmap(icon_Path)

    backgroungImage_Path = ".\\Media\\background.jpg"
    backgroungImage = ImageTk.PhotoImage(Image.open(backgroungImage_Path))

    # Place frames
    loginFrame = Frame(window)
    scanFrame = Frame(window)
    for frame in (loginFrame, scanFrame):
        frame.grid(row=0, column=0, sticky='news')


    ###################################################################################################################
    ###                                            LOGIN FRAME                                                      ###
    ###                                                                                                             ###
    ###                                                                                                             ###
    ###   Contains the initial screen where operator has to input his/her badge number so they can start            ###
    ###   scanning units                                                                                            ###
    ###################################################################################################################

    #Wolf Logo
    wolfLogo = Label(loginFrame, image=backgroungImage)
    wolfLogo.pack()

    text1 = Label(loginFrame, text="Welcome", fg="white", bg="#012B7D", font=('times','35', 'bold'))
    text1.place(relx=0.5, rely=0.2, anchor="center")

    text2 = Label(loginFrame, text="Scan your ID:", fg="white", bg="#0071AB", font=('times','25'))
    text2.place(relx=0.5, rely=0.4, anchor="center")

    inputField.Badge = Entry(loginFrame, width=10, bg="white", borderwidth=5, font=('times','25'), justify='center')
    inputField.Badge.place(relx=0.5, rely=0.7, anchor="center")
    inputField.Badge.focus_set()

    logIn_Bttn = Button(loginFrame, text="Log in", command=lambda: login(loginFrame, scanFrame, inputField.Badge, inputField.Serial), bg="light blue", font=('times','15'), relief=RAISED, borderwidth=5)
    logIn_Bttn.place(relx=0.5, rely=0.9, anchor="center")
    inputField.Badge.bind('<Return>', lambda event: login(loginFrame, scanFrame, inputField.Badge, inputField.Serial))


    ###################################################################################################################
    ###                                             SCAN FRAME                                                      ###
    ###                                                                                                             ###
    ###                                                                                                             ###
    ###   Contains the screen where operator has to scan the serial number, puma, MDL 1, and MDL2 (if required)     ###
    ###                                                                                                             ###
    ###################################################################################################################

    text_Relx = 0.4
    IF_Relx = 0.45
    image_Relx = 0.905
    _rely = 0.1

    wolfLogo = Label(scanFrame, image=backgroungImage)
    wolfLogo.pack()

    text3 =Label(scanFrame, text= "Scan pallet label:", fg="white", bg="#011F67", font=('times','25'))
    text3.place(relx=text_Relx, rely=_rely, anchor="e")

    inputField.Serial = Entry(scanFrame, width=15, bg="white", font=('times','25'), borderwidth=4)
    inputField.Serial.place(relx=IF_Relx, rely=_rely, anchor="w")
    inputField.Serial.bind('<Return>', lambda event: GoToNextEntry(inputField.Serial, "serialNumber", inputField.Puma, inputField.MDL2))

    labelImage = ImageTk.PhotoImage(Image.open(".\\Media\\label.jpg"))
    chip_Canvas = Label(scanFrame, image=labelImage)
    chip_Canvas.place(relx=image_Relx, rely=_rely, anchor="w")

    text4 = Label(scanFrame, text= "Scan Puma:", fg="white", bg="#004694", font=('times','25'), justify="right")
    text4.place(relx=text_Relx, rely=_rely*3, anchor="e")

    inputField.Puma = Entry(scanFrame, width=15, bg="white", font=('times','25'), borderwidth=4)
    inputField.Puma.place(relx=IF_Relx, rely=_rely * 3, anchor="w")
    inputField.Puma.bind('<Return>', lambda event: GoToNextEntry(inputField.Puma, "puma", inputField.MDL1))
    inputField.Puma["state"] = "disabled"

    chipImage = ImageTk.PhotoImage(Image.open(".\\Media\\chip.jpg"))
    chip_Canvas = Label(scanFrame, image=chipImage)
    chip_Canvas.place(relx=image_Relx, rely=_rely*3, anchor="w")

    text5 = Label(scanFrame, text= "Scan MDL:", fg="white", bg="#0472A3", font=('times','25'), justify="right")
    text5.place(relx=text_Relx, rely=_rely*5, anchor="e")

    inputField.MDL1 = Entry(scanFrame, width=15, bg="white", font=('times','25'), borderwidth=4)
    inputField.MDL1.place(relx=IF_Relx, rely=_rely*5, anchor="w")
    inputField.MDL1.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL1, "MDL1", inputField.MDL2))

    MDLImage = ImageTk.PhotoImage(Image.open(".\\Media\\MDL.png"))
    chip_Canvas = Label(scanFrame, image=MDLImage)
    chip_Canvas.place(relx=image_Relx, rely=_rely*5, anchor="w")



    text6 = Label(scanFrame, text="Scan MDL:", fg="white", bg="#2099C6", font=('times', '25'), justify="right")
    text6.place(relx=text_Relx, rely=_rely*7, anchor="e")

    inputField.MDL2 = Entry(scanFrame, width=15, bg="white", font=('times','25'), borderwidth=4)
    inputField.MDL2.place(relx=IF_Relx, rely=_rely * 7, anchor="w")
    inputField.MDL2.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL2, "MDL2"))
    inputField.MDL2["state"] = "disabled"

    MDL2Image = ImageTk.PhotoImage(Image.open(".\\Media\\MDL2.png"))
    chip_Canvas = Label(scanFrame, image=MDL2Image)
    chip_Canvas.place(relx=image_Relx, rely=_rely*7, anchor="w")

    logOut_Bttn = Button(scanFrame, text="Log out", command=lambda: Logout(loginFrame), bg="light blue", font=('times', '15'), relief=RAISED, borderwidth=5)
    logOut_Bttn.place(relx=0.3, rely=_rely*9, anchor="center")

    Clear_Bttn = Button(scanFrame, text="Clear fields", command=startOver, bg="light blue", font=('times', '15'), relief=RAISED, borderwidth=5)
    Clear_Bttn.place(relx=0.5, rely=_rely * 9, anchor="center", x=30)

    # the submit button calls the submit() but the way the program functions with the scanner
    # as the main input source the submit() never gets called
    Submit_Bttn = Button(scanFrame, text="Submit", command=lambda: submit(), bg="light blue", font=('times', '15'), relief=RAISED, borderwidth=5)
    Submit_Bttn.place(relx=0.7, rely=_rely*9, anchor="center", x=55)
  

    # initial frame
    raise_frame(loginFrame, inputField.Badge)

    window.mainloop()


if __name__ == "__main__":
    # Initialize variables
    data = data("","","","","","","")
    inputField = inputField(None, None, None, None, None, None, None, None, None, None, None)
    driver = driver(None)

    # Kill any Chrome process
    killProcess("CHROME.EXE")
    killProcess("CHROMEDRIVER.EXE")

    # Execute GUI
    GUI()
