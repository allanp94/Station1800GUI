from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tkinter import messagebox
import time
import os
from ProcessKiller import killProcess


webdriver.ChromeOptions().add_argument("--ignore-certificate-errors")
webdriver.ChromeOptions().add_argument("--no-sandbox")

def fileList(directory, *extension):
    """
    This program takes a directory path as input, then returns a list with all the files inside that folder
    that end with the extensions provided
    """
    programs = []

    for extns in extension[0]:
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                if filename.lower().endswith(extns):
                    programs.append(filename)
        else:
            print("Invalid directory path")
    return programs


def LaunchBrowser():
    # For testing
    # MESWebSite = "http://fit-wcapp-01.subzero.com:8000/EnterpriseConsole/BPMUITemplates/Default/Repository/Site/CustomLogin.aspx?ListItemId=e0a7e9d4-02f2-4c6d-898c-8714b73c8c08&FormLink=NGDF%20Station%209050"

    driver = None
    MESWebSite = "http://FIT-WCAPP-01.subzero.com:8000/EnterpriseConsole/BPMUITemplates/Default/Repository/Site/CustomLogin.aspx?ListItemId=E0A7E9D4-02F2-4C6D-898C-8714B73C8C08&FormLink=NGDF%20Station%201800"
    # import Chrome web driver

    listOfChromeDrivers = fileList(".\\Drivers\\", [".exe"])
    print(listOfChromeDrivers)
    for x in listOfChromeDrivers:
        try:
            driver = webdriver.Chrome(os.path.join(".\\Drivers\\", x))
            driver.get(MESWebSite)
            return driver
        except:
            pass
    print("None of the drivers worked")
    exit(0)



def pressButton(driver, findBy, errorMessage, ID=None, XPath=None):
    if findBy == "ID":
        try:
            x = driver.find_element_by_id(ID)
        except:
            print(errorMessage)
        else:
            x.click()

    elif findBy == "XPath":
        try:
            x = driver.find_element_by_xpath(XPath)
        except:
            print(errorMessage)
        else:
            x.click()

    return driver


def waitForWebsite(driver, findBy, item, waitTime):

    # Check if Sample is required
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "sampleoverlay"))
        )

        messagebox.showwarning("Warning",
                               "Sample required\nPlease, resolve this issue before continuing.\n"
                               "Accept this message ONLY AFTER the sample requirement has been satisfied")


    except Exception as e:
        print("No sample required. Carry on")

    finally:
        if findBy == "ID":
            try:
                WebDriverWait(driver, waitTime).until(
                    EC.presence_of_element_located((By.ID, item))
                )

                print(item + " found")


            except:
                print("Couldn't find item: " + item)
                messagebox.showwarning("Warning", "Couldn't find item: " + item)

            finally:
                return driver

        elif findBy =="Class":
            try:

                WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, item)))

                """WebDriverWait(driver, waitTime).until(
                    EC.presence_of_element_located((By.CLASS_NAME, item))
                )"""

                print(item + " found")
                return driver
            except:
                print("Couldn't find item " + item)
                messagebox.showwarning("Warning", "Couldn't find item: " + item)



            try:
                print("Searching for object")
                driver.find_element_by_class_name(item)
                print("Found 123")
            except:
                print("No luck searching by object with driver.find_element_by_class_name(item)")


def fillEntryBox(driver,findBy, errorMessage, text, ID=None, XPath=None, Class=None):
    x = None
    if findBy == "ID":
        try:
            x = driver.find_element_by_id(ID)
        except:
            print(errorMessage)
        else:
            x.clear()
            x.send_keys(text)

    elif findBy == "XPath":
        try:
            x = driver.find_element_by_xpath(XPath)
        except:
            print(errorMessage)
        else:
            x.clear()
            x.send_keys(text)

    elif findBy == "Class":
        try:
            x = driver.find_element_by_class_name(Class)
        except:
            print(errorMessage)
        else:
            x.clear()
            x.send_keys(text)
    return driver, x


#--------------------------------------------------------------------------------------------------------------#
def MESLogIn(badgeNum):
    driver = LaunchBrowser()
    driver = waitForWebsite(driver, "ID", "LogInButton", 10)
    driver, _ = fillEntryBox(driver, "ID", "Couldn't find id", badgeNum, ID="BadgeIDTextBox")
    driver = pressButton(driver, "ID", "Couldn't find login button", ID="LogInButton")
    driver = waitForWebsite(driver, "ID", "T7", 30)
    return driver


#--------------------------------------------------------------------------------------------------------------#
def MESWork(data, driver):

    print("switching to default frame")
    try:
        driver.switch_to.default_content()
        print("switched to default frame")
    except Exception as e:

        if str(e).startswith("Message: chrome not reachable") == True:
            print("Can't reach")
            # Chrome was closed and needs to be relaunched
            print("Chrome was closed and needs to be relaunched")

            killProcess("CHROME.EXE")
            killProcess("CHROMEDRIVER.EXE")

            # Log in again
            driver = MESLogIn(data)

        else:
            print(e)
    # driver.switch_to.default_content()
    driver = waitForWebsite(driver, "ID", "T7", 30)


    driver,_ = fillEntryBox(driver, "ID", "Couldn't find serial entry box", data[1], ID="T7") # Input serial number
    driver = pressButton(driver, "XPath", "Couldn't find load button", XPath="/html/body/form/div/div[10]/div[2]/div/div/div[1]/div[1]/div[4]/div/div[2]/div[5]/div[1]/div[4]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/button")
    driver = waitForWebsite(driver, "ID", "E2frameEmbedPage", 10)

    print("Switch to contentFrame iFrame")
    try:
        driver.switch_to.frame("E2frameEmbedPage")
        driver = waitForWebsite(driver, "ID", "T2", 10) #T2 is the "Scan Vendor Barcode" input box

        # check to see if unit has a KCV requirement for puma
        if 'DF' in data[1] or 'IR' in data[1]:
            driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data[2], ID="T2")
            entryBox.send_keys(Keys.RETURN)
            time.sleep(2)

        # MDL KVC requirement 
        driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data[3], ID="T2")
        entryBox.send_keys(Keys.RETURN)
        time.sleep(2)

        # if data[4] is true, means that two MDLs were scanned in by the user 
        # and that the present unit is a 48' or 60' and has two MDL KCV requirements
        if data[4]:
            driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data[4], ID="T2")
            entryBox.send_keys(Keys.RETURN)
            time.sleep(2)

    except:
        # Unit already scanned
        driver = waitForWebsite(driver, "Class", "skfli sklc skc lblBackflushComplete_skc", 10)
        driver = pressButton(driver, "Class", "Couldn't find scan for test button", "skfli sklc skc lblBackflushComplete_skc" )

    driver.switch_to.default_content()
    return driver

# #--------------------------------------------------------------------------------------------------------------#
# def MESLogout(driver):
#     driver.quit()


if __name__ == "__main__":
    pass