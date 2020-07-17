import pyodbc
import selenium
from Helpers import bColors as tc
import Helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

manufacturerColumn = config.get('Config', 'manufacturerColumn')
hpPcNames = config.get('Config', 'hpPcNames')
buyDateColumn = config.get('Config', 'buyDateColumn')
expDateColumn = config.get('Config', 'expDateColumn')
prodNumColumn = config.get('Config', 'prodNumColumn')
serialColumn = config.get('Config', 'serialColumn')
tableName = config.get('Config', 'tableName')
countryCode = config.get('Config', 'countryCode')

print(tc.OKGREEN + "SETTINGS:" +tc.ENDC)


print(tc.OKBLUE + "manufacturerColumn: " +tc.ENDC+ manufacturerColumn)
print(tc.OKBLUE + "hpPcNames: " +tc.ENDC+ hpPcNames)
print(tc.OKBLUE + "buyDateColumn: " +tc.ENDC+ buyDateColumn)
print(tc.OKBLUE + "expDateColumn: " +tc.ENDC+ expDateColumn)
print(tc.OKBLUE + "prodNumColumn: " +tc.ENDC+ prodNumColumn)
print(tc.OKBLUE + "serialColumn: " +tc.ENDC+ serialColumn)


SelectString = "SELECT * FROM "+tableName+ " WHERE ["+manufacturerColumn+"] IN ("+hpPcNames+") AND (["+buyDateColumn+"] IS NULL OR ["+expDateColumn+"] IS NULL OR ["+prodNumColumn+"] IS NULL);"
CountString = "SELECT COUNT(*) FROM "+tableName+ " WHERE ["+manufacturerColumn+"] IN ("+hpPcNames+") AND (["+buyDateColumn+"] IS NULL OR ["+expDateColumn+"] IS NULL OR ["+prodNumColumn+"] IS NULL);"

conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ='+ config.get('Config', 'dbPath')+ ';')

totalRowsc = conn.cursor()
totalRowsc.execute(CountString)
totalRows = totalRowsc.fetchone()[0]
totalRows = int(totalRows)
currentRow = 0

cursor = conn.cursor()
#cursor.execute("SELECT * FROM Computers WHERE [?] IN (?) AND ([?] IS NULL OR [?] IS NULL OR [?] IS NULL);",manufacturerColumn,hpPcNames,expDateColumn,prodNumColumn)
cursor.execute(SelectString)





Helpers.ProgressBar.draw(0,totalRows, 100)
for row in cursor.fetchall():

    SerialNumber = row.__getattribute__(serialColumn)
    
    

    driver = webdriver.Firefox()
    #driver = webdriver.PhantomJS(r'phantomjs-2.1.1-windows\bin\phantomjs.exe')
    #open website
    driver.get('https://support.hp.com/'+countryCode+'-en/checkwarranty')



    #Select the serial number input box
    serial_box = driver.find_element_by_id('wFormSerialNumber')


    acceptCookies = driver.find_element_by_class_name('accept-cookies-button')
    script = acceptCookies.get_attribute("onclick")
    driver.execute_script(script)

    #Scrolls down page to avoid accepting cookies
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 

    #click submit button
    submit_btn = driver.find_element_by_id('btnWFormSubmit')

    #Type in the serial number
    serial_box.send_keys(SerialNumber)

    #click submit button
    submit_btn.click()

    #wait for the page to load
    driver.implicitly_wait(10)

    #get values
    ProductNumber = None

    
    try:
        ProductNumber_box = driver.find_element_by_id('productNumberValue')
        buyDate_box = driver.find_element_by_xpath('//*[@id="warrantyResultBase"]/div/div[1]/div[1]/div[4]/div[2]')
        expDate_box =  driver.find_element_by_xpath('//*[@id="warrantyResultBase"]/div/div[1]/div[1]/div[5]/div[2]')
        
        ProductNumber = ProductNumber_box.text
        buyDate = buyDate_box.text
        expDate = expDate_box.text

        if buyDate == '' or expDate == '' or buyDate == None or expDate == None:
            buyDate_box = driver.find_element_by_xpath('//*[@id="additionalExtWarranty_1"]/div/div/div[1]/div[4]/div[2]')
            expDate_box =  driver.find_element_by_xpath('//*[@id="additionalExtWarranty_1"]/div/div/div[1]/div[5]/div[2]')
            buyDate = buyDate_box.text
            expDate = expDate_box.text

        #print("\rProduct number: "+ProductNumber)
        #print("\rDate of purchase: " +buyDate)
        #print("\rWarranty expires: " +expDate)

        sqlSuccess = "UPDATE "+tableName+" SET ["+buyDateColumn+"] = '"+ buyDate+"', ["+expDateColumn+"] = '" +expDate+ "', ["+prodNumColumn+"] = '" + ProductNumber+"' WHERE ["+serialColumn+"] ='"+SerialNumber+"';"
        
        

        #cursor.execute("UPDATE Computers SET [PurchaseDate] = ?, [WarrantyExpiration] = ?, [ProductNumber] = ? WHERE [Serial number] = ?;", buyDate, expDate, ProductNumber, SerialNumber)
        cursor.execute(sqlSuccess)
        cursor.commit()
        status = tc.OKGREEN+"[OK]"+ tc.OKBLUE+" ["+SerialNumber+"] " + tc.ENDC+ "succsess                                                                  "
    except:
        try:
            if(ProductNumber != None):
               #cursor.execute("UPDATE Computers SET [ProductNumber] = ? WHERE [Serial number] = ?;", ProductNumber, SerialNumber)
                sqlWarning = "UPDATE "+tableName+" SET ["+prodNumColumn+"] = '"+ProductNumber+"' WHERE ["+serialColumn+"] = '"+SerialNumber+"';"
                cursor.execute(sqlWarning)
                cursor.commit()
                status = tc.WARNING+"[WARNING]"+ tc.OKBLUE+" ["+SerialNumber+"] " + tc.ENDC +" Only Product number found                                   "
            else:
                #cursor.execute("UPDATE Computers SET [ProductNumber] = ? WHERE [Serial number] = ?;", 'Need product number', SerialNumber)
                sqlFail =    "UPDATE "+tableName+" SET ["+prodNumColumn+"] = 'Need product number' WHERE ["+serialColumn+"] = '"+SerialNumber+"';"
                cursor.execute(sqlFail)
                cursor.commit()
                status = tc.FAIL +"[FAILED]"+ tc.OKBLUE+" ["+SerialNumber+"] " + tc.ENDC + "Could not find values: product number required                 "
        except:
            #cursor.execute("UPDATE Computers SET [ProductNumber] = ? WHERE [Serial number] = ?;", 'Need product number', SerialNumber)
            sqlFail =    "UPDATE "+tableName+" SET ["+prodNumColumn+"] = 'Need product number' WHERE ["+serialColumn+"] = '"+SerialNumber+"';"
            cursor.execute(sqlFail)
            cursor.commit()
            status = tc.FAIL +"[FAILED]"+ tc.OKBLUE+" ["+SerialNumber+"] "+ tc.ENDC + " ould not find values: product number required                     "

    currentRow+=1
    Helpers.ProgressBar.draw(currentRow,totalRows, 100, ' '+status+'\r')
    
    driver.close()

    


    


print("\r"+tc.OKGREEN+"DONE!"+tc.ENDC)


