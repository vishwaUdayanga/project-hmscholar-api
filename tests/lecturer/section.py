# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get("http://localhost:3000")
time.sleep(2)

username_field = driver.find_element(By.NAME, "user_name")  
password_field = driver.find_element(By.NAME, "password")  


# Entering which platform you want to login to
username_field.send_keys("vishwa@gmail.com")
password_field.send_keys("password123")

submit_button = driver.find_element(By.XPATH, '//button[@name="lms"]')
submit_button.click()

time.sleep(10)

try:
    driver.get("http://localhost:3000/lecturer/dashboard/view-course/50074ded-2568-41ec-a574-5c49285352e1/settings")
    time.sleep(20)

    course_description = driver.find_element(By.NAME, "course_description")
    course_description.clear()
    course_description.send_keys("New description")

    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()

    time.sleep(10)
except:
    print("Login failed!")

