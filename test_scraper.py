from Scraper.amazon_scraper import scrape_reviews_dynamic

# Test the scraper with an Amazon product reviews URL
if __name__ == "__main__":
    test_url = "https://www.amazon.com/product-reviews/B0CP8D4SM2"  # Replace with your test URL
    output_file = "amazon_reviews_all_pages.xlsx"  # Specify the output Excel file name
    reviews = scrape_reviews_dynamic(test_url, output_file)

    # Display results
    if reviews:
        print(f"Saved {len(reviews)} reviews to {output_file}.")
    else:
        print("No reviews found.")
