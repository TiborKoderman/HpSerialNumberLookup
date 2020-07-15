import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SerialNum = ''


############
#LOOP START#
############
driver = webdriver.Firefox()
#open website
driver.get('https://support.hp.com/si-en/checkwarranty')



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
serial_box.send_keys(SerialNum)

#click submit button
submit_btn.click()

#wait for the page to load
driver.implicitly_wait(10)

#get values
ProductNumber_box = driver.find_element_by_id('productNumberValue')
buyDate_box = driver.find_element_by_xpath('//*[@id="warrantyResultBase"]/div/div[1]/div[1]/div[4]/div[2]')
expDate_box =  driver.find_element_by_xpath('//*[@id="warrantyResultBase"]/div/div[1]/div[1]/div[5]/div[2]')



ProductNumber = ProductNumber_box.text
buyDate = buyDate_box.text
expDate = expDate_box.text
print(ProductNumber)
print(buyDate)
print(expDate)

driver.close()
##########
#LOOP END#
##########