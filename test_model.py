import json
import together
from sklearn.metrics import confusion_matrix, classification_report

# Initialize Together AI with your API key
together.api_key = "ee8552694594c67d41de1f94ee06f3922eeab8e6f5cd6cc99ed3266c329a15c6"

# Model parameters matching the Flask app
model = "meta-llama/Llama-3.2-3B-Instruct-Turbo"
temperature = 0.3
top_p = 0.8
top_k = 20
max_tokens = 10

# Function to test the model on an independent labeled dataset
def test_model_on_labeled_dataset(labeled_dataset):
    true_sentiments = []
    predicted_sentiments = []

    for data in labeled_dataset:
        review_text = data["Review"]
        true_sentiment = data["True Sentiment"]

        try:
            # Refined prompt for sentiment analysis
            prompt = (
                "You are a sentiment analysis expert. Read the review below and classify its sentiment as Positive, Neutral, or Negative. "
                "Only respond with one of these labels.\n\n"
                f"Review: {review_text}\nSentiment:"
            )

            # Call Together AI's model
            response = together.Complete.create(
                prompt=prompt,
                model=model,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                max_tokens=max_tokens
            )
            predicted_sentiment = response.get("choices")[0]["text"].strip()

            # Append true and predicted sentiments for evaluation
            true_sentiments.append(true_sentiment)
            predicted_sentiments.append(predicted_sentiment)

            # Print for manual review
            print(f"Review: {review_text}")
            print(f"True Sentiment: {true_sentiment}")
            print(f"Predicted Sentiment: {predicted_sentiment}")
            print("---")

        except Exception as e:
            print(f"Error processing review: {e}")

    # Calculate and print evaluation metrics
    print("\nConfusion Matrix:")
    print(confusion_matrix(true_sentiments, predicted_sentiments, labels=["Positive", "Neutral", "Negative"]))
    print("\nClassification Report:")
    print(classification_report(true_sentiments, predicted_sentiments, target_names=["Positive", "Neutral", "Negative"]))

# Main function to run the test
if __name__ == "__main__":
    # Path to the labeled dataset
    labeled_dataset_path = "labeled_dataset.json"

    try:
        # Load the independent labeled test dataset
        with open(labeled_dataset_path, "r") as f:
            labeled_dataset = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)

    # Run the test
    print("Testing model on labeled dataset...")
    test_model_on_labeled_dataset(labeled_dataset)
