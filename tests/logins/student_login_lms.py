# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

driver.get("http://localhost:3000")
time.sleep(2)

username_field = driver.find_element(By.NAME, "user_name")  # Change to the correct attribute
password_field = driver.find_element(By.NAME, "password")  # Change to the correct attribute


# Enter which platform you want to login to
print("Enter the platform you want to login to: ")
print("1. LMS")
print("2. Portal")

platform = input()

if platform == "1":
    print("Actor type : ")
    print("1. Student")
    print("2. Lecturer")
    print("3. Admin")

    actor_type = input()

    if actor_type == "1":
        username_field.send_keys("janith@gmail.com")
        password_field.send_keys("password123")

    
    elif actor_type == "2":
        username_field.send_keys("vishwa@gmail.com")
        password_field.send_keys("password123")

    
    elif actor_type == "3":
        username_field.send_keys("shehan@gmail.com")
        password_field.send_keys("password123")

    submit_button = driver.find_element(By.XPATH, '//button[@name="lms"]')
    submit_button.click()

elif platform == "2":
    print("Actor type : ")
    print("1. Student")
    print("3. Admin")

    actor_type = input()

    if actor_type == "1":
        username_field.send_keys("janith@gmail.com")
        password_field.send_keys("password123")
    
    elif actor_type == "3":
        username_field.send_keys("shehan@gmail.com")
        password_field.send_keys("password123")
    
    submit_button = driver.find_element(By.XPATH, '//button[@name="portal"]')
    submit_button.click()

# password_field.send_keys(Keys.RETURN)

time.sleep(100)

# # Close the browser window
# driver.quit()
