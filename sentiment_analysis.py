import pandas as pd
from textblob import TextBlob

# Define the file paths
input_file = 'amazon_reviews_all_pages.xlsx'
output_file = 'amazon_reviews_with_sentiments.xlsx'

try:
    # Confirm the actual column name for reviews
    data = pd.read_excel(input_file)
    reviews_column = 'Review'  # Replace with the correct column name if different
    print("Columns in the file:", data.columns)  # Print column names for verification
    
    # Ensure the column exists
    if reviews_column not in data.columns:
        raise ValueError(f"Column '{reviews_column}' not found in the file.")
    
    reviews = data[reviews_column].dropna()
    print("Sample reviews:")
    print(reviews.head())  # Display the first few reviews for debugging
except Exception as e:
    print(f"Error loading the file or accessing the column: {e}")
    exit()

# Perform sentiment analysis
def analyze_sentiment(review):
    try:
        analysis = TextBlob(review)
        sentiment = analysis.sentiment.polarity
        if sentiment > 0:
            return 'Positive'
        elif sentiment < 0:
            return 'Negative'
        else:
            return 'Neutral'
    except Exception as e:
        print(f"Error analyzing review: {review}, Error: {e}")
        return 'Error'

# Apply the sentiment analysis
try:
    data['Sentiment'] = reviews.apply(analyze_sentiment)
    print("Sentiment analysis completed. Saving results...")
    data.to_excel(output_file, index=False)
    print(f"Sentiment analysis results saved to {output_file}")
except Exception as e:
    print(f"Error during sentiment analysis or saving the file: {e}")
