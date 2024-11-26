from flask import Flask, render_template, request
from Scraper.amazon_scraper import scrape_reviews_dynamic
import together
import os
import time
import json

app = Flask(__name__)

# Initialize Together AI with your API key
together.api_key = "ee8552694594c67d41de1f94ee06f3922eeab8e6f5cd6cc99ed3266c329a15c6"

# Perform sentiment analysis using Together AI
def analyze_sentiment(reviews):
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    model = "meta-llama/Llama-3.2-3B-Instruct-Turbo"

    for review in reviews:
        try:
            # Refined prompt for better performance
            prompt = (
                "You are a sentiment analysis expert. Read the review below and classify its sentiment as Positive, Neutral, or Negative. "
                "Only respond with one of these labels.\n\n"
                f"Review: {review['Review']}\nSentiment:"
            )

            # Call Together AI's model
            response = together.Complete.create(
                prompt=prompt,
                model=model,
                temperature=0.3,
                top_p=0.8,
                top_k=20,
                max_tokens=10
            )
            sentiment = response.get("choices")[0]["text"].strip()

            # Map the model's output to predefined labels
            if "positive" in sentiment.lower():
                sentiment_label = "Positive"
            elif "negative" in sentiment.lower():
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
        except Exception as e:
            print(f"Error processing review sentiment: {e}")
            sentiment_label = "Unknown"

        # Update counts
        if sentiment_label in sentiment_counts:
            sentiment_counts[sentiment_label] += 1

        # Append sentiment to review
        review["Sentiment Label"] = sentiment_label

    # Save reviews with sentiments to a file
    with open("latest_reviews.json", "w") as f:
        json.dump(reviews, f, indent=4)

    return reviews, sentiment_counts

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    product_url = request.form.get('product_url')

    # Define output directory
    output_directory = os.path.join(os.getcwd(), "output")
    os.makedirs(output_directory, exist_ok=True)

    # Unique Excel file name for this scrape
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(output_directory, f"amazon_reviews_{timestamp}.xlsx")

    # Scrape reviews
    try:
        reviews = scrape_reviews_dynamic(product_url, output_file)
    except Exception as e:
        print(f"Error during scraping: {e}")
        return "Error occurred while scraping reviews. Please try again."

    if not reviews:
        return "No reviews found. Please check the URL and try again."

    # Perform sentiment analysis
    try:
        reviews_with_sentiment, sentiment_counts = analyze_sentiment(reviews)
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        reviews_with_sentiment = []
        sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}

    # Debug prints to verify the data
    print("Reviews with Sentiment:", reviews_with_sentiment)
    print("Sentiment Counts:", sentiment_counts)
    print("Output File Path:", output_file)

    # Ensure valid data is passed to the template
    reviews_with_sentiment = reviews_with_sentiment or []
    sentiment_counts = sentiment_counts or {"Positive": 0, "Neutral": 0, "Negative": 0}

    # Render results
    try:
        return render_template(
            'results.html',
            reviews=reviews_with_sentiment,
            sentiment_counts=sentiment_counts,
            output_file=output_file
        )
    except Exception as e:
        print(f"Error rendering template: {e}")
        return "Error occurred while rendering the results. Please try again."

if __name__ == '__main__':
    app.run(debug=True)
