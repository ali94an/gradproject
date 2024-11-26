from selenium import webdriver
from selenium.webdriver.edge.service import Service
import pickle
import time

def save_amazon_cookies():
    service = Service(r"C:\Users\amr_q\Downloads\edgedriver_win64\msedgedriver.exe")
    driver = webdriver.Edge(service=service)

    driver.get("https://www.amazon.com/")
    print("Please log in to your Amazon account in the browser window.")
    time.sleep(60)  # Allow time to log in manually

    cookies = driver.get_cookies()
    with open("amazon_cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)
    print("Cookies saved successfully!")
    driver.quit()

if __name__ == "__main__":
    save_amazon_cookies()
