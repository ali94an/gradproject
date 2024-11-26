from selenium import webdriver
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_reviews_dynamic(url, output_file="ebay_reviews.xlsx"):
    # Set up Edge WebDriver
    service = Service(r"C:\Users\amr_q\Downloads\edgedriver_win64\msedgedriver.exe")  # Update WebDriver path
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Edge(service=service, options=options)
    all_reviews = []

    try:
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            review_boxes = soup.select('div.review-section')  # Update selector based on the eBay review page structure

            if not review_boxes:
                print("No more reviews found.")
                break

            for box in review_boxes:
                try:
                    review_text = box.select_one('.review-text').text.strip()
                    review_date = box.select_one('.review-date').text.strip()
                    review_rating = box.select_one('.review-stars').text.strip()  # Update selector
                    all_reviews.append({
                        "Date": review_date,
                        "Rating": review_rating,
                        "Review": review_text,
                    })
                except AttributeError:
                    continue

            # Check for the next button
            try:
                next_button = driver.find_element_by_css_selector('.pagination__next')
                if "disabled" in next_button.get_attribute("class"):
                    break
                next_button.click()
                time.sleep(5)
            except Exception:
                break

    finally:
        driver.quit()

    # Save to Excel
    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_excel(output_file, index=False)
        print(f"Saved {len(all_reviews)} reviews to {output_file}")
    else:
        print("No reviews to save.")

    return all_reviews
