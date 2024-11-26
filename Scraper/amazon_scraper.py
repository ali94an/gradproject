from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import time

def save_cookies(driver, filepath):
    """Save cookies to a file after signing in manually."""
    with open(filepath, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, filepath):
    """Load cookies from a file."""
    with open(filepath, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def scrape_reviews_dynamic(url, output_file="reviews.xlsx"):
    # Initialize WebDriver
    driver = webdriver.Edge()
    cookies_path = "amazon_cookies.pkl"  # File to store cookies
    all_reviews = []

    try:
        # Step 1: Load Amazon homepage
        driver.get("https://www.amazon.com/")
        time.sleep(5)  # Allow the page to load

        # Step 2: Handle Cookies
        try:
            load_cookies(driver, cookies_path)  # Load saved cookies
            driver.refresh()  # Refresh page after adding cookies
            print("Cookies loaded successfully.")
        except FileNotFoundError:
            print("Cookies not found. Log in manually.")
            input("Please log in manually, then press Enter...")
            save_cookies(driver, cookies_path)
            print("Cookies saved successfully.")

        # Step 3: Navigate to the product URL
        driver.get(url)
        time.sleep(5)  # Wait for reviews to load

        # Step 4: Scrape reviews
        while True:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            review_boxes = soup.select("div[data-hook='review']")

            if not review_boxes:
                break

            for box in review_boxes:
                try:
                    review_text = box.select_one("span[data-hook='review-body']").text.strip()
                    review_date = box.select_one("span[data-hook='review-date']").text.strip()
                    review_rating = box.select_one("i[data-hook='review-star-rating']").text.strip()
                    all_reviews.append({
                        "Date": review_date,
                        "Rating": review_rating,
                        "Review": review_text,
                    })
                except AttributeError:
                    continue

            # Check for the "Next" button
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                next_button.click()
                time.sleep(5)  # Wait for the next page to load
            except:
                print("No more pages to navigate.")
                break

    finally:
        driver.quit()

    # Save reviews to Excel
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_excel(output_file, index=False)
        print(f"Saved {len(all_reviews)} reviews to {output_file}")
    else:
        print("No reviews to save.")

    return all_reviews
