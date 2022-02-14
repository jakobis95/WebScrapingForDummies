[12:54] Wei, Zeping (PEG-IH)
#import library
from selenium import webdriver
import configuration.database as database
import configuration.setting as setting
import datetime
import time


#Global variables
backend = 'https://test.bematix.com/'status = 'running'
sec_user = 'SecDevelopment'
sec_password = 'CPC_IAmSuperAdmin#J1'
result = "None"
global driver
global cookies




##Functions
def login_backend():
    global backend, sec_user, sec_password, driver, cookies
    #Set option, without this option the browser will be closed automatically
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    # Open browser
    driver = webdriver.Chrome(chrome_options=option)
    driver.implicitly_wait(setting.timeout)  #Every step 20s timeout, can be defined by yourself
    #open BE
    driver.get(backend)
    driver.minimize_window()
    #login
    username = driver.find_element_by_id("name") #find id using DevTool
    password = driver.find_element_by_id("password") #analog
    login_button = driver.find_element_by_id('login')
    username.send_keys(sec_user)
    password.send_keys(sec_password)
    login_button.click()
    cookies = driver.get_cookies()
    #print(1)

