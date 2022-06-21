import time
import datetime
import random

from selenium import webdriver
from selenium.webdriver.common import by
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import smtplib, ssl

url = "http://www.seine-saint-denis.gouv.fr/booking/create/17088"
planning_num = ["990" , "1000", "1001", "1002", "1003", "1005", "1028", "1029"]
index = list(range(0,8))

#driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver.maximize_window()

sendemail = False
port = 587  # For starttls
smtp_server = "smtp.live.com"
sender_email = "email@hotmail.com"
password = "azerty"
message = """
Subject: Check PREFECTURE

This message is sent from Python."""

while True:
	driver.get(url)

	time.sleep(3)

	bad_gateway = 0
	indispo = 0
	overloaded = 0

	try:
		bad_gateway = driver.find_element(by.By.XPATH,"//*[contains(text(), 'Bad Gateway')]")
	except NoSuchElementException:
		True

	try:
		elem = driver.find_element(by.By.ID,"condition")
		driver.execute_script("arguments[0].click();",elem)
	except NoSuchElementException:
		True

	time.sleep(1)

	try:
		elem = driver.find_element(by.By.NAME,"nextButton")
		driver.execute_script("arguments[0].click();",elem)
	except NoSuchElementException:
		True

	time.sleep(5)

	try:
		ran = random.choice(index)
		planning_click='planning'+planning_num[ran]
		elem = driver.find_element(by.By.ID,planning_click)
		driver.execute_script("arguments[0].click();",elem)
	except NoSuchElementException:
		True

	time.sleep(1)

	try:
		elem = driver.find_element(by.By.NAME,"nextButton")
		driver.execute_script("arguments[0].click();",elem)
	except NoSuchElementException:
		True

	time.sleep(10)

	try:
		indispo = driver.find_element(by.By.XPATH,"//*[contains(text(),'existe plus de plage horaire')]")
	except NoSuchElementException:
		True

	try:
		bad_gateway = driver.find_element(by.By.XPATH,"//*[contains(text(), 'Bad Gateway')]")
	except NoSuchElementException:
		True

	try:
		overloaded = driver.find_element(by.By.XPATH,"//*[contains(text(), 'Service surchargé')]")
	except NoSuchElementException:
		True

	f = open('prefecture.txt', 'a+')
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	if indispo != 0:
		print("indisponible")
		f.write(st + " : indisponible" + "\n")
	if bad_gateway != 0:
		print("Bad Gateway")
		f.write(st + " : Bad Gateway" + "\n")
	if overloaded != 0:
		print("Service Overloaded")
		f.write(st +" :Service Overloaded" + "\n")
	if indispo == 0 and bad_gateway == 0 and overloaded == 0:
		print("OK !!")
		f.write(st + " : OK !!" + "\n")
		if sendemail:
			context = ssl.create_default_context()
			with smtplib.SMTP(smtp_server, port) as server:
				server.ehlo()  # Can be omitted
				server.starttls(context=context)
				server.ehlo()  # Can be omitted
				server.login(sender_email, password)
				server.sendmail(sender_email, "receiver1@laposte.net", message)
				server.sendmail(sender_email, "receiver2@googlemail.com", message)
	f.close()
	time.sleep(60)
