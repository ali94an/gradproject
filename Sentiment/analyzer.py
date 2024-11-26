import pandas as pd
from transformers import pipeline
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Use Hugging Face's state-of-the-art model for sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

def analyze_sentiments(reviews):
    results = []
    for review in reviews:
        result = sentiment_pipeline(review)[0]
        sentiment = result['label']
        score = result['score']
        results.append({'Review': review, 'Sentiment': sentiment, 'Score': score})

    df = pd.DataFrame(results)

    # Generate word cloud for visual interest
    word_cloud = create_word_cloud(" ".join(reviews))

    return df, word_cloud

def create_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # Save word cloud image to base64 for HTML rendering
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return image

def generate_dashboard(df):
    sentiment_counts = df['Sentiment'].value_counts()

    # Pie Chart
    pie_chart = px.pie(
        sentiment_counts,
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title="Sentiment Distribution"
    )

    # Bar Chart
    bar_chart = px.histogram(
        df,
        x='Score',
        color='Sentiment',
        title="Sentiment Score Distribution",
        nbins=20
    )

    return pie_chart.to_html(), bar_chart.to_html()
